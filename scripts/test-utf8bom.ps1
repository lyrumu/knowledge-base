# UTF-8 BOM 测试 — 中文哈希表
$h = @{
"a" = "中文值"
"b" = "Docker"
"c" = "普通"
}
Write-Host $h['a']
Write-Host $h['b']
Write-Host $h['c']