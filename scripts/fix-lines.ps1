$path = 'f:\Notes\scripts\migrate-vault.ps1'
$content = Get-Content -Path $path -Raw -Encoding UTF8

# 修复被合并的两行
$bad = "  # 复制 PDF 资料（other C++/）`r`n  if (`$m.copyPdfs) {"
$good = "  # 复制 PDF 资料（other C++/）`r`n  if (`$m.copyPdfs) {"

# 实际上需要找的是被错误合并的行
$bad2 = "  # 复制 PDF 资料（other C++/）  if (`$m.copyPdfs) {"
$good2 = "  # 复制 PDF 资料（other C++/）`r`n  if (`$m.copyPdfs) {"

$content = $content -replace $bad2, $good2

Set-Content -Path $path -Value $content -Encoding UTF8 -NoNewline
Write-Host "OK"