#!/usr/bin/env python3
"""
Vault Site Builder — 从 Obsidian vault 生成静态网站
使用 Prism.js 代码高亮 + Fuse.js 搜索 + 自定义 CSS
"""

import os
import sys
import json
import shutil
import hashlib
import urllib.parse
from pathlib import Path
from datetime import datetime

try:
    import markdown
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.toc import TocExtension
except ImportError:
    print("ERROR: pip install markdown")
    sys.exit(1)

# ============================================================
# 配置
# ============================================================
VAULT_DIR = Path(os.environ.get("VAULT_DIR", ".")).resolve()
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "site")).resolve()
STATIC_DIR = Path(__file__).parent / "static"
SITE_TITLE = "lyrumu's site"
SITE_REPO = "knowledge-base"

IGNORED_DIRS = {
    ".git", ".obsidian", ".smart-env", "node_modules",
    ".venv", "__pycache__", "site", ".github", ".mypy_cache",
    ".pytest_cache", "dist", "build", ".tox", ".eggs", "static",
}
IGNORED_FILES = {
    ".gitignore", ".DS_Store", "Thumbs.db", "desktop.ini",
    "build_site.py", "requirements.txt", "LICENSE",
}

# 扩展名 → Prism.js 语言名
LANG_MAP = {
    ".py": "python", ".pyw": "python",
    ".cpp": "cpp", ".cxx": "cpp", ".cc": "cpp",
    ".c": "c", ".h": "c", ".hpp": "cpp",
    ".js": "javascript", ".mjs": "javascript",
    ".ts": "typescript", ".tsx": "tsx", ".jsx": "jsx",
    ".bat": "batch", ".cmd": "batch",
    ".sh": "bash", ".bash": "bash",
    ".f90": "fortran", ".f95": "fortran",
    ".java": "java", ".kt": "kotlin", ".scala": "scala",
    ".rs": "rust", ".go": "go", ".rb": "ruby",
    ".php": "php", ".swift": "swift",
    ".r": "r", ".lua": "lua", ".pl": "perl",
    ".sql": "sql",
    ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml", ".ini": "ini",
    ".xml": "xml", ".html": "html", ".htm": "html",
    ".css": "css", ".scss": "scss",
    ".json": "json", ".jsonl": "json",
    ".mcmeta": "json",
}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp"}
AUDIO_EXTS = {".mp3", ".ogg", ".wav", ".flac", ".m4a", ".aac"}

# ============================================================
# 工具函数
# ============================================================
def should_ignore(path: Path) -> bool:
    name = path.name
    if path.is_dir():
        return name in IGNORED_DIRS or name.startswith(".")
    return name in IGNORED_FILES or name.startswith(".")

def file_ext(path: Path) -> str:
    return path.suffix.lower()

def rel_path(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)

def output_path_for_file(rel: str) -> str:
    parts = Path(rel).parts
    stem = Path(rel).stem
    parent = str(Path(*parts[:-1])) if len(parts) > 1 else ""
    if not parent:
        return f"{stem}.html"
    return f"{parent}/{stem}.html"

def href_for_file(rel: str) -> str:
    return "/" + SITE_REPO + "/" + output_path_for_file(rel)

def url_for_dir(rel: str) -> str:
    parts = Path(rel).parts
    if not parts or parts == (".",):
        return "index.html"
    return "/".join(parts) + "/index.html"

def href_for_dir(rel: str) -> str:
    return "/" + SITE_REPO + "/" + url_for_dir(rel)

def get_file_icon(ext: str) -> str:
    icons = {
        ".md": "📝", ".py": "🐍", ".cpp": "⚙️", ".c": "⚙️", ".h": "⚙️",
        ".js": "📜", ".ts": "📜", ".html": "🌐", ".css": "🎨",
        ".json": "📋", ".yaml": "📋", ".yml": "📋", ".toml": "📋",
        ".bat": "🖥️", ".sh": "🖥️",
        ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️", ".gif": "🖼️", ".svg": "🖼️",
        ".mp3": "🎵", ".ogg": "🎵", ".wav": "🎵", ".flac": "🎵",
        ".zip": "📦", ".gz": "📦", ".tar": "📦",
        ".pdf": "📄", ".txt": "📄", ".csv": "📊",
        ".java": "☕", ".rs": "🦀", ".go": "🐹",
        ".f90": "📐",
    }
    return icons.get(ext, "📄")

