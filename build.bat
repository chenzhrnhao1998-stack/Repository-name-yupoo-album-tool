@echo off
setlocal
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name YupooAlbumAssistant main.py
echo.
echo Build complete: dist\YupooAlbumAssistant.exe
pause
