# =============================================================================
# fix-images.ps1
# 补回被错误删除的 image/ 目录
# =============================================================================

$ErrorActionPreference = "Stop"
$Vault   = "f:\Notes\Vault"
$Content = "f:\Notes\content\notes"

# mapping: content path → vault image path
$Map = @(
@{ slug = "docs/wifi-dorm-fix";                      vault = "Docs\宿舍WLAN修复.md" }
@{ slug = "docs/docker/docker-dify";                 vault = "Docs\Docker\docker-Dify.md" }
@{ slug = "docs/flutter/flutter-dart-trae";          vault = "Docs\Flutter\Flutter-Dart-Trae.md" }
@{ slug = "docs/git/git-basics";                     vault = "Docs\Git\Git.md" }
@{ slug = "docs/apps/app-notes";                     vault = "Docs\Other apps\app_note.md" }
@{ slug = "docs/vscode/vscode-cpp-env";              vault = "Docs\VScode\C++刷题环境.md" }
@{ slug = "docs/vscode/vscode-python-env";           vault = "Docs\VScode\Python环境.md" }
@{ slug = "docs/wsl2/fix/wsl2-vmware-fix";           vault = "Docs\WSL2\Fix\VMware关机挂起修复.md" }
@{ slug = "docs/wsl2/fix/wsl2-vmware-fix-2";         vault = "Docs\WSL2\Fix\VMware关机挂起修复2.md" }
@{ slug = "docs/wsl2/fix/wsl2-winnat-fix";           vault = "Docs\WSL2\Fix\WinNAT端口冲突修复.md" }
@{ slug = "docs/wsl2/hermes/wsl2-hermes-agent";      vault = "Docs\WSL2\Hermes\hermes-agent.md" }
@{ slug = "docs/wsl2/hermes/wsl2-hermes-api";        vault = "Docs\WSL2\Hermes\hermes-api-network-fix.md" }
@{ slug = "docs/wsl2/hermes/wsl2-hermes-dashboard";  vault = "Docs\WSL2\Hermes\hermes-dashboard-fix.md" }
@{ slug = "docs/wsl2/opencode/wsl2-opencode";        vault = "Docs\WSL2\Opencode\opencode-agent.md" }
@{ slug = "docs/wsl2/opencode/wsl2-opencode-mcp";    vault = "Docs\WSL2\Opencode\mcp-setup-note.md" }
@{ slug = "language/cpp-algorithm/basic-cpp/algo-notes";      vault = "Language\C++Algorithm\basic C++\C++算法NOTE.md" }
@{ slug = "language/cpp-algorithm/basic-cpp/examples";        vault = "Language\C++Algorithm\basic C++\例题.md" }
@{ slug = "language/cpp-algorithm/basic-cpp/graph";           vault = "Language\C++Algorithm\basic C++\图论.md" }
@{ slug = "language/cpp-algorithm/other-cpp/applications";    vault = "Language\C++Algorithm\other C++\C++应用.md" }
@{ slug = "language/cpp-algorithm/other-cpp/data-structures"; vault = "Language\C++Algorithm\other C++\C++数据结构.md" }
@{ slug = "language/python/python-note/pycharm";              vault = "Language\Python\Python_Note\Pycharm.md" }
)

foreach ($m in $Map) {
    $vaultImg = Join-Path (Join-Path $Vault (Split-Path $m.vault -Parent)) "image"
    $dstImg   = Join-Path (Join-Path $Content $m.slug) "image"
    if (-not (Test-Path $vaultImg)) {
        Write-Host "  [NO-IMG] $($m.slug)" -ForegroundColor DarkGray
        continue
    }
    if ((Test-Path $dstImg) -and ((Get-ChildItem $dstImg -Force -Recurse | Measure-Object).Count -gt 0)) {
        Write-Host "  [OK]     $($m.slug)" -ForegroundColor DarkGray
        continue
    }
    Write-Host "  [FIX]    $($m.slug)" -ForegroundColor Yellow
    if (Test-Path $dstImg) { Remove-Item $dstImg -Recurse -Force }
    New-Item -ItemType Directory -Path $dstImg -Force | Out-Null
    & robocopy "$vaultImg" "$dstImg" /E /NFL /NDL /NJH /NJS /NP /R:0 /W:0 | Out-Null
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan