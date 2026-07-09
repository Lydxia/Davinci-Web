# Wrapper: runs the project's Python build with the D:-installed toolchain.
# Usage: powershell -File build.ps1   (paths derived from env to avoid non-ASCII issues)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$work = "D:\temporary use for claude\davinci\.tooling"
$env:PYTHONPATH = "$work\pylibs"
$env:TEMP = "$work\tmp"; $env:TMP = "$work\tmp"
$py = Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"
Push-Location $root
try { & $py build.py } finally { Pop-Location }
