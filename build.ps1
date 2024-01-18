$scriptpath = $MyInvocation.MyCommand.Path
$dir = Split-Path $scriptpath
cd $dir

pyinstaller.exe --onefile  .\ramTracker.py