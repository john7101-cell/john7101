#!/usr/bin/env bash
# Instala lo necesario para la editorial de ebooks (Linux Debian/Ubuntu; en macOS ver la nota al final).
#   bash scripts/instalar_ebooks.sh
set -euo pipefail
SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"

echo "→ Paquetes del sistema: Pandoc, Hunspell (español), Java (EPUBCheck), poppler (vista previa), fuentes"
$SUDO apt-get update -q
$SUDO apt-get install -y -q pandoc hunspell hunspell-es default-jre-headless poppler-utils \
  fonts-ebgaramond fonts-ebgaramond-extra fonts-lato fonts-linuxlibertine

echo "→ Paquetes de Python: Typst (PDF), Pillow (portadas), PyYAML, MarkItDown (leer .docx/.pdf)"
pip install -q -e ".[ebooks]"

echo "→ EPUBCheck 5.1.0 (validador oficial W3C de EPUB)"
if ! command -v epubcheck >/dev/null; then
  DEST=/opt/epubcheck; TMP=$(mktemp -d)
  curl -sSfL -o "$TMP/epubcheck.zip" https://github.com/w3c/epubcheck/releases/download/v5.1.0/epubcheck-5.1.0.zip
  $SUDO mkdir -p "$DEST" && $SUDO python3 -m zipfile -e "$TMP/epubcheck.zip" "$DEST" && rm -rf "$TMP"
  printf '#!/bin/sh\nexec java -jar %s/epubcheck-5.1.0/epubcheck.jar "$@"\n' "$DEST" | $SUDO tee /usr/local/bin/epubcheck >/dev/null
  $SUDO chmod +x /usr/local/bin/epubcheck
fi

echo "→ Comprobación"
pandoc --version | head -1
python3 -c "import typst, PIL, yaml; print('typst, Pillow y PyYAML OK')"
echo "hola" | hunspell -d es_ES -l >/dev/null && echo "Hunspell es_ES OK"
epubcheck --version 2>/dev/null | grep -i epubcheck | head -1 || true
fc-list | grep -qi "EB Garamond" && echo "Fuente EB Garamond OK"
echo "✔ Listo. Prueba: python -m ugc_agency ebook-maquetar examples/manuscrito_muestra.md --out output/prueba"

# macOS (Homebrew):
#   brew install pandoc hunspell openjdk poppler epubcheck && brew install --cask font-eb-garamond font-lato
#   pip install -e ".[ebooks]"   # diccionario: descarga es_ES.dic/.aff a ~/Library/Spelling
