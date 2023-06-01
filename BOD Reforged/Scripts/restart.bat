@echo off

echo restart blade...
ping /n 3 127.1 >nul

cd /d %~dp0/../../../../bin/bin
start "" Blade.exe %1

exit
