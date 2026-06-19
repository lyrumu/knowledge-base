$files = @(
  "f:\Notes\scripts\full-rebuild.ps1"
)
foreach ($f in $files) {
  if (-not (Test-Path $f)) { continue }
  $content = [System.IO.File]::ReadAllText($f)
  $utf8Bom = New-Object System.Text.UTF8Encoding($true)
  [System.IO.File]::WriteAllText($f, $content, $utf8Bom)
  Write-Host "BOM added: $f"
}