#!/usr/bin/env bash
# tools/build_all.sh
# Build script for CryoOmega ULTRA (Linux / macOS)

set -e

# Globals
DIST_DIR="$(pwd)/dist"
BUNDLE_DIR="$(pwd)/bundle"
APP_NAME="cryo-omega-ultra"
APP_VERSION="0.4.0" # Should match pyproject.toml

# Clean previous builds
echo "[*] Cleaning previous builds..."
rm -rf "${DIST_DIR}" "${BUNDLE_DIR}" build/
mkdir -p "${DIST_DIR}" "${BUNDLE_DIR}"

build_python() {
    echo "[*] Building Python Wheel and sdist..."
    # Ensure build is installed: pip install build
    python3 -m build --outdir "${DIST_DIR}"
    echo "[+] Python build complete."
}

build_exe() {
    echo "[*] Building Standalone Executables (Host OS)..."
    # Builds native executable (ELF on Linux, Mach-O on macOS)
    # Using PyInstaller
    # Include IDE static files so the executable can serve them

    # Check if pyinstaller is available
    if command -v pyinstaller >/dev/null 2>&1; then
        pyinstaller --noconfirm --onefile --clean \
            --add-data "ide:ide" \
            --distpath "${DIST_DIR}/bin" \
            --name omega \
            bin/omega

        pyinstaller --noconfirm --onefile --clean \
            --add-data "ide:ide" \
            --distpath "${DIST_DIR}/bin" \
            --name omega-gateway \
            bin/omega-gateway

        echo "[+] Executables built in ${DIST_DIR}/bin"
    else
        echo "[-] pyinstaller not found, skipping standalone executable build."
    fi
}

build_deb() {
    echo "[*] Building .deb package..."
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        echo "[-] Skipping .deb build on non-Linux OS."
        return
    fi

    # We will use fpm if available, otherwise just print commands
    if command -v fpm >/dev/null 2>&1; then
        # Create staging directory
        STAGING_DIR="${BUNDLE_DIR}/deb_staging"
        mkdir -p "${STAGING_DIR}/opt/${APP_NAME}/bin"
        mkdir -p "${STAGING_DIR}/opt/${APP_NAME}/ide"
        mkdir -p "${STAGING_DIR}/usr/local/bin"

        # Copy binaries if they exist
        if [ -f "${DIST_DIR}/bin/omega" ]; then
            cp "${DIST_DIR}/bin/omega" "${STAGING_DIR}/opt/${APP_NAME}/bin/"
            ln -s "/opt/${APP_NAME}/bin/omega" "${STAGING_DIR}/usr/local/bin/omega"
        else
            echo "[-] omega binary not found. Run build_exe first."
        fi

        if [ -f "${DIST_DIR}/bin/omega-gateway" ]; then
            cp "${DIST_DIR}/bin/omega-gateway" "${STAGING_DIR}/opt/${APP_NAME}/bin/"
            ln -s "/opt/${APP_NAME}/bin/omega-gateway" "${STAGING_DIR}/usr/local/bin/omega-gateway"
        fi

        # Copy IDE
        cp -r ide/* "${STAGING_DIR}/opt/${APP_NAME}/ide/"

        fpm -s dir -t deb \
            -n "${APP_NAME}" \
            -v "${APP_VERSION}" \
            --prefix / \
            -C "${STAGING_DIR}" \
            -p "${DIST_DIR}/${APP_NAME}_${APP_VERSION}_amd64.deb" \
            opt usr

        echo "[+] .deb package built."
    else
        echo "[-] fpm not found. To build .deb, please install fpm (gem install fpm)."
    fi
}

build_appimage() {
    echo "[*] Building AppImage..."
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        echo "[-] Skipping AppImage on non-Linux OS."
        return
    fi

    if command -v appimagetool >/dev/null 2>&1 || [ -f "./appimagetool-x86_64.AppImage" ]; then
        APPDIR="${BUNDLE_DIR}/${APP_NAME}.AppDir"
        mkdir -p "${APPDIR}/usr/bin"
        mkdir -p "${APPDIR}/usr/share/ide"

        # Copy binaries and IDE
        if [ -f "${DIST_DIR}/bin/omega" ]; then
            cp "${DIST_DIR}/bin/omega" "${APPDIR}/usr/bin/"
        fi
        if [ -f "${DIST_DIR}/bin/omega-gateway" ]; then
            cp "${DIST_DIR}/bin/omega-gateway" "${APPDIR}/usr/bin/"
        fi
        cp -r ide/* "${APPDIR}/usr/share/ide/"

        # Create AppRun
        cat << 'EOF' > "${APPDIR}/AppRun"
#!/bin/sh
HERE="$(dirname "$(readlink -f "${0}")")"
export IDE_PATH="${HERE}/usr/share/ide"
exec "${HERE}/usr/bin/omega" "$@"
EOF
        chmod +x "${APPDIR}/AppRun"

        # Create desktop file
        cat << EOF > "${APPDIR}/${APP_NAME}.desktop"
[Desktop Entry]
Name=CryoOmega ULTRA
Exec=omega
Icon=omega
Type=Application
Categories=Development;
EOF

        # Create icon
        cp ide/mark.svg "${APPDIR}/omega.svg"

        # Build AppImage
        APPIMAGE_TOOL="appimagetool"
        if [ -f "./appimagetool-x86_64.AppImage" ]; then
            APPIMAGE_TOOL="./appimagetool-x86_64.AppImage"
        fi

        ARCH=x86_64 $APPIMAGE_TOOL "${APPDIR}" "${DIST_DIR}/${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
        echo "[+] AppImage built."
    else
        echo "[-] appimagetool not found. Skipping AppImage build."
    fi
}

build_js() {
    echo "[*] Building JS/TSX Bundles (Web IDE & Browser Extension)..."
    # Stub / best-effort script since no package.json exists natively yet

    # 1. Package browser extension as a zip for distribution
    echo "  - Packaging browser-extension..."
    cd browser-extension
    zip -r "${DIST_DIR}/browser-extension.zip" . -x "*.git*" -x "*node_modules*" > /dev/null
    cd ..

    # 2. Stub for JS bundle (e.g. if we had a bundler like esbuild or Webpack)
    # if [ -f "ide/package.json" ]; then
    #     echo "  - Building IDE via npm..."
    #     cd ide && npm install && npm run build && cd ..
    #     cp -r ide/dist "${DIST_DIR}/ide-bundle"
    # else
    echo "  - No JS bundler config found, copying static IDE files..."
    cp -r ide "${DIST_DIR}/ide-static"
    # fi
    echo "[+] JS Build steps complete."
}

build_android() {
    echo "[*] Building Android APK/AAB (Stub)..."
    echo "  - Note: Android build requires a separate WebView/Capacitor/React Native wrapper project."
    echo "  - To build an APK/AAB, you would typically run:"
    echo "    cd android-wrapper && ./gradlew assembleRelease bundleRelease"
    echo "  - Copying stub outputs..."
    mkdir -p "${DIST_DIR}/android"
    echo "APK and AAB will be placed here once the wrapper project is configured." > "${DIST_DIR}/android/README.txt"
    echo "[+] Android stub complete."
}

build_java() {
    echo "[*] Building Java/JVM JAR (Stub)..."
    echo "  - Note: JAR packaging makes sense if a JVM-based client/wrapper is added."
    echo "  - Currently not applicable to the Python CLI codebase."
}

main() {
    echo "=== Starting Build for CryoOmega ULTRA ==="
    build_python
    build_exe
    build_deb
    build_appimage
    build_js
    build_android
    build_java
    echo "=== All builds complete. Check the ${DIST_DIR} directory. ==="
}

main
