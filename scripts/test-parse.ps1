$lines = Get-Content -Path 'f:\Notes\scripts\migrate-vault.ps1'
Write-Host "Total: $($lines.Count)"
for ($i = 175; $i -lt 215; $i++) {
  if ($i -lt $lines.Count) {
    Write-Host ("{0,4}: [{1}]" -f ($i + 1), $lines[$i])
  }
}