# =============================================================================
# full-rebuild.ps1 — 彻底重建 content/notes/ 结构
# =============================================================================

$ErrorActionPreference = "Stop"
$Vault   = "f:\Notes\Vault"
$Content = "f:\Notes\content\notes"

$Frontmatter = @'
---
date: 2026-01-01
draft: false
description: ""
tags: []
categories: []
showHero: true
heroStyle: "background"
---
'@

function New-LeafBundle {
    param(
        [string]$Slug,         # content/notes/<Slug>
        [string]$VaultSrc,     # Vault 子路径里的 .md
        [string]$VaultImgDir   # Vault image/ 目录（绝对路径），可空
    )

    $destDir = Join-Path $Content $Slug
    $destIdx = Join-Path $destDir "index.md"

    New-Item -ItemType Directory -Path $destDir -Force | Out-Null

    # 1. 写 index.md
    $vaultMd = Join-Path $Vault $VaultSrc
    if (Test-Path $vaultMd) {
        $body = Get-Content -Path $vaultMd -Raw -Encoding UTF8
        # 提取第一个 # 标题作为 title
        $firstH1 = ($body -split "`r?`n" | Select-Object -First 30 | Where-Object { $_ -match '^\s*#\s+(.+)' } | Select-Object -First 1)
        $title = ""
        if ($firstH1) {
            $title = (($firstH1 -replace '^\s*#\s+','') -replace '<[^>]+>','' -replace '^\s+|\s+$','').Trim()
        }
        if (-not $title) { $title = [System.IO.Path]::GetFileNameWithoutExtension($VaultSrc) }

        # 去掉已存在的 frontmatter
        $body = $body -replace '^---\s*\r?\n[\s\S]*?\r?\n---\s*\r?\n',''
        # 拼接新 frontmatter
        $fm = $Frontmatter -replace "title:.*", "title: `"$title`""
        $content = $fm + "`n" + $body
        Set-Content -Path $destIdx -Value $content -Encoding UTF8
    }

    # 2. 复制 image/
    if ($VaultImgDir -and (Test-Path $VaultImgDir)) {
        $imgDest = Join-Path $destDir "image"
        if ((Test-Path $imgDest) -and ((Get-ChildItem $imgDest -Force -Recurse -File | Measure-Object).Count -gt 0)) {
            Write-Host "  [IMG-OK]   $Slug" -ForegroundColor DarkGray
        } else {
            if (Test-Path $imgDest) { Remove-Item $imgDest -Recurse -Force }
            New-Item -ItemType Directory -Path $imgDest -Force | Out-Null
            & robocopy "$VaultImgDir" "$imgDest" /E /NFL /NDL /NJH /NJS /NP /R:0 /W:0 | Out-Null
            Write-Host "  [IMG-FIX]  $Slug" -ForegroundColor Green
        }
    }
}

