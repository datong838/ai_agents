#Requires -Version 5.1
<#
.SYNOPSIS
  Map case .env (NIUSHOP_DB_*) to aos-platform/.env AOS_MYSQL_*.
.NOTES
  Does not print password. Both .env files are gitignored.
  After first write, restart aos-api if it was already running
  (or use qyh_data_access.py body overrides — no restart needed).
#>
$ErrorActionPreference = "Stop"
$CaseRoot = Split-Path -Parent $PSScriptRoot
$CaseEnv = Join-Path $CaseRoot ".env"
$PlatformRoot = (Resolve-Path (Join-Path $CaseRoot "..\..\..\..\aos-platform")).Path
$PlatformEnv = Join-Path $PlatformRoot ".env"

if (-not (Test-Path $CaseEnv)) {
  Write-Error "Missing case .env: $CaseEnv"
}

function Read-DotEnv([string]$Path) {
  $map = @{}
  Get-Content -LiteralPath $Path -Encoding UTF8 | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) { return }
    $i = $line.IndexOf("=")
    $k = $line.Substring(0, $i).Trim()
    $v = $line.Substring($i + 1).Trim().Trim('"').Trim("'")
    $map[$k] = $v
  }
  return $map
}

function Upsert-EnvLine([System.Collections.Generic.List[string]]$Lines, [string]$Key, [string]$Value) {
  $found = $false
  for ($i = 0; $i -lt $Lines.Count; $i++) {
    if ($Lines[$i] -match ("^\s*" + [regex]::Escape($Key) + "\s*=")) {
      $Lines[$i] = "$Key=$Value"
      $found = $true
      break
    }
  }
  if (-not $found) { [void]$Lines.Add("$Key=$Value") }
}

$cfg = Read-DotEnv $CaseEnv
foreach ($req in @("NIUSHOP_DB_HOST", "NIUSHOP_DB_PORT", "NIUSHOP_DB_USER", "NIUSHOP_DB_PASSWORD", "NIUSHOP_DB_NAME")) {
  if (-not $cfg.ContainsKey($req) -or [string]::IsNullOrWhiteSpace($cfg[$req])) {
    Write-Error "Case .env missing $req"
  }
}

$lines = [System.Collections.Generic.List[string]]::new()
if (Test-Path $PlatformEnv) {
  Get-Content -LiteralPath $PlatformEnv -Encoding UTF8 | ForEach-Object { [void]$lines.Add($_) }
} else {
  Write-Host "Creating $PlatformEnv"
}

Upsert-EnvLine $lines "AOS_MYSQL_HOST" $cfg["NIUSHOP_DB_HOST"]
Upsert-EnvLine $lines "AOS_MYSQL_PORT" $cfg["NIUSHOP_DB_PORT"]
Upsert-EnvLine $lines "AOS_MYSQL_USER" $cfg["NIUSHOP_DB_USER"]
Upsert-EnvLine $lines "AOS_MYSQL_PASSWORD" $cfg["NIUSHOP_DB_PASSWORD"]
Upsert-EnvLine $lines "AOS_MYSQL_DATABASE" $cfg["NIUSHOP_DB_NAME"]
# Default table fallback; multi-table uses request body `table` in qyh_data_access.py
Upsert-EnvLine $lines "AOS_MYSQL_TABLE" "ns_order"
Upsert-EnvLine $lines "AOS_MYSQL_DISABLED" "0"
Upsert-EnvLine $lines "AOS_AUTH_ALLOW_DEV" "1"

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllLines($PlatformEnv, $lines.ToArray(), $utf8NoBom)

Write-Host "Wrote AOS_MYSQL_* to $PlatformEnv"
Write-Host ("  host={0} port={1} database={2} user={3} table=ns_order" -f `
  $cfg["NIUSHOP_DB_HOST"], $cfg["NIUSHOP_DB_PORT"], $cfg["NIUSHOP_DB_NAME"], $cfg["NIUSHOP_DB_USER"])
Write-Host "Hint: restart aos-api if already running; or run qyh_data_access.py (body overrides)."
