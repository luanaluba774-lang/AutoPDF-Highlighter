@echo off
REM Gera o executavel Windows (.exe) usando PyInstaller
pip install -r requirements-dev.txt
pyinstaller --onefile --windowed --name AutoPDFHighlighter --add-data "keywords.json;." main.py
echo.
echo Executavel gerado em dist\AutoPDFHighlighter.exe
pause
