$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$src = Join-Path $root "codex-skills\content-strategy-room"
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
$dest = Join-Path $codexHome "skills\content-strategy-room"

if (-not (Test-Path -LiteralPath $src)) {
  throw "Missing skill source: $src"
}

New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item -Path (Join-Path $src "*") -Destination $dest -Recurse -Force

Write-Output "Installed content-strategy-room to $dest"
Write-Output "Restart Codex or open a new thread if the skill is not detected immediately."
