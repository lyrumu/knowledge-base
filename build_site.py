#!/usr/bin/env python3
"""
Vault Site Builder — 从 Obsidian vault 生成静态网站
支持: .md(渲染HTML) .py/.cpp/.bat等(语法高亮) .png/.jpg(内嵌图片) .mp3/.ogg(音频) .csv(表格) 其他(下载)
"""

import os
import sys
import json
import shutil
import hashlib
import mimetypes
import urllib.parse
from pathlib import Path
from datetime import datetime

try:
    import markdown
    from markdown.extensions.codehilite import CodeHiliteExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.toc import TocExtension
    from markdown.extensions.nl2br import Nl2BrExtension
except ImportError:
    print("ERROR: 需要安装 markdown 库: pip install markdown")
    sys.exit(1)

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_for_filename, get_lexer_by_name, TextLexer, guess_lexer
    from pygments.formatters import HtmlFormatter
    from pygments.util import ClassNotFound
except ImportError:
    print("ERROR: 需要安装 pygments 库: pip install pygments")
    sys.exit(1)


# ============================================================
# 配置
# ============================================================

VAULT_DIR = Path(os.environ.get("VAULT_DIR", ".")).resolve()
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "site")).resolve()
SITE_TITLE = "lyrumu's site"

# 忽略的目录
IGNORED_DIRS = {
    ".git", ".obsidian", ".smart-env", "node_modules",
    ".venv", "__pycache__", "site", ".github", ".mypy_cache",
    ".pytest_cache", "dist", "build", ".tox", ".eggs",
}

# 忽略的文件
IGNORED_FILES = {
    ".gitignore", ".DS_Store", "Thumbs.db", "desktop.ini",
    "build_site.py", "requirements.txt",
}

# 代码文件扩展名 → Pygments lexer 名
CODE_MAP = {
    ".py": "python", ".pyw": "python",
    ".cpp": "cpp", ".cxx": "cpp", ".cc": "cpp",
    ".c": "c", ".h": "c", ".hpp": "cpp",
    ".js": "javascript", ".mjs": "javascript",
    ".ts": "typescript", ".tsx": "tsx", ".jsx": "jsx",
    ".bat": "batch", ".cmd": "batch",
    ".sh": "bash", ".bash": "bash", ".zsh": "bash",
    ".f90": "fortran", ".f95": "fortran", ".f": "fortran",
    ".java": "java", ".kt": "kotlin", ".scala": "scala",
    ".rs": "rust", ".go": "go", ".rb": "ruby",
    ".php": "php", ".swift": "swift", ".dart": "dart",
    ".r": "r", ".lua": "lua", ".pl": "perl",
    ".sql": "sql", ".hs": "haskell", ".ex": "elixir",
    ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml", ".ini": "ini", ".cfg": "ini",
    ".xml": "xml", ".html": "html", ".htm": "html",
    ".css": "css", ".scss": "scss", ".less": "less",
    ".json": "json", ".jsonl": "json",
    ".dockerfile": "dockerfile",
    ".makefile": "makefile", ".cmake": "cmake",
    ".vue": "html", ".svelte": "html",
    ".mcmeta": "json", ".nbt": None,  # nbt is binary
}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp"}
AUDIO_EXTS = {".mp3", ".ogg", ".wav", ".flac", ".m4a", ".aac"}
VIDEO_EXTS = {".mp4", ".webm", ".mov", ".avi", ".mkv"}
ARCHIVE_EXTS = {".zip", ".gz", ".tar", ".rar", ".7z", ".bz2"}
FONT_EXTS = {".ttf", ".otf", ".woff", ".woff2"}

# mimetypes 补充
mimetypes.add_type("audio/ogg", ".ogg")
mimetypes.add_type("audio/flac", ".flac")
mimetypes.add_type("font/woff2", ".woff2")


# ============================================================
# 工具函数
# ============================================================

