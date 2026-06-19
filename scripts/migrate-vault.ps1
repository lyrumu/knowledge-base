$ErrorActionPreference = "Stop"

$Vault     = "f:\Notes\Vault"
$Content   = "f:\Notes\content\notes"
$StaticDir = "f:\Notes\static\notes-assets"

$DocsMap = @(
@{ src = "Docs\宿舍WLAN修复.md";                  dest = "docs/wifi-dorm-fix" }
@{ src = "Docs\Docker\docker-Dify.md";            dest = "docs/docker-dify" }
@{ src = "Docs\Flutter\Flutter-Dart-Trae.md";     dest = "docs/flutter-dart-trae" }
@{ src = "Docs\Git\Git.md";                       dest = "docs/git-basics" }
@{ src = "Docs\Other apps\app_note.md";           dest = "docs/app-notes" }
@{ src = "Docs\VScode\C++刷题环境.md";             dest = "docs/vscode-cpp-env" }
@{ src = "Docs\VScode\Python环境.md";              dest = "docs/vscode-python-env" }
@{ src = "Docs\WSL2\Fix\VMware关机挂起修复.md";     dest = "docs/wsl2-vmware-fix" }
@{ src = "Docs\WSL2\Fix\VMware关机挂起修复2.md";    dest = "docs/wsl2-vmware-fix-2" }
@{ src = "Docs\WSL2\Fix\WinNAT端口冲突修复.md";     dest = "docs/wsl2-winnat-fix" }
@{ src = "Docs\WSL2\Hermes\hermes-agent.md";       dest = "docs/wsl2-hermes-agent" }
@{ src = "Docs\WSL2\Hermes\hermes-api-network-fix.md"; dest = "docs/wsl2-hermes-api" }
@{ src = "Docs\WSL2\Hermes\hermes-dashboard-fix.md";   dest = "docs/wsl2-hermes-dashboard" }
@{ src = "Docs\WSL2\Opencode\mcp-setup-note.md";   dest = "docs/wsl2-opencode-mcp" }
@{ src = "Docs\WSL2\Opencode\opencode-agent.md";   dest = "docs/wsl2-opencode" }
)

$LanguageMap = @(
@{ src = "Language\C++Algorithm\basic C++\C++算法NOTE.md"; dest = "language/cpp-algo-notes"; copyTemplates = "basic C++\template" }
@{ src = "Language\C++Algorithm\basic C++\例题.md";         dest = "language/cpp-examples" }
@{ src = "Language\C++Algorithm\basic C++\图论.md";         dest = "language/cpp-graph" }
@{ src = "Language\C++Algorithm\other C++\C++应用.md";      dest = "language/cpp-applications" }
@{ src = "Language\C++Algorithm\other C++\C++数据结构.md";   dest = "language/cpp-data-structures"; copyPdfs = "other C++" }
@{ src = "Language\Python\Python_Note\Pycharm.md";          dest = "language/python-pycharm" }
)

$DemoMap = @(
@{ src = "Demo&&Resources\Minecraft\datapacks\note\notes.md";       dest = "demo/minecraft-datapacks-notes" }
@{ src = "Demo&&Resources\Minecraft\resourcepacks\FOR MODS\patpat\PatPat-Wiki-中文完整版.md"; dest = "demo/minecraft-patpat-wiki" }
@{ src = "Demo&&Resources\Minecraft\resourcepacks\FOR MODS\patpat\PatPat-资源包制作指南.md";   dest = "demo/minecraft-patpat-guide" }
)

$AipythonSource = "Demo&&Resources\AIpython"
$ToolsSource    = "Tools\Scripts"

function New-Frontmatter {
    param([string]$Title)
    $today = "2026-01-01"
    $lines = @(
        "---",
        "title: `"$Title`"",
        "date: $today",
        "draft: false",
        "description: `"`"",
        "tags: []",
        "categories: []",
        "showHero: true",
        "heroStyle: `"background`"",
        "---",
        ""
    )
    return ($lines -join "`n")
}

function Copy-LeafBundle {
    param(
        [string]$VaultRoot,
        [string]$ContentRoot,
        [string]$RelSrc,
        [string]$RelDest
    )
    $srcPath = Join-Path $VaultRoot $RelSrc
    $destDir = Join-Path $ContentRoot $RelDest
    $destIdx = Join-Path $destDir "index.md"
    if (Test-Path $destIdx) {
        Write-Host "  [SKIP] $RelDest" -ForegroundColor DarkGray
        return
    }
    if (-not (Test-Path $srcPath)) {
        Write-Host "  [MISS] $RelSrc not found" -ForegroundColor Red
        return
    }
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    $content = Get-Content -Path $srcPath -Raw -Encoding UTF8
    $firstLine = ($content -split "`r?`n" | Select-Object -First 30 | Where-Object { $_ -match '^\s*#\s+(.+)' } | Select-Object -First 1)
    $title = ""
    if ($firstLine) {
        $title = (($firstLine -replace '^\s*#\s+','') -replace '<[^>]+>','' -replace '^\s+|\s+$','').Trim()
    }
    if (-not $title) {
        $title = [System.IO.Path]::GetFileNameWithoutExtension($RelSrc)
    }
    $fm = New-Frontmatter -Title $title
    $cleanContent = $content -replace '^---\s*\r?\n[\s\S]*?\r?\n---\s*\r?\n',''
    Set-Content -Path $destIdx -Value ($fm + $cleanContent) -Encoding UTF8
    $srcDir = Split-Path $srcPath -Parent
    $imgDir = Join-Path $srcDir "image"
    if (Test-Path $imgDir) {
        Copy-Item -Path $imgDir -Destination $destDir -Recurse -Force
        Write-Host "  [BUNDLE] $RelDest (+ image/)" -ForegroundColor Green
    } else {
        Write-Host "  [BUNDLE] $RelDest" -ForegroundColor Green
    }
}

function Copy-DirectoryTree {
    param(
        [string]$Src,
        [string]$Dst,
        [string[]]$ExcludeDirs = @('.venv', 'node_modules', '.git', '__pycache__')
    )
    if (-not (Test-Path $Src)) {
        Write-Host "  [MISS] $Src" -ForegroundColor Red
        return
    }
    New-Item -ItemType Directory -Path $Dst -Force | Out-Null
    $excludeArgs = @()
    foreach ($e in $ExcludeDirs) { $excludeArgs += "/XD"; $excludeArgs += $e }
    $robocopyArgs = @($Src, $Dst, "/E", "/NFL", "/NDL", "/NJH", "/NJS", "/NP", "/R:0", "/W:0") + $excludeArgs
    & robocopy @robocopyArgs | Out-Null
    $rc = $LASTEXITCODE
    if ($rc -lt 8) {
        Write-Host "  [COPY] $Src -> $Dst" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] robocopy rc=$rc $Src" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== 1. Docs leaf bundles ===" -ForegroundColor Cyan
foreach ($m in $DocsMap) {
    Copy-LeafBundle -VaultRoot $Vault -ContentRoot $Content -RelSrc $m.src -RelDest $m.dest
}

Write-Host ""
Write-Host "=== 2. Language leaf bundles ===" -ForegroundColor Cyan
foreach ($m in $LanguageMap) {
    Copy-LeafBundle -VaultRoot $Vault -ContentRoot $Content -RelSrc $m.src -RelDest $m.dest
    if ($m.copyTemplates) {
        $tplSrc = Join-Path $Vault $m.copyTemplates
        if (Test-Path $tplSrc) {
            $tplDst = Join-Path (Join-Path $Content $m.dest) "code"
            Copy-DirectoryTree -Src $tplSrc -Dst $tplDst
        }
    }
    if ($m.copyPdfs) {
        $pdfSrc = Join-Path $Vault $m.copyPdfs
        if (Test-Path $pdfSrc) {
            $pdfFiles = @(Get-ChildItem -Path $pdfSrc -Filter "*.pdf" -Recurse)
            foreach ($pdf in $pdfFiles) {
                $rel = $pdf.FullName.Substring($pdfSrc.Length).TrimStart('\','/')
                $dst = Join-Path (Join-Path $Content $m.dest) $rel
                New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null
                Copy-Item -Path $pdf.FullName -Destination $dst -Force
                Write-Host "  [PDF]  $($m.dest)/$rel" -ForegroundColor Green
            }
        }
    }
}

Write-Host ""
Write-Host "=== 3. Demo leaf bundles ===" -ForegroundColor Cyan
foreach ($m in $DemoMap) {
    Copy-LeafBundle -VaultRoot $Vault -ContentRoot $Content -RelSrc $m.src -RelDest $m.dest
}

Write-Host ""
Write-Host "=== 4. Demo/Minecraft binaries -> static ===" -ForegroundColor Cyan
$mcSrc = Join-Path $Vault "Demo&&Resources\Minecraft"
$mcDst = Join-Path $StaticDir "demo/minecraft"
if (Test-Path $mcSrc) {
    New-Item -ItemType Directory -Path $mcDst -Force | Out-Null
    $rcArgs = @($mcSrc, $mcDst, "/E", "/XD", "datapacks\note", "resourcepacks\FOR MODS\patpat", "/NFL", "/NDL", "/NJH", "/NJS", "/NP", "/R:0", "/W:0")
    & robocopy @rcArgs | Out-Null
    Write-Host "  [COPY] Minecraft (note/, patpat/ excluded)" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 5. Demo/AIpython scripts -> static ===" -ForegroundColor Cyan
$aipySrc = Join-Path $Vault $AipythonSource
$aipyDst = Join-Path $StaticDir "demo/aipython"
if (Test-Path $aipySrc) {
    Copy-DirectoryTree -Src $aipySrc -Dst $aipyDst
}

Write-Host ""
Write-Host "=== 6. Tools scripts -> static ===" -ForegroundColor Cyan
$toolsSrc = Join-Path $Vault $ToolsSource
$toolsDst = Join-Path $StaticDir "tools"
if (Test-Path $toolsSrc) {
    Copy-DirectoryTree -Src $toolsSrc -Dst $toolsDst
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan