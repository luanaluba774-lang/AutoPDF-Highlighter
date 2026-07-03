#!/bin/bash
# Gera o executavel (Linux/Mac) usando PyInstaller
pip install -r requirements-dev.txt
pyinstaller --onefile --windowed --name AutoPDFHighlighter --add-data "keywords.json:." main.py
echo ""
echo "Executavel gerado em dist/AutoPDFHighlighter"
