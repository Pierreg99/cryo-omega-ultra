@echo off
REM tools\build_all.cmd
REM Build script for CryoOmega ULTRA (Windows)

setlocal
set DIST_DIR=%CD%\dist
set BUNDLE_DIR=%CD%\bundle
set APP_NAME=cryo-omega-ultra
set APP_VERSION=0.4.0

echo === Starting Build for CryoOmega ULTRA (Windows) ===

echo [*] Cleaning previous builds...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%BUNDLE_DIR%" rmdir /s /q "%BUNDLE_DIR%"
if exist "build" rmdir /s /q "build"
mkdir "%DIST_DIR%"
mkdir "%BUNDLE_DIR%"

:build_python
echo [*] Building Python Wheel and sdist...
python -m build --outdir "%DIST_DIR%"
echo [+] Python build complete.

:build_exe
echo [*] Building Standalone Executables (Windows)...
REM Requires pyinstaller: pip install pyinstaller
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [-] pyinstaller not found, skipping executable build.
    goto build_js
)

echo   - Building omega.exe...
pyinstaller --noconfirm --onefile --clean ^
    --add-data "ide;ide" ^
    --distpath "%DIST_DIR%\bin" ^
    --name omega ^
    bin\omega

echo   - Building omega-gateway.exe...
pyinstaller --noconfirm --onefile --clean ^
    --add-data "ide;ide" ^
    --distpath "%DIST_DIR%\bin" ^
    --name omega-gateway ^
    bin\omega-gateway

echo [+] Executables built in %DIST_DIR%\bin

:build_js
echo [*] Building JS/TSX Bundles (Web IDE ^& Browser Extension)...
REM Package browser extension as a zip
echo   - Packaging browser-extension...
powershell -Command "Compress-Archive -Path 'browser-extension\*' -DestinationPath '%DIST_DIR%\browser-extension.zip' -Force"

REM Stub for JS bundle
echo   - No JS bundler config found, copying static IDE files...
xcopy /E /I /Y "ide" "%DIST_DIR%\ide-static"
echo [+] JS Build steps complete.

:build_android
echo [*] Building Android APK/AAB (Stub)...
echo   - Note: Android build requires a separate WebView wrapper project.
mkdir "%DIST_DIR%\android"
echo APK and AAB will be placed here once the wrapper project is configured. > "%DIST_DIR%\android\README.txt"

echo === All builds complete. Check the %DIST_DIR% directory. ===
endlocal
exit /b 0