def format_size(size: int) -> str:
    s = float(size)
    for unit in ["B", "KB", "MB", "GB"]:
        if s < 1024:
            return f"{s:.1f} {unit}"
        s /= 1024
    return f"{s:.1f} TB"

def html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ============================================================
# 文件树
# ============================================================
class FileNode:
    def __init__(self, name, path, is_dir=False):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.children = []
        self.rel = ""

    def sort_children(self):
        self.children.sort(key=lambda n: (not n.is_dir, n.name.lower()))
        for c in self.children:
            c.sort_children()

def build_file_tree(vault_dir):
    root = FileNode(vault_dir.name, vault_dir, is_dir=True)
    root.rel = "."

    def walk(d, parent, depth=0):
        if depth > 20: return
        try:
            entries = sorted(d.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            return
        for e in entries:
            if should_ignore(e): continue
            node = FileNode(e.name, e, is_dir=e.is_dir())
            node.rel = rel_path(e, vault_dir)
            parent.children.append(node)
            if e.is_dir():
                walk(e, node, depth + 1)

    walk(vault_dir, root)
    root.sort_children()
    return root

def tree_to_html(node, current_path="", depth=0):
    if not node.children:
        return ""
    lines = []
    for child in node.children:
        if child.is_dir:
            is_open = current_path.startswith(child.rel) if current_path else False
            open_cls = " open" if is_open else ""
            href = href_for_dir(child.rel)
            lines.append(f'<li class="tree-item dir{open_cls}">')
            lines.append(f'  <div class="toggle-row"><span class="toggle-icon">▶</span><a href="{href}">📁 {child.name}</a></div>')
            sub = tree_to_html(child, current_path, depth + 1)
            if sub:
                lines.append(f'  <ul class="tree-children">{sub}</ul>')
            lines.append('</li>')
        else:
            ext = file_ext(child.path)
            icon = get_file_icon(ext)
            href = href_for_file(child.rel)
            is_active = (current_path == child.rel)
            active_cls = " active" if is_active else ""
            lines.append(f'<li class="tree-item file{active_cls}">')
            lines.append(f'  <a href="{href}">{icon} {child.name}</a>')
            lines.append('</li>')
    return "\n".join(lines)

# ============================================================
# 内容渲染
# ============================================================
def render_markdown_file(content, vault_dir, file_path):
    import re

    # Obsidian wiki links [[link|alias]] → [alias](link)
    content = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'[\2](\1)', content)
    content = re.sub(r'\[\[([^\]]+)\]\]', r'[\1](\1)', content)

    # Embedded files ![[file.png]] → <img>
    content = re.sub(
        r'!\[\[([^\]]+\.(png|jpg|jpeg|gif|svg|webp))\]\]',
        lambda m: f'![{m.group(1)}]({m.group(1)})',
        content, flags=re.IGNORECASE
    )
    content = re.sub(r'!\[\[([^\]]+)\]\]', r'📎 [\1](\1)', content)

    md = markdown.Markdown(extensions=[
        FencedCodeExtension(),
        TableExtension(),
        TocExtension(permalink=True),
        'pymdownx.tilde',          # ~~删除线~~
        'pymdownx.mark',           # ==高亮==
        'pymdownx.tasklist',       # - [ ] 任务列表
        'pymdownx.details',        # 可折叠 details
        'pymdownx.emoji',          # :emoji:
        'pymdownx.keys',           # <kbd>键盘按键
        'pymdownx.smartsymbols',   # 自动替换符号 → 1/2 等
        'pymdownx.striphtml',      # 移除 HTML 标签（可选）
    ], extension_configs={
        'pymdownx.emoji': {
            'emoji_index': 'twemoji',
            'emoji_generator': 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/',
        },
        'pymdownx.tasklist': {
            'custom_checkbox': True,
        },
    })
    html = md.convert(content)

    toc = ""
    if getattr(md, "toc", ""):
        toc = f'<div class="toc"><details open><summary>目录</summary>{md.toc}</details></div>'

    return toc + html

def render_code_file(content, filename):
    ext = Path(filename).suffix.lower()
    lang = LANG_MAP.get(ext, "")
    escaped = html_escape(content)

    if lang:
        return f'<pre class="line-numbers"><code class="language-{lang}">{escaped}</code></pre>'
    else:
        return f'<pre class="line-numbers"><code>{escaped}</code></pre>'

def render_image(media_url, alt=""):
    alt = alt or Path(media_url).name
    return f'<div class="image-container"><img src="{media_url}" alt="{alt}" loading="lazy"></div>'

def render_audio(media_url):
    name = Path(media_url).name
    return f'''<div class="audio-player">
  <p>🎵 {name}</p>
  <audio controls preload="metadata"><source src="{media_url}">不支持音频</audio>
</div>'''

def render_csv(content):
    lines = content.strip().split("\n")
    if not lines: return "<p>[空文件]</p>"
    rows = [[c.strip() for c in line.split(",")] for line in lines]
    h = "<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr></thead><tbody>"
    for row in rows[1:]:
        h += "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
    h += "</tbody></table>"
    return f'<div class="table-container">{h}</div>'

# ============================================================
# HTML 模板
# ============================================================
def _breadcrumb(file_rel):
    parts = Path(file_rel).parts
    if not parts or parts == (".",):
        return '<a href="/' + SITE_REPO + '/">🏠 Home</a>'
    crumbs = [f'<a href="/{SITE_REPO}/">🏠 Home</a>']
    for i, part in enumerate(parts[:-1]):
        d = "/".join(parts[:i+1])
        crumbs.append(f'<a href="{href_for_dir(d)}">{html_escape(part)}</a>')
    crumbs.append(f'<span>{html_escape(parts[-1])}</span>')
    return " / ".join(crumbs)

def generate_html_page(content_html, title, file_rel, file_tree_html, current_rel):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_escape(title)} — {SITE_TITLE}</title>
  <link rel="stylesheet" href="/{SITE_REPO}/static/style.css">
  <link rel="stylesheet" href="/{SITE_REPO}/static/prism-theme.css">
  <link rel="stylesheet" href="/{SITE_REPO}/static/prism-line-numbers.css">
</head>
<body>
  <button class="menu-toggle" aria-label="Toggle menu">☰</button>
  <div class="sidebar-overlay"></div>

  <nav class="sidebar">
    <div class="sidebar-header">
      <h1><a href="/{SITE_REPO}/">📚 {SITE_TITLE}</a></h1>
      <div class="search-wrapper">
        <input type="text" class="search-box" placeholder="搜索... (Ctrl+K)">
      </div>
    </div>
    <div class="tree-container">
      <ul>{file_tree_html}</ul>
    </div>
  </nav>

  <main class="main-content">
    <div class="content-header">
      <h1>{html_escape(title)}</h1>
      <div class="breadcrumb">{_breadcrumb(file_rel)}</div>
    </div>
    <div class="content-body">
      {content_html}
    </div>
  </main>

  <script src="/{SITE_REPO}/static/prism.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-python.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-c.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-cpp.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-javascript.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-bash.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-json.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-yaml.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-java.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-rust.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-go.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-sql.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-lua.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-typescript.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-ruby.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-r.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-makefile.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-cmake.min.js"></script>
  <script src="/{SITE_REPO}/static/prism-line-numbers.min.js"></script>
  <script src="/{SITE_REPO}/static/fuse.min.js"></script>
  <script src="/{SITE_REPO}/static/app.js"></script>
</body>
</html>'''

# ============================================================
# 构建
# ============================================================
def build():
    print(f"🔨 Vault Site Builder")
    print(f"   源: {VAULT_DIR}")
    print(f"   输出: {OUTPUT_DIR}")
    print()

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # 复制 static/
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")
        print(f"📦 复制 static/ ({len(list((OUTPUT_DIR / 'static').iterdir()))} files)")

    # 构建文件树
    print("📁 构建文件树...")
    tree = build_file_tree(VAULT_DIR)
    tree_html = tree_to_html(tree)

    # 统计
    stats = {"md": 0, "code": 0, "image": 0, "audio": 0, "other": 0}
    all_files = []
    def collect(n):
        for c in n.children:
            if c.is_dir: collect(c)
            else: all_files.append(c)
    collect(tree)
    print(f"   找到 {len(all_files)} 个文件")

    # 处理文件
    print("🔨 生成页面...")
    for fnode in all_files:
        ext = file_ext(fnode.path)
        rel = fnode.rel
        out_path = OUTPUT_DIR / output_path_for_file(rel)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if ext == ".md":
                content = fnode.path.read_text(encoding="utf-8", errors="replace")
                rendered = render_markdown_file(content, VAULT_DIR, fnode.path)
                html = generate_html_page(rendered, fnode.path.stem, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["md"] += 1

            elif ext in LANG_MAP:
                content = fnode.path.read_text(encoding="utf-8", errors="replace")
                rendered = render_code_file(content, fnode.path.name)
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["code"] += 1

            elif ext in IMAGE_EXTS:
                media_out = OUTPUT_DIR / "media" / rel
                media_out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fnode.path, media_out)
                media_url = "/" + SITE_REPO + "/media/" + rel
                rendered = render_image(media_url, fnode.path.name)
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["image"] += 1

            elif ext in AUDIO_EXTS:
                media_out = OUTPUT_DIR / "media" / rel
                media_out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fnode.path, media_out)
                media_url = "/" + SITE_REPO + "/media/" + rel
                rendered = render_audio(media_url)
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["audio"] += 1

            elif ext == ".csv":
                content = fnode.path.read_text(encoding="utf-8", errors="replace")
                rendered = render_csv(content)
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["other"] += 1

            elif ext in {".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".mcmeta"}:
                content = fnode.path.read_text(encoding="utf-8", errors="replace")
                lang = LANG_MAP.get(ext, "")
                escaped = html_escape(content)
                if lang:
                    rendered = f'<pre class="line-numbers"><code class="language-{lang}">{escaped}</code></pre>'
                else:
                    rendered = f'<pre class="line-numbers"><code>{escaped}</code></pre>'
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["code"] += 1

            else:
                file_size = fnode.path.stat().st_size
                size_str = format_size(file_size)
                encoded = "/" + SITE_REPO + "/" + urllib.parse.quote(rel)
                icon = get_file_icon(ext)
                rendered = f'''<div class="download-card" href="{encoded}">
  <span class="icon">{icon}</span>
  <div><div class="name">{html_escape(fnode.path.name)}</div><div class="meta">{size_str} — 点击下载</div></div>
</div>'''
                html = generate_html_page(rendered, fnode.path.name, rel, tree_html, rel)
                out_path.write_text(html, encoding="utf-8")
                stats["other"] += 1

            print(f"   ✓ {rel}")
        except Exception as e:
            print(f"   ✗ {rel}: {e}")

    # 目录索引
    print("📁 生成目录索引...")
    dirs_done = set()

    def gen_dir_index(node, parent_rel="."):
        if parent_rel in dirs_done: return
        dirs_done.add(parent_rel)
        out_path = OUTPUT_DIR / url_for_dir(parent_rel)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        items = ""
        for child in node.children:
            if child.is_dir:
                items += f'<li><a href="{href_for_dir(child.rel)}">📁 {html_escape(child.name)}/</a></li>\n'
            else:
                ext = file_ext(child.path)
                icon = get_file_icon(ext)
                items += f'<li><a href="{href_for_file(child.rel)}">{icon} {html_escape(child.name)}</a></li>\n'

        dir_name = Path(parent_rel).name if parent_rel != "." else SITE_TITLE
        content = f"<h1>📁 {html_escape(dir_name)}</h1>\n<ul class='dir-list'>\n{items}</ul>"
        html = generate_html_page(content, dir_name, parent_rel, tree_html, parent_rel)
        out_path.write_text(html, encoding="utf-8")

        for child in node.children:
            if child.is_dir:
                gen_dir_index(child, child.rel)

    gen_dir_index(tree)

    # 首页
    print("📄 生成首页...")
    # 尝试用 README.md 作为首页内容
    readme_path = VAULT_DIR / "README.md"
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding="utf-8", errors="replace")
        index_content = render_markdown_file(readme_content, VAULT_DIR, readme_path)
        index_content += f'\n<hr>\n<p style="color:var(--text-muted);font-size:13px;margin-top:24px">最后构建: {datetime.now().strftime("%Y-%m-%d %H:%M")} · 共 {sum(stats.values())} 个文件</p>'
    else:
        index_content = f"""
<h1>📚 {SITE_TITLE}</h1>
<p style="color:var(--text-dim)">由 Obsidian vault 自动生成 · 最后构建: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<p style="color:var(--text-dim);margin-top:16px">使用左侧边栏浏览所有文件。</p>
"""
    index_html = generate_html_page(index_content, "Home", ".", tree_html, ".")
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    print(f"\n✅ 构建完成！{sum(stats.values())} 个页面 → {OUTPUT_DIR}")

if __name__ == "__main__":
    build()