def should_ignore(path: Path) -> bool:
    """判断文件/目录是否应忽略"""
    name = path.name
    if path.is_dir():
        return name in IGNORED_DIRS or name.startswith(".")
    return name in IGNORED_FILES or name.startswith(".")


def file_ext(path: Path) -> str:
    """获取小写扩展名"""
    return path.suffix.lower()


def rel_path(path: Path, base: Path) -> str:
    """获取相对路径，URL友好"""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def output_path_for_file(rel: str) -> str:
    """将文件相对路径转为输出文件路径（磁盘上，不编码）"""
    parts = Path(rel).parts
    stem = Path(rel).stem
    parent = str(Path(*parts[:-1])) if len(parts) > 1 else ""
    if not parent:
        return f"{stem}.html"
    return f"{parent}/{stem}.html"


def href_for_file(rel: str) -> str:
    """将文件相对路径转为 HTML href（HTML 实体转义 & 等）"""
    path = output_path_for_file(rel)
    return path.replace("&", "&amp;")


def url_for_file(rel: str) -> str:
    """将文件相对路径转为 HTML 页面 URL（兼容旧调用）"""
    return href_for_file(rel)


def url_for_dir(rel: str) -> str:
    """将目录相对路径转为输出文件路径（磁盘上）"""
    parts = Path(rel).parts
    if not parts or parts == (".",):
        return "index.html"
    dir_path = "/".join(parts)
    return f"{dir_path}/index.html"


def href_for_dir(rel: str) -> str:
    """将目录相对路径转为 HTML href（HTML 实体转义）"""
    return url_for_dir(rel).replace("&", "&amp;")


def hash_content(content: bytes) -> str:
    """内容哈希，用于缓存破坏"""
    return hashlib.md5(content).hexdigest()[:8]


def get_lexer(filename: str):
    """获取代码高亮 lexer"""
    ext = Path(filename).suffix.lower()
    lexer_name = CODE_MAP.get(ext)
    if lexer_name is None:
        return None  # 二进制文件
    if lexer_name:
        try:
            return get_lexer_by_name(lexer_name)
        except Exception:
            pass
    try:
        return get_lexer_for_filename(filename)
    except ClassNotFound:
        return TextLexer()


# ============================================================
# 文件树构建
# ============================================================

class FileNode:
    """文件树节点"""
    def __init__(self, name: str, path: Path, is_dir: bool = False):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.children: list["FileNode"] = []
        self.rel: str = ""  # 相对于 vault 根的路径

    def sort_children(self):
        """排序: 目录在前，然后按名称"""
        self.children.sort(key=lambda n: (not n.is_dir, n.name.lower()))
        for child in self.children:
            child.sort_children()


