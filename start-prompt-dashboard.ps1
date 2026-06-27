$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Port = 8765
$Url = "http://127.0.0.1:$Port"

function Test-PortOpen {
  param([int]$Port)
  try {
    $client = New-Object Net.Sockets.TcpClient
    $async = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
    $success = $async.AsyncWaitHandle.WaitOne(300)
    if ($success) {
      $client.EndConnect($async)
      $client.Close()
      return $true
    }
    $client.Close()
    return $false
  } catch {
    return $false
  }
}

function Find-Python {
  $candidates = @(
    (Join-Path $Root ".venv\Scripts\python.exe"),
    "D:\hermes\hermes-agent\venv\Scripts\python.exe",
    "C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
  )
  foreach ($candidate in $candidates) {
    if (Test-Path $candidate) { return $candidate }
  }
  $cmd = Get-Command python -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }
  throw "Python not found."
}

if (-not (Test-PortOpen -Port $Port)) {
  $Python = Find-Python
  $Server = Join-Path $Root "prompt-dashboard\server.py"
  Start-Process -FilePath $Python -ArgumentList @($Server, "--port", "$Port") -WorkingDirectory $Root -WindowStyle Hidden
  Start-Sleep -Milliseconds 900
}

Start-Process $Url
