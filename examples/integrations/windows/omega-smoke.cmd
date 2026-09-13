@echo off
setlocal
set "ROOT=%~dp0..\..\.."
python "%ROOT%\bin\omega" doctor
if errorlevel 1 exit /b %errorlevel%
python "%ROOT%\bin\omega" gateway status
endlocal