def build_file_tree(vault_dir: Path) -> FileNode:
    """递归构建文件树"""
    root = FileNode(vault_dir.name, vault_dir, is_dir=True)
    root.rel = "."

    def _walk(dir_path: Path, parent: FileNode, depth: int = 0):
        if depth > 20:  # 防止无限递归
            return
        try:
            entries = sorted(dir_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            return

        for entry in entries:
            if should_ignore(entry):
                continue
            if entry.is_dir():
                node = FileNode(entry.name, entry, is_dir=True)
                node.rel = rel_path(entry, vault_dir)
                parent.children.append(node)
                _walk(entry, node, depth + 1)
            elif entry.is_file():
                node = FileNode(entry.name, entry, is_dir=False)
                node.rel = rel_path(entry, vault_dir)
                parent.children.append(node)

    _walk(vault_dir, root)
    root.sort_children()
    return root


def tree_to_html(node: FileNode, current_path: str = "", depth: int = 0) -> str:
    """将文件树渲染为 HTML 侧边栏"""
    if not node.children:
        return ""

    lines = []
    for child in node.children:
        indent = "  " * depth
        if child.is_dir:
            dir_url = href_for_dir(child.rel)
            is_active = current_path.startswith(child.rel) if current_path else False
            open_class = " open" if is_active else ""
            lines.append(f'{indent}<li class="dir{open_class}">')
            lines.append(f'{indent}  <span class="dir-toggle" onclick="this.parentElement.classList.toggle(\'open\')">▶</span>')
            lines.append(f'{indent}  <a href="{dir_url}" class="dir-link">📁 {child.name}</a>')
            sub = tree_to_html(child, current_path, depth + 1)
            if sub:
                lines.append(f'{indent}  <ul class="tree-children">{sub}</ul>')
            lines.append(f'{indent}</li>')
        else:
            ext = file_ext(child.path)
            icon = get_file_icon(ext)
            page_url = href_for_file(child.rel)
            is_active = (current_path == child.rel)
            active_class = " active" if is_active else ""
            lines.append(f'{indent}<li class="file{active_class}">')
            lines.append(f'{indent}  <a href="{page_url}">{icon} {child.name}</a>')
            lines.append(f'{indent}</li>')

    return "\n".join(lines)


def get_file_icon(ext: str) -> str:
    """根据扩展名返回图标"""
    icons = {
        ".md": "📝", ".py": "🐍", ".cpp": "⚙️", ".c": "⚙️", ".h": "⚙️",
        ".js": "📜", ".ts": "📜", ".html": "🌐", ".css": "🎨",
        ".json": "📋", ".yaml": "📋", ".yml": "📋", ".toml": "📋",
        ".bat": "🖥️", ".sh": "🖥️", ".cmd": "🖥️",
        ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️", ".gif": "🖼️", ".svg": "🖼️",
        ".mp3": "🎵", ".ogg": "🎵", ".wav": "🎵", ".flac": "🎵",
        ".mp4": "🎬", ".webm": "🎬",
        ".zip": "📦", ".gz": "📦", ".tar": "📦",
        ".pdf": "📄", ".txt": "📄", ".csv": "📊",
        ".java": "☕", ".rs": "🦀", ".go": "🐹", ".rb": "💎",
        ".f90": "📐", ".f95": "📐",
    }
    return icons.get(ext, "📄")


# ============================================================
# 内容渲染
# ============================================================

def render_markdown_file(content: str, vault_dir: Path, file_path: Path) -> str:
    """渲染 Markdown 文件为 HTML"""
    # 预处理: Obsidian wiki links [[link]] → <a>
    import re
    content = re.sub(
        r'\[\[([^\]|]+)\|([^\]]+)\]\]',
        lambda m: f'[{m.group(1)}]({m.group(2)})',
        content
    )
    content = re.sub(
        r'\[\[([^\]]+)\]\]',
        lambda m: f'[{m.group(1)}]({m.group(1)})',
        content
    )

    # 预处理: 嵌入文件 ![[file]] → 图片或链接
    content = re.sub(
        r'!\[\[([^\]]+\.(png|jpg|jpeg|gif|svg|webp))\]\]',
        lambda m: f'![{m.group(1)}]({m.group(1)})',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'!\[\[([^\]]+)\]\]',
        lambda m: f'📎 [{m.group(1)}]({m.group(1)})',
        content
    )

    extensions = [
        FencedCodeExtension(),
        CodeHiliteExtension(css_class='highlight', linenums=True, guess_lang=False),
        TableExtension(),
        TocExtension(permalink=True),
        Nl2BrExtension(),
        'markdown.extensions.nl2br',
    ]

    md = markdown.Markdown(extensions=extensions)
    html = md.convert(content)

    # 添加目录
    toc = ""
    toc_content = getattr(md, "toc", "")
    if toc_content:
        toc = f'<div class="toc"><details open><summary>📑 目录</summary>{toc_content}</details></div>'

    return toc + html


def render_code_file(content: str, filename: str) -> str:
    """渲染代码文件为语法高亮 HTML"""
    ext = Path(filename).suffix.lower()
    lexer_name = CODE_MAP.get(ext)

    if lexer_name is None:
        return '<pre class="code-block">[二进制文件，无法显示]</pre>'

    try:
        if lexer_name:
            lexer = get_lexer_by_name(lexer_name)
        else:
            lexer = get_lexer_for_filename(filename)
    except Exception:
        lexer = TextLexer()

    formatter = HtmlFormatter(
        cssclass='highlight',
        linenos=True,
        linenostart=1,
        cssstyles='font-size: 14px; line-height: 1.5;',
    )
    return highlight(content, lexer, formatter)


def render_image(rel_path: str, alt: str = "") -> str:
    """渲染图片"""
    encoded_path = urllib.parse.quote(rel_path)
    alt = alt or Path(rel_path).name
    return f'<div class="image-container"><img src="{encoded_path}" alt="{alt}" loading="lazy" onclick="this.classList.toggle(\'zoomed\')" /></div>'


def render_audio(rel_path: str) -> str:
    """渲染音频播放器"""
    encoded_path = urllib.parse.quote(rel_path)
    name = Path(rel_path).name
    return f'''<div class="audio-player">
  <p>🎵 {name}</p>
  <audio controls preload="metadata">
    <source src="{encoded_path}">
    您的浏览器不支持音频播放。
  </audio>
</div>'''


def render_csv(content: str) -> str:
    """将 CSV 渲染为 HTML 表格"""
    lines = content.strip().split("\n")
    if not lines:
        return "<p>[空文件]</p>"

    rows = []
    for line in lines:
        # 简单 CSV 解析 (不处理引号内的逗号)
        cells = [c.strip() for c in line.split(",")]
        rows.append(cells)

    html = '<div class="table-container"><table>\n'
    # 第一行作为表头
    html += "  <thead><tr>"
    for cell in rows[0]:
        html += f"<th>{cell}</th>"
    html += "</tr></thead>\n"

    html += "  <tbody>\n"
    for row in rows[1:]:
        html += "    <tr>"
        for cell in row:
            html += f"<td>{cell}</td>"
        html += "</tr>\n"
    html += "  </tbody>\n</table></div>"
    return html


# ============================================================
# HTML 模板
# ============================================================

def get_css() -> str:
    """返回完整 CSS"""
    return """
:root {
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --bg-tertiary: #1c2128;
  --bg-hover: #1f2937;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --text-muted: #6e7681;
  --border: #30363d;
  --accent: #58a6ff;
  --accent-hover: #79c0ff;
  --green: #3fb950;
  --orange: #d29922;
  --red: #f85149;
  --purple: #bc8cff;
  --sidebar-width: 300px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", Helvetica, Arial, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  display: flex;
  min-height: 100vh;
}

/* ========== 侧边栏 ========== */
.sidebar {
  width: var(--sidebar-width);
  background: var(--bg-secondary);
  border-right: 1px solid var(--border);
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  overflow-y: auto;
  z-index: 100;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease;
}

.sidebar-header {
  padding: 16px 16px 12px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.sidebar-header h1 {
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.search-box {
  width: 100%;
  padding: 6px 10px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
}

.search-box:focus { border-color: var(--accent); }
.search-box::placeholder { color: var(--text-muted); }

.tree-container {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.tree-container ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tree-container li {
  padding: 0;
}

.tree-container li a {
  display: block;
  padding: 4px 16px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: background 0.1s;
}

.tree-container li a:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.tree-container li.file a.active {
  background: rgba(88, 166, 255, 0.1);
  color: var(--accent);
  border-left: 2px solid var(--accent);
  padding-left: 14px;
}

.dir-toggle {
  display: inline-block;
  width: 16px;
  text-align: center;
  font-size: 10px;
  color: var(--text-muted);
  cursor: pointer;
  user-select: none;
  transition: transform 0.15s;
  vertical-align: middle;
}

.dir.open > .dir-toggle { transform: rotate(90deg); }

.tree-children {
  display: none;
}

.dir.open > .tree-children {
  display: block;
}

.tree-children li a { padding-left: 32px; }
.tree-children .tree-children li a { padding-left: 48px; }
.tree-children .tree-children .tree-children li a { padding-left: 64px; }

/* ========== 主内容 ========== */
.main-content {
  margin-left: var(--sidebar-width);
  flex: 1;
  min-width: 0;
}

.content-header {
  padding: 20px 40px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-secondary);
}

.content-header h1 {
  font-size: 24px;
  font-weight: 600;
}

.content-header .breadcrumb {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 4px;
}

.content-header .breadcrumb a {
  color: var(--accent);
  text-decoration: none;
}

.content-body {
  padding: 32px 40px;
  max-width: 960px;
}

/* ========== Markdown 渲染 ========== */
.content-body h1 { font-size: 2em; margin: 24px 0 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.content-body h2 { font-size: 1.5em; margin: 20px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }
.content-body h3 { font-size: 1.25em; margin: 16px 0 8px; }
.content-body h4 { font-size: 1.1em; margin: 12px 0 6px; }
.content-body h5, .content-body h6 { font-size: 1em; margin: 10px 0 4px; color: var(--text-secondary); }

.content-body p { margin: 8px 0; }
.content-body ul, .content-body ol { margin: 8px 0; padding-left: 24px; }
.content-body li { margin: 4px 0; }
.content-body blockquote {
  border-left: 4px solid var(--accent);
  padding: 8px 16px;
  margin: 12px 0;
  background: var(--bg-secondary);
  color: var(--text-secondary);
}
.content-body a { color: var(--accent); text-decoration: none; }
.content-body a:hover { text-decoration: underline; color: var(--accent-hover); }
.content-body hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }

.content-body img {
  max-width: 100%;
  border-radius: 6px;
  border: 1px solid var(--border);
}

/* 行内代码 */
.content-body code {
  background: var(--bg-tertiary);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: "SF Mono", "Fira Code", Consolas, monospace;
}

.content-body pre code {
  background: none;
  padding: 0;
  border-radius: 0;
}

/* 代码块 */
.content-body pre, .code-block {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 16px 0;
  font-size: 14px;
  line-height: 1.5;
}

/* Pygments 代码高亮 */
.highlight {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 16px 0;
}

.highlight pre {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

.highlight td {
  padding: 0;
  border: none;
}

.highlight .linenos {
  color: var(--text-muted);
  padding-right: 16px;
  border-right: 1px solid var(--border);
  user-select: none;
  text-align: right;
}

.highlight .linenodiv pre {
  color: var(--text-muted);
}

/* ========== 表格 ========== */
.table-container {
  overflow-x: auto;
  margin: 16px 0;
  border: 1px solid var(--border);
  border-radius: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th {
  background: var(--bg-tertiary);
  padding: 10px 16px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid var(--border);
}

td {
  padding: 8px 16px;
  border-bottom: 1px solid var(--border);
}

tr:last-child td { border-bottom: none; }
tr:hover { background: var(--bg-hover); }

/* ========== 特殊组件 ========== */
.toc {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
}

.toc summary {
  cursor: pointer;
  font-weight: 600;
  color: var(--text-primary);
}

.toc ul { margin: 8px 0; padding-left: 20px; }
.toc li { margin: 4px 0; }
.toc a { color: var(--accent); text-decoration: none; font-size: 14px; }
.toc a:hover { text-decoration: underline; }

.image-container {
  text-align: center;
  margin: 16px 0;
}

.image-container img {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 8px;
  border: 1px solid var(--border);
  cursor: zoom-in;
  transition: transform 0.2s;
}

.image-container img.zoomed {
  max-height: none;
  cursor: zoom-out;
  position: fixed;
  top: 5%;
  left: 5%;
  width: 90%;
  height: 90%;
  object-fit: contain;
  z-index: 1000;
  background: rgba(0,0,0,0.9);
  padding: 10px;
}

.audio-player {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
}

.audio-player p { margin-bottom: 8px; color: var(--text-secondary); }
.audio-player audio { width: 100%; }

.download-card {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px 24px;
  margin: 16px 0;
  color: var(--text-primary);
  text-decoration: none;
  transition: border-color 0.2s;
}

.download-card:hover {
  border-color: var(--accent);
  text-decoration: none;
}

.download-card .icon { font-size: 32px; }
.download-card .info { font-size: 14px; }
.download-card .name { font-weight: 600; }
.download-card .meta { color: var(--text-muted); font-size: 12px; }

/* ========== 目录列表 ========== */
.dir-list {
  list-style: none;
  padding: 0;
  margin: 16px 0;
}

.dir-list li {
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
}

.dir-list li:last-child { border-bottom: none; }

.dir-list li a {
  color: var(--text-primary);
  text-decoration: none;
  display: block;
}

.dir-list li a:hover {
  color: var(--accent);
  background: var(--bg-hover);
  border-radius: 4px;
}

/* ========== 移动端 ========== */
.menu-toggle {
  display: none;
  position: fixed;
  top: 12px;
  left: 12px;
  z-index: 200;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 12px;
  color: var(--text-primary);
  cursor: pointer;
  font-size: 18px;
}

@media (max-width: 768px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); box-shadow: 4px 0 20px rgba(0,0,0,0.5); }
  .main-content { margin-left: 0; }
  .menu-toggle { display: block; }
  .content-header, .content-body { padding-left: 16px; padding-right: 16px; }
}

/* ========== 滚动条 ========== */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ========== 打印 ========== */
@media print {
  .sidebar, .menu-toggle { display: none !important; }
  .main-content { margin-left: 0 !important; }
}
"""


def get_js() -> str:
    """返回 JavaScript"""
    return """
// 搜索过滤
document.addEventListener('DOMContentLoaded', function() {
  const searchBox = document.querySelector('.search-box');
  if (!searchBox) return;

  const treeItems = document.querySelectorAll('.tree-container li');

  searchBox.addEventListener('input', function() {
    const query = this.value.toLowerCase().trim();

    if (!query) {
      treeItems.forEach(item => item.style.display = '');
      return;
    }

    // 收集所有匹配项及其父目录
    const matches = new Set();
    treeItems.forEach(item => {
      const text = item.textContent.toLowerCase();
      if (text.includes(query)) {
        // 标记此项和所有祖先
        let el = item.parentElement;
        while (el && el.classList) {
          if (el.tagName === 'LI') {
            matches.add(el);
            el.classList.add('open');
          }
          el = el.parentElement;
        }
        // 标记子项
        item.querySelectorAll('li').forEach(child => matches.add(child));
        matches.add(item);
      }
    });

    treeItems.forEach(item => {
      item.style.display = matches.has(item) ? '' : 'none';
    });
  });

  // 展开/折叠所有目录
  document.querySelectorAll('.dir-toggle').forEach(toggle => {
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.parentElement.classList.toggle('open');
    });
  });
});
"""


# ============================================================
# 页面生成
# ============================================================

def generate_html_page(
    content_html: str,
    title: str,
    file_rel: str,
    file_tree_html: str,
    current_rel: str,
    page_type: str = "content",
) -> str:
    """生成完整的 HTML 页面"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — {SITE_TITLE}</title>
  <style>{get_css()}</style>
</head>
<body>
  <button class="menu-toggle" onclick="document.querySelector('.sidebar').classList.toggle('open')">☰</button>

  <nav class="sidebar">
    <div class="sidebar-header">
      <h1><a href="index.html" style="color:inherit;text-decoration:none">📚 {SITE_TITLE}</a></h1>
      <input type="text" class="search-box" placeholder="搜索文件...">
    </div>
    <div class="tree-container">
      <ul>{file_tree_html}</ul>
    </div>
  </nav>

  <main class="main-content">
    <div class="content-header">
      <h1>{title}</h1>
      <div class="breadcrumb">{_breadcrumb(file_rel)}</div>
    </div>
    <div class="content-body">
      {content_html}
    </div>
  </main>

  <script>{get_js()}</script>
</body>
</html>"""


def _breadcrumb(file_rel: str) -> str:
    """生成面包屑导航"""
    parts = Path(file_rel).parts
    if not parts or parts == (".",):
        return '<a href="index.html">🏠 Home</a>'
    crumbs = ['<a href="index.html">🏠 Home</a>']
    for i, part in enumerate(parts[:-1]):
        # 链接到目录的 index.html
        dir_path = "/".join(parts[:i+1])
        dir_url = href_for_dir(dir_path)
        crumbs.append(f'<a href="{dir_url}">{part}</a>')
    crumbs.append(f'<span>{parts[-1]}</span>')
    return " / ".join(crumbs)


# ============================================================
# 主构建流程
# ============================================================

def build():
    """主构建函数"""
    print(f"🔨 Vault Site Builder")
    print(f"   源目录: {VAULT_DIR}")
    print(f"   输出目录: {OUTPUT_DIR}")
    print()

    # 1. 清理输出目录
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # 2. 构建文件树
    print("📁 构建文件树...")
    tree = build_file_tree(VAULT_DIR)
    tree_html = tree_to_html(tree)

    # 3. 统计
    stats = {"md": 0, "code": 0, "image": 0, "audio": 0, "other": 0}
    all_files = []

    def collect_files(node: FileNode):
        for child in node.children:
            if child.is_dir:
                collect_files(child)
            else:
                all_files.append(child)
    collect_files(tree)

    print(f"   找到 {len(all_files)} 个文件")

    # 4. 逐个处理文件
    print("🔨 生成页面...")
    for fnode in all_files:
        ext = file_ext(fnode.path)
        rel = fnode.rel
        page_url = output_path_for_file(rel)

        # 创建输出目录
        out_path = OUTPUT_DIR / page_url
        out_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if ext == ".md":
                # Markdown 文件
                content = fnode.path.read_text(encoding="utf-8", errors="replace")
                rendered = render_markdown_file(content, VAULT_DIR, fnode.path)
                html = generate_html_page(rendered, fnode.path.stem, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["md"] += 1

            elif ext in CODE_MAP:
                # 代码文件
                content = fnode.path.read_text(encoding="utf-8", errors="replace")
                rendered = render_code_file(content, fnode.path.name)
                title = fnode.path.name
                html = generate_html_page(rendered, title, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["code"] += 1

            elif ext in IMAGE_EXTS:
                # 图片 → 复制到输出目录 + 生成展示页
                media_out = OUTPUT_DIR / "media" / rel
                media_out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fnode.path, media_out)

                media_url = "media/" + rel
                rendered = render_image(media_url, fnode.path.name)
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["image"] += 1

            elif ext in AUDIO_EXTS:
                # 音频 → 复制到输出目录 + 生成播放页
                media_out = OUTPUT_DIR / "media" / rel
                media_out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fnode.path, media_out)

                media_url = "media/" + rel
                rendered = render_audio(media_url)
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["audio"] += 1

            elif ext == ".csv":
                # CSV → 表格
                content = fnode.path.read_text(encoding="utf-8", errors="replace")
                rendered = render_csv(content)
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["other"] += 1

            elif ext in {".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".mcmeta"}:
                # 配置/数据文件 → 代码高亮
                content = fnode.path.read_text(encoding="utf-8", errors="replace")
                rendered = render_code_file(content, fnode.path.name)
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["code"] += 1

            else:
                # 其他文件 → 下载链接
                file_size = fnode.path.stat().st_size
                size_str = format_size(file_size)
                encoded = urllib.parse.quote(rel)
                icon = get_file_icon(ext)
                rendered = f'''<div class="download-card" href="{encoded}">
  <span class="icon">{icon}</span>
  <div class="info">
    <div class="name">{fnode.path.name}</div>
    <div class="meta">{size_str} — 点击下载</div>
  </div>
</div>
<p style="margin-top:16px;color:var(--text-muted)">此文件类型无法在浏览器中直接预览。</p>'''
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["other"] += 1

            print(f"   ✓ {rel}")

        except Exception as e:
            print(f"   ✗ {rel}: {e}")

    # 5. 生成目录索引页
    print("📁 生成目录索引...")
    dirs_processed = set()

    def gen_dir_index(node: FileNode, parent_rel: str = "."):
        """为每个目录生成 index.html"""
        if parent_rel in dirs_processed:
            return
        dirs_processed.add(parent_rel)

        dir_url = url_for_dir(parent_rel)
        out_path = OUTPUT_DIR / dir_url
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # 生成目录内容列表
        items_html = ""
        for child in node.children:
            if child.is_dir:
                d_url = href_for_dir(child.rel)
                items_html += f'<li><a href="{d_url}">📁 {child.name}/</a></li>\n'
            else:
                ext = file_ext(child.path)
                icon = get_file_icon(ext)
                f_url = href_for_file(child.rel)
                items_html += f'<li><a href="{f_url}">{icon} {child.name}</a></li>\n'

        dir_name = Path(parent_rel).name if parent_rel != "." else SITE_TITLE
        content = f"<h1>📁 {dir_name}</h1>\n<ul class='dir-list'>\n{items_html}</ul>"
        html = generate_html_page(content, dir_name, parent_rel, tree_html, parent_rel)
        out_path.write_text(html, encoding="utf-8")

        for child in node.children:
            if child.is_dir:
                gen_dir_index(child, child.rel)

    gen_dir_index(tree)

    # 6. 生成首页
    print("📄 生成首页...")
    index_content = f"""
<h1>📚 {SITE_TITLE}</h1>
<p>由 Obsidian vault 自动生成，最后构建: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<hr>
<h2>📊 统计</h2>
<table>
  <thead><tr><th>类型</th><th>数量</th></tr></thead>
  <tbody>
    <tr><td>📝 Markdown</td><td>{stats['md']}</td></tr>
    <tr><td>💻 代码/配置</td><td>{stats['code']}</td></tr>
    <tr><td>🖼️ 图片</td><td>{stats['image']}</td></tr>
    <tr><td>🎵 音频</td><td>{stats['audio']}</td></tr>
    <tr><td>📦 其他</td><td>{stats['other']}</td></tr>
    <tr><td><strong>总计</strong></td><td><strong>{sum(stats.values())}</strong></td></tr>
  </tbody>
</table>
<h2>📁 文件结构</h2>
<p>使用左侧边栏浏览所有文件。</p>
"""
    index_html = generate_html_page(index_content, "Home", ".", tree_html, ".", page_type="index")
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    print()
    print(f"✅ 构建完成！")
    print(f"   📝 Markdown: {stats['md']}")
    print(f"   💻 代码/配置: {stats['code']}")
    print(f"   🖼️ 图片: {stats['image']}")
    print(f"   🎵 音频: {stats['audio']}")
    print(f"   📦 其他: {stats['other']}")
    print(f"   📊 总计: {sum(stats.values())} 个页面")
    print(f"   📂 输出: {OUTPUT_DIR}")


def format_size(size: int) -> str:
    """格式化文件大小"""
    s = float(size)
    for unit in ["B", "KB", "MB", "GB"]:
        if s < 1024:
            return f"{s:.1f} {unit}"
        s /= 1024
    return f"{s:.1f} TB"


if __name__ == "__main__":
    build()