function New-SectionIndex {
    param(
        [string]$RelDir,
        [string]$Title,
        [string]$Kicker,
        [string]$Subtitle
    )
    $fullPath = Join-Path $Content $RelDir
    New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
    $body = @(
        '---'
        "title: `"$Title`""
        "kicker: `"$Kicker`""
        "subtitle: `"$Subtitle`""
        "description: `"$Title`""
        'layout: "page"'
        'showHero: false'
        'showBreadcrumbs: false'
        'showTableOfContents: false'
        '---'
        ''
    ) -join "`n"
    Set-Content -Path (Join-Path $fullPath "_index.md") -Value $body -Encoding UTF8
    Write-Host "  [INDEX] $RelDir" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 1. Docs leaf bundles (完整重建) ===" -ForegroundColor Cyan

$DocsBundles = @(
@{ slug = "docs/wifi-dorm-fix";                       src = "Docs\宿舍WLAN修复.md" }
@{ slug = "docs/docker/docker-dify";                  src = "Docs\Docker\docker-Dify.md" }
@{ slug = "docs/flutter/flutter-dart-trae";           src = "Docs\Flutter\Flutter-Dart-Trae.md" }
@{ slug = "docs/git/git-basics";                      src = "Docs\Git\Git.md" }
@{ slug = "docs/apps/app-notes";                      src = "Docs\Other apps\app_note.md" }
@{ slug = "docs/vscode/vscode-cpp-env";               src = "Docs\VScode\C++刷题环境.md" }
@{ slug = "docs/vscode/vscode-python-env";            src = "Docs\VScode\Python环境.md" }
@{ slug = "docs/wsl2/fix/wsl2-vmware-fix";            src = "Docs\WSL2\Fix\VMware关机挂起修复.md" }
@{ slug = "docs/wsl2/fix/wsl2-vmware-fix-2";          src = "Docs\WSL2\Fix\VMware关机挂起修复2.md" }
@{ slug = "docs/wsl2/fix/wsl2-winnat-fix";            src = "Docs\WSL2\Fix\WinNAT端口冲突修复.md" }
@{ slug = "docs/wsl2/hermes/wsl2-hermes-agent";       src = "Docs\WSL2\Hermes\hermes-agent.md" }
@{ slug = "docs/wsl2/hermes/wsl2-hermes-api";         src = "Docs\WSL2\Hermes\hermes-api-network-fix.md" }
@{ slug = "docs/wsl2/hermes/wsl2-hermes-dashboard";   src = "Docs\WSL2\Hermes\hermes-dashboard-fix.md" }
@{ slug = "docs/wsl2/opencode/wsl2-opencode";         src = "Docs\WSL2\Opencode\opencode-agent.md" }
@{ slug = "docs/wsl2/opencode/wsl2-opencode-mcp";     src = "Docs\WSL2\Opencode\mcp-setup-note.md" }
)

foreach ($b in $DocsBundles) {
    $vaultImg = Join-Path (Join-Path $Vault (Split-Path $b.src -Parent)) "image"
    New-LeafBundle -Slug $b.slug -VaultSrc $b.src -VaultImgDir $vaultImg
}

Write-Host ""
Write-Host "=== 2. Language leaf bundles (完整重建) ===" -ForegroundColor Cyan

$LangBundles = @(
@{ slug = "language/cpp-algorithm/basic-cpp/algo-notes";      src = "Language\C++Algorithm\basic C++\C++算法NOTE.md" }
@{ slug = "language/cpp-algorithm/basic-cpp/examples";        src = "Language\C++Algorithm\basic C++\例题.md" }
@{ slug = "language/cpp-algorithm/basic-cpp/graph";           src = "Language\C++Algorithm\basic C++\图论.md" }
@{ slug = "language/cpp-algorithm/other-cpp/applications";    src = "Language\C++Algorithm\other C++\C++应用.md" }
@{ slug = "language/cpp-algorithm/other-cpp/data-structures"; src = "Language\C++Algorithm\other C++\C++数据结构.md" }
@{ slug = "language/python/python-note/pycharm";              src = "Language\Python\Python_Note\Pycharm.md" }
)

foreach ($b in $LangBundles) {
    $vaultImg = Join-Path (Join-Path $Vault (Split-Path $b.src -Parent)) "image"
    New-LeafBundle -Slug $b.slug -VaultSrc $b.src -VaultImgDir $vaultImg
}

# 复制 .cpp 模板到 code/ 子目录
$algoNotesDir = Join-Path $Content "language/cpp-algorithm/basic-cpp/algo-notes"
$codeDir      = Join-Path $algoNotesDir "code"
$srcTemplates = Join-Path $Vault "Language\C++Algorithm\basic C++\template"
if (Test-Path $srcTemplates) {
    if (-not (Test-Path $codeDir) -or ((Get-ChildItem $codeDir -Force -Recurse -File | Measure-Object).Count -eq 0)) {
        if (Test-Path $codeDir) { Remove-Item $codeDir -Recurse -Force }
        New-Item -ItemType Directory -Path $codeDir -Force | Out-Null
        & robocopy "$srcTemplates" "$codeDir" /E /NFL /NDL /NJH /NJS /NP /R:0 /W:0 | Out-Null
        Write-Host "  [TPL]   cpp-algo-notes/code" -ForegroundColor Green
    }
}

# 复制 PDF 到 other-cpp/data-structures
$dstDS = Join-Path $Content "language/cpp-algorithm/other-cpp/data-structures"
$srcDS = Join-Path $Vault "Language\C++Algorithm\other C++"
$pdfFiles = @(Get-ChildItem -Path $srcDS -Filter "*.pdf" -Recurse)
foreach ($pdf in $pdfFiles) {
    $rel = $pdf.FullName.Substring($srcDS.Length).TrimStart('\','/')
    $dst = Join-Path $dstDS $rel
    New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null
    Copy-Item -Path $pdf.FullName -Destination $dst -Force
    Write-Host "  [PDF]   $($rel)" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 3. Section landing pages ===" -ForegroundColor Cyan

New-SectionIndex -RelDir "docs"                            -Title "Docs"            -Kicker "DOCS - 文档"       -Subtitle "环境配置 / 工具使用 / 踩坑记录。"
New-SectionIndex -RelDir "docs/docker"                     -Title "Docker"          -Kicker "DOCKER - 容器"     -Subtitle "Docker 折腾记录：WSL2 集成 / 镜像 / 部署。"
New-SectionIndex -RelDir "docs/flutter"                    -Title "Flutter"         -Kicker "FLUTTER - 跨端"    -Subtitle "Flutter + Dart 配置 / 插件 / 实践。"
New-SectionIndex -RelDir "docs/git"                        -Title "Git"             -Kicker "GIT - 版本控制"    -Subtitle "Git 常用命令 / 多账号 / 常见问题。"
New-SectionIndex -RelDir "docs/apps"                       -Title "其他 Apps"       -Kicker "APPS - 其他工具"   -Subtitle "Windows / Ubuntu 下杂七杂八的工具使用笔记。"
New-SectionIndex -RelDir "docs/vscode"                     -Title "VSCode"          -Kicker "VSCODE - 编辑器"   -Subtitle "VSCode 环境配置：C++ 刷题 / Python 开发。"
New-SectionIndex -RelDir "docs/wsl2"                       -Title "WSL2"            -Kicker "WSL2 - Linux 子系统" -Subtitle "WSL2 安装 / 配置 / 周边工具（Hermes / Opencode）。"
New-SectionIndex -RelDir "docs/wsl2/fix"                   -Title "WSL2 · Fix"      -Kicker "WSL2 - 修复"        -Subtitle "WSL2 各种坑的修复记录。"
New-SectionIndex -RelDir "docs/wsl2/hermes"                -Title "WSL2 · Hermes"   -Kicker "WSL2 - Hermes Agent" -Subtitle "Hermes Agent 安装 / API / Dashboard 修复。"
New-SectionIndex -RelDir "docs/wsl2/opencode"              -Title "WSL2 · Opencode" -Kicker "WSL2 - Opencode"     -Subtitle "Opencode Agent / MCP 配置。"
New-SectionIndex -RelDir "language"                        -Title "Language"        -Kicker "LANGUAGE - 语言"   -Subtitle "C++ 算法 / Python 语法 / 代码模板。"
New-SectionIndex -RelDir "language/cpp-algorithm"           -Title "C++ Algorithm"   -Kicker "C++ - 算法"         -Subtitle "C++ 算法笔记 / 模板 / 题解。"
New-SectionIndex -RelDir "language/cpp-algorithm/basic-cpp" -Title "C++ · 基础算法"  -Kicker "C++ - BASIC"         -Subtitle "C++ 基础算法笔记：DP / 图论 / 字符串。"
New-SectionIndex -RelDir "language/cpp-algorithm/other-cpp" -Title "C++ · 其他"      -Kicker "C++ - APPLICATIONS" -Subtitle "C++ 应用 / 数据结构 / 资料。"
New-SectionIndex -RelDir "language/python"                  -Title "Python"          -Kicker "PYTHON"             -Subtitle "Python 语法 / 工具 / 笔记。"
New-SectionIndex -RelDir "language/python/python-note"      -Title "Python · Note"   -Kicker "PYTHON - NOTE"      -Subtitle "Python 开发笔记。"
New-SectionIndex -RelDir "demo"                            -Title "Demo && Resources" -Kicker "DEMO - 示例与资源" -Subtitle "AI 入门 / Minecraft / Agent 实验。"
New-SectionIndex -RelDir "demo/minecraft"                  -Title "Minecraft"       -Kicker "MINECRAFT - 我的世界" -Subtitle "Minecraft 数据包 / 资源包 / 材质 / 音乐 / 皮肤。"

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan