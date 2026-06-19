$ErrorActionPreference = "Stop"

$Content = "f:\Notes\content\notes"

$DocsRestructure = @(
@{ old = "docs/docker-dify";                new = "docs/docker/docker-dify" }
@{ old = "docs/flutter-dart-trae";          new = "docs/flutter/flutter-dart-trae" }
@{ old = "docs/git-basics";                 new = "docs/git/git-basics" }
@{ old = "docs/app-notes";                  new = "docs/apps/app-notes" }
@{ old = "docs/vscode-cpp-env";             new = "docs/vscode/vscode-cpp-env" }
@{ old = "docs/vscode-python-env";          new = "docs/vscode/vscode-python-env" }
@{ old = "docs/wsl2-vmware-fix";            new = "docs/wsl2/fix/wsl2-vmware-fix" }
@{ old = "docs/wsl2-vmware-fix-2";          new = "docs/wsl2/fix/wsl2-vmware-fix-2" }
@{ old = "docs/wsl2-winnat-fix";            new = "docs/wsl2/fix/wsl2-winnat-fix" }
@{ old = "docs/wsl2-hermes-agent";          new = "docs/wsl2/hermes/wsl2-hermes-agent" }
@{ old = "docs/wsl2-hermes-api";            new = "docs/wsl2/hermes/wsl2-hermes-api" }
@{ old = "docs/wsl2-hermes-dashboard";      new = "docs/wsl2/hermes/wsl2-hermes-dashboard" }
@{ old = "docs/wsl2-opencode";              new = "docs/wsl2/opencode/wsl2-opencode" }
@{ old = "docs/wsl2-opencode-mcp";          new = "docs/wsl2/opencode/wsl2-opencode-mcp" }
)

$LanguageRestructure = @(
@{ old = "language/cpp-algo-notes";            new = "language/cpp-algorithm/basic-cpp/algo-notes" }
@{ old = "language/cpp-examples";              new = "language/cpp-algorithm/basic-cpp/examples" }
@{ old = "language/cpp-graph";                 new = "language/cpp-algorithm/basic-cpp/graph" }
@{ old = "language/cpp-applications";          new = "language/cpp-algorithm/other-cpp/applications" }
@{ old = "language/cpp-data-structures";       new = "language/cpp-algorithm/other-cpp/data-structures" }
@{ old = "language/python-pycharm";            new = "language/python/python-note/pycharm" }
)

$DemoRestructure = @(
@{ old = "demo/minecraft-datapacks-notes";     new = "demo/minecraft/datapacks-notes" }
@{ old = "demo/minecraft-patpat-wiki";         new = "demo/minecraft/patpat-wiki" }
@{ old = "demo/minecraft-patpat-guide";        new = "demo/minecraft/patpat-guide" }
)

$IndexDefsMap = @{
"docs" = "Docs|DOCS - 文档|环境配置 / 工具使用 / 踩坑记录。"
"docs|docker" = "Docker|DOCKER - 容器|Docker 折腾记录：WSL2 集成 / 镜像 / 部署。"
"docs|flutter" = "Flutter|FLUTTER - 跨端|Flutter + Dart 配置 / 插件 / 实践。"
"docs|git" = "Git|GIT - 版本控制|Git 常用命令 / 多账号 / 常见问题。"
"docs|apps" = "其他 Apps|APPS - 其他工具|Windows / Ubuntu 下杂七杂八的工具使用笔记。"
"docs|vscode" = "VSCode|VSCODE - 编辑器|VSCode 环境配置：C++ 刷题 / Python 开发。"
"docs|wsl2" = "WSL2|WSL2 - Linux 子系统|WSL2 安装 / 配置 / 周边工具（Hermes / Opencode）。"
"docs|wsl2|fix" = "WSL2 · Fix|WSL2 - 修复|WSL2 各种坑的修复记录。"
"docs|wsl2|hermes" = "WSL2 · Hermes|WSL2 - Hermes Agent|Hermes Agent 安装 / API / Dashboard 修复。"
"docs|wsl2|opencode" = "WSL2 · Opencode|WSL2 - Opencode|Opencode Agent / MCP 配置。"
"language" = "Language|LANGUAGE - 语言|C++ 算法 / Python 语法 / 代码模板。"
"language|cpp-algorithm" = "C++ Algorithm|C++ - 算法|C++ 算法笔记 / 模板 / 题解。"
"language|cpp-algorithm|basic-cpp" = "C++ · 基础算法|C++ - BASIC|C++ 基础算法笔记：DP / 图论 / 字符串。"
"language|cpp-algorithm|other-cpp" = "C++ · 其他|C++ - APPLICATIONS|C++ 应用 / 数据结构 / 资料。"
"language|python" = "Python|PYTHON|Python 语法 / 工具 / 笔记。"
"language|python|python-note" = "Python · Note|PYTHON - NOTE|Python 开发笔记。"
"demo" = "Demo && Resources|DEMO - 示例与资源|AI 入门 / Minecraft / Agent 实验。"
"demo|minecraft" = "Minecraft|MINECRAFT - 我的世界|Minecraft 数据包 / 资源包 / 材质 / 音乐 / 皮肤。"
}

function Get-IndexDef([string]$Path) {
    $key = $Path -replace '/', '|'
    $raw = $IndexDefsMap[$key]
    if (-not $raw) { return $null }
    $parts = $raw -split '\|', 3
    return @{ T = $parts[0]; K = $parts[1]; S = $parts[2] }
}

function New-SectionIndex {
    param([string]$RelDir)
    $def = Get-IndexDef -Path $RelDir
    if (-not $def) { Write-Host "  [NODEF] $RelDir" -ForegroundColor Yellow; return }
    $frontmatter = @(
        '---'
        "title: `"$($def.T)`""
        "kicker: `"$($def.K)`""
        "subtitle: `"$($def.S)`""
        "description: `"$($def.T)`""
        'layout: "page"'
        'showHero: false'
        'showBreadcrumbs: false'
        'showTableOfContents: false'
        '---'
        ''
    ) -join "`n"
    $fullPath = Join-Path $Content $RelDir
    New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
    Set-Content -Path (Join-Path $fullPath "_index.md") -Value $frontmatter -Encoding UTF8
    Write-Host "  [INDEX] $RelDir" -ForegroundColor Green
}

function Move-LeafBundle {
    param([string]$Old, [string]$New)
    $src = Join-Path $Content $Old
    $dst = Join-Path $Content $New
    if (-not (Test-Path $src)) { Write-Host "  [MISS] $Old" -ForegroundColor Red; return }
    if (Test-Path $dst) { Write-Host "  [SKIP] $New exists" -ForegroundColor DarkGray; return }
    New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null
    Move-Item -Path $src -Destination $dst -Force
    Write-Host "  [MOVE]  $Old -> $New" -ForegroundColor Cyan
}

function Remove-EmptyDirs {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return }
    $items = @(Get-ChildItem -Path $Path -Force -Recurse -Directory | Sort-Object { $_.FullName.Length } -Descending)
    foreach ($d in $items) {
        $hasContent = @(Get-ChildItem -Path $d.FullName -Force | Where-Object { -not $_.PSIsContainer }).Count
        if ($hasContent -eq 0) {
            Remove-Item -Path $d.FullName -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "  [RMDIR] $($d.FullName.Replace($Content + '\', ''))" -ForegroundColor DarkGray
        }
    }
}

Write-Host ""
Write-Host "=== A. Docs 嵌套化 ===" -ForegroundColor Cyan
foreach ($m in $DocsRestructure) { Move-LeafBundle -Old $m.old -New $m.new }
foreach ($k in @("docs","docs/docker","docs/flutter","docs/git","docs/apps","docs/vscode","docs/wsl2/fix","docs/wsl2/hermes","docs/wsl2/opencode")) {
    New-SectionIndex -RelDir $k
}

Write-Host ""
Write-Host "=== B. Language 嵌套化 ===" -ForegroundColor Cyan
foreach ($m in $LanguageRestructure) { Move-LeafBundle -Old $m.old -New $m.new }
foreach ($k in @("language","language/cpp-algorithm","language/cpp-algorithm/basic-cpp","language/cpp-algorithm/other-cpp","language/python","language/python/python-note")) {
    New-SectionIndex -RelDir $k
}

Write-Host ""
Write-Host "=== C. Demo 嵌套化 ===" -ForegroundColor Cyan
foreach ($m in $DemoRestructure) { Move-LeafBundle -Old $m.old -New $m.new }
foreach ($k in @("demo","demo/minecraft")) { New-SectionIndex -RelDir $k }

Write-Host ""
Write-Host "=== D. 清理空目录 ===" -ForegroundColor Cyan
Remove-EmptyDirs -Path (Join-Path $Content "docs")
Remove-EmptyDirs -Path (Join-Path $Content "language")
Remove-EmptyDirs -Path (Join-Path $Content "demo")

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan