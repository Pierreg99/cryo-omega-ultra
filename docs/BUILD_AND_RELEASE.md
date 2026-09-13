# Build & Release Strategy: CryoOmega ULTRA

## 1. Architektur-Analyse (Packaging-Sicht)
Das "CryoOmega ULTRA"-Projekt besteht aktuell vorwiegend aus Python-Code (`bin/omega`, `bin/omega-gateway`, `lib/ultra`) sowie statischen Web-Assets (`ide/`, `browser-extension/`).
Für das Release-Management ergeben sich folgende Artefakt-Ziele:
- **Python Wheel/sdist (`.whl`, `.tar.gz`)**: Das natürlichste und direkteste Packaging-Format. Entwickler können das Tool direkt via `pip install` beziehen.
- **Standalone Binaries (Linux ELF, macOS Mach-O, Windows `.exe`)**: Generiert mittels PyInstaller aus `bin/omega` und `bin/omega-gateway`. Sie beinhalten die Python-Laufzeitumgebung und verpacken die statischen Assets (`ide/`), was sie ideal für User ohne Python-Setup macht.
- **Linux Packages (`.deb`, AppImage)**:
  - *`.deb`*: Bietet tiefe Systemintegration (z.B. in `/opt/cryo-omega-ultra` und `/usr/local/bin`). Basiert auf den vorab gebauten Linux-Binaries und den IDE-Dateien.
  - *AppImage*: Ideal als "Portable App" für jegliche Linux-Distributionen; verpackt die Binaries und IDE in eine ausführbare Datei, ohne Root-Rechte vorauszusetzen.
- **Web/JS Bundles**: Da `ide/` und `browser-extension/` primär statisches HTML/JS beinhalten (ohne Node.js/Webpack-Infrastruktur), reicht ein einfacher Zip/Kopier-Vorgang als Artefakt-Erzeugung aus.
- **Android (APK/AAB) & Java (JAR)**: Aktuell existiert im Repository **kein** nativer Code oder Android-Wrapper. Diese Ziele sind technisch möglich (z.B. über ein neu anzulegendes Capacitor- oder React Native-Projekt, welches ein WebView auf das Gateway schaltet), befinden sich derzeit jedoch lediglich im "Best-Effort-Stub"-Stadium.

**Priorisierung für pragmatischen Release-Prozess:**
1) Python Wheels (geringster Aufwand, höchste native Kompatibilität).
2) Linux (AppImage & deb) und Windows (.exe) (erfordert PyInstaller, liefert hohen Mehrwert für Endanwender).
3) JS-Bundles (aktuell nur ZIPs/Kopien statischer Dateien).
4) Android / JVM (Nur umsetzen, wenn echte Projekte / Wrapper hinzugefügt werden).

---

## 2. Verfügbare CLI-Kommandos

Um die Builds lokal anzustoßen, können die entwickelten Skripte verwendet oder die Kommandos manuell ausgeführt werden. Alle Ergebnisse landen im generierten `/dist`-Ordner.

### Zentrale Skripte
- **Linux / macOS:** `./tools/build_all.sh`
- **Windows:** `.\tools\build_all.cmd`

### Wichtige manuelle Befehle (Auszug)

**Python Packages (Wheel / sdist):**
```bash
python -m build --outdir dist
```

**Windows / Linux Standalone (PyInstaller):**
```bash
# Linux
pyinstaller --noconfirm --onefile --clean --add-data "ide:ide" --distpath dist/bin --name omega bin/omega

# Windows (Semikolon als Pfadtrenner)
pyinstaller --noconfirm --onefile --clean --add-data "ide;ide" --distpath dist\bin --name omega bin\omega
```

**Debian-Paket (via fpm - benötigt installierte fpm-gem):**
```bash
fpm -s dir -t deb -n cryo-omega-ultra -v 0.4.0 --prefix / -C bundle/deb_staging -p dist/cryo-omega-ultra_0.4.0_amd64.deb opt usr
```

**AppImage (benötigt appimagetool):**
```bash
ARCH=x86_64 appimagetool bundle/cryo-omega-ultra.AppDir dist/cryo-omega-ultra-0.4.0-x86_64.AppImage
```

---

## 3. CI/CD Snippets (GitHub Actions)

Hier ist eine beispielhafte Basis-Konfiguration (`.github/workflows/release.yml`), die zeigt, wie das Build-Skript in eine Matrix-Pipeline für Linux und Windows integriert wird.

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Build Dependencies
        run: pip install build pyinstaller

      - name: Build (Linux)
        if: runner.os == 'Linux'
        run: |
          chmod +x tools/build_all.sh
          # Install fpm and appimagetool for deb and AppImage if required
          # sudo gem install fpm
          # wget -O appimagetool https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage && chmod +x appimagetool
          ./tools/build_all.sh

      - name: Build (Windows)
        if: runner.os == 'Windows'
        run: .\tools\build_all.cmd

      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: built-artifacts-${{ runner.os }}
          path: dist/
```

---

## 4. Übersicht für das Projekt-README

*Der folgende Block kann direkt ins `README.md` kopiert werden.*

### 📦 Build & Installation

CryoOmega ULTRA wird auf verschiedenen Wegen bereitgestellt. Alle Builds lassen sich plattformübergreifend im `/dist`-Verzeichnis über unsere zentralen Tools erzeugen:
- **Linux/macOS:** `./tools/build_all.sh`
- **Windows:** `.\tools\build_all.cmd`

#### Verfügbare Artefakte
- **Python (Wheel / sdist):** Native Installation via `pip install dist/cryo_omega_ultra-*.whl`.
- **Standalone Executables (.exe / ELF):** Im Ordner `dist/bin/`. Ideal für den direkten Start ohne Python-Abhängigkeiten. Beinhaltet die Web-IDE.
- **Linux Pakete:**
  - `.deb`: Für Ubuntu/Debian, installiert nach `/opt/cryo-omega-ultra`.
  - `AppImage`: Portable Executable für jegliche Linux-Distributionen.
- **Web IDE & Extension:** ZIP-Archive (`dist/browser-extension.zip`) oder statische Verzeichnisse (`dist/ide-static`) zur Einbindung in Browser oder externe Webserver.
- **Android/JAR:** *In Planung* (Benötigt dedizierte Wrapper-Projekte, aktuell als Stub im Buildscript hinterlegt).
