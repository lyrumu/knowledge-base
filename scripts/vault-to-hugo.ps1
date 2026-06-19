# vault-to-hugo.ps1
# =============================================================================
# 把 /Vault 里的 ".md + image/" 同步为 Hugo leaf bundle
# 用法：
#   powershell -File scripts/vault-to-hugo.ps1           # 全量同步
#   powershell -File scripts/vault-to-hugo.ps1 -Watch    # 持续监听（配合 hugo server）
#
# 幂等：只更新 source 更新的 bundle，已存在且未变的跳过
# 速度：全量扫描 < 1 秒（没有 robocopy 开销）
# =============================================================================

param([switch]$Watch)

$Vault   = "f:\Notes\Vault"
$Content = "f:\Notes\content\notes"
$Static  = "f:\Notes\static\notes-assets"

# ============================================================
# 映射表 — 告诉脚本 Vault 的什么文件 → content 的哪个位置
# 想加新文章，就在这里加一行
# ============================================================
$DocsMap = @(
@{ src = "Docs\宿舍WLAN修复.md";                  bundle = "docs/wifi-dorm-fix" }
@{ src = "Docs\Docker\docker-Dify.md";            bundle = "docs/docker/docker-dify" }
@{ src = "Docs\Flutter\Flutter-Dart-Trae.md";     bundle = "docs/flutter/flutter-dart-trae" }
@{ src = "Docs\Git\Git.md";                       bundle = "docs/git/git-basics" }
@{ src = "Docs\Other apps\app_note.md";           bundle = "docs/apps/app-notes" }
@{ src = "Docs\VScode\C++刷题环境.md";             bundle = "docs/vscode/vscode-cpp-env" }
@{ src = "Docs\VScode\Python环境.md";              bundle = "docs/vscode/vscode-python-env" }
@{ src = "Docs\WSL2\Fix\VMware关机挂起修复.md";     bundle = "docs/wsl2/fix/wsl2-vmware-fix" }
@{ src = "Docs\WSL2\Fix\VMware关机挂起修复2.md";    bundle = "docs/wsl2/fix/wsl2-vmware-fix-2" }
@{ src = "Docs\WSL2\Fix\WinNAT端口冲突修复.md";     bundle = "docs/wsl2/fix/wsl2-winnat-fix" }
@{ src = "Docs\WSL2\Hermes\hermes-agent.md";       bundle = "docs/wsl2/hermes/wsl2-hermes-agent" }
@{ src = "Docs\WSL2\Hermes\hermes-api-network-fix.md"; bundle = "docs/wsl2/hermes/wsl2-hermes-api" }
@{ src = "Docs\WSL2\Hermes\hermes-dashboard-fix.md";   bundle = "docs/wsl2/hermes/wsl2-hermes-dashboard" }
@{ src = "Docs\WSL2\Opencode\mcp-setup-note.md";   bundle = "docs/wsl2/opencode/wsl2-opencode-mcp" }
@{ src = "Docs\WSL2\Opencode\opencode-agent.md";   bundle = "docs/wsl2/opencode/wsl2-opencode" }
)

$LangMap = @(
@{ src = "Language\C++Algorithm\basic C++\C++算法NOTE.md";   bundle = "language/cpp-algorithm/basic-cpp/algo-notes";  copyTemplates = $true }
@{ src = "Language\C++Algorithm\basic C++\例题.md";           bundle = "language/cpp-algorithm/basic-cpp/examples" }
@{ src = "Language\C++Algorithm\basic C++\图论.md";           bundle = "language/cpp-algorithm/basic-cpp/graph" }
@{ src = "Language\C++Algorithm\other C++\C++应用.md";        bundle = "language/cpp-algorithm/other-cpp/applications" }
@{ src = "Language\C++Algorithm\other C++\C++数据结构.md";     bundle = "language/cpp-algorithm/other-cpp/data-structures"; copyPdfs = $true }
@{ src = "Language\Python\Python_Note\Pycharm.md";            bundle = "language/python/python-note/pycharm" }
)

$DemoMap = @(
@{ src = "Demo&&Resources\Minecraft\datapacks\note\notes.md";       bundle = "demo/minecraft/datapacks-notes" }
@{ src = "Demo&&Resources\Minecraft\resourcepacks\FOR MODS\patpat\PatPat-Wiki-中文完整版.md"; bundle = "demo/minecraft/patpat-wiki" }
@{ src = "Demo&&Resources\Minecraft\resourcepacks\FOR MODS\patpat\PatPat-资源包制作指南.md";   bundle = "demo/minecraft/patpat-guide" }
)

# ============================================================
# 核心函数：只更新 source 更新的 bundle
# ============================================================
function Sync-Bundle {
    param([string]$VaultSrc, [string]$BundlePath)
    $srcFile = Join-Path $Vault $VaultSrc
    $dstDir  = Join-Path $Content $BundlePath
    $dstIdx  = Join-Path $dstDir "index.md"

    if (-not (Test-Path $srcFile)) { return }  # source 文件不存在，跳过

    # 是否需要更新：dst 不存在 或 源文件比 dst 新
    $needUpdate = (-not (Test-Path $dstIdx)) -or ((Get-Item $srcFile).LastWriteTime -gt (Get-Item $dstIdx).LastWriteTime)
    if (-not $needUpdate) { return }

    New-Item -ItemType Directory -Path $dstDir -Force | Out-Null

    # 提取 title（第一个 # 标题）
    $body = Get-Content -Path $srcFile -Raw -Encoding UTF8
    $first = ($body -split "`r?`n" | Select-Object -First 20 | Where-Object { $_ -match '^\s*#\s+(.+)' } | Select-Object -First 1)
    $title = ""
    if ($first) { $title = (($first -replace '^\s*#\s+','') -replace '<[^>]+>','' -replace '^\s+|\s+$','').Trim() }
    if (-not $title) { $title = [System.IO.Path]::GetFileNameWithoutExtension($BundlePath) }

    # 去掉原有 frontmatter（如果有）
    $body = $body -replace '^---\s*\r?\n[\s\S]*?\r?\n---\s*\r?\n',''
    # 写新 index.md（不盖 frontmatter，让 Hugo 自动从当前模板继承）
    Set-Content -Path $dstIdx -Value $body -Encoding UTF8

    # 复制 image/（如果存在）
    $srcDir  = Split-Path $srcFile -Parent
    $imgDir  = Join-Path $srcDir "image"
    $dstImg  = Join-Path $dstDir "image"
    if (Test-Path $imgDir) {
        New-Item -ItemType Directory -Path $dstImg -Force | Out-Null
        & robocopy "$imgDir" "$dstImg" /E /NFL /NDL /NJH /NJS /NP /R:0 /W:0 | Out-Null
    }
}

# ============================================================
# 同步所有映射
# ============================================================
function Sync-All {
    Write-Host "Syncing..." -NoNewline
    foreach ($m in ($DocsMap + $LangMap + $DemoMap)) {
        Sync-Bundle -VaultSrc $m.src -BundlePath $m.bundle
    }
    Write-Host " done" -ForegroundColor Green
}

# ============================================================
# -Watch 模式：每 5 秒扫一次（保留老方法，实测优于 FileSystemWatcher）
# ============================================================
if ($Watch) {
    Write-Host "Watching Vault for changes... (Ctrl+C to stop)" -ForegroundColor Cyan
    Sync-All
    while ($true) {
        Start-Sleep -Seconds 5
        Sync-All
    }
} else {
    Sync-All
}