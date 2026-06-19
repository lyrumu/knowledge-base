$IndexDefsMap = @{
"docs" = "Docs|DOCS - 文档|环境配置 / 工具使用 / 踩坑记录。"
"docs|docker" = "Docker|DOCKER - 容器|Docker 折腾记录：WSL2 集成 / 镜像 / 部署。"
}

$raw = $IndexDefsMap["docs"]
Write-Host "raw=[$raw]"
$parts = $raw -split '\|', 3
Write-Host "parts count: $($parts.Count)"
Write-Host "T=[$($parts[0])]"
Write-Host "K=[$($parts[1])]"
Write-Host "S=[$($parts[2])]"