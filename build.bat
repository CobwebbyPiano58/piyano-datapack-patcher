@echo off
chcp 65001
cd /d "%~dp0"

for /f %%i in ('python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])"') do set VERSION=%%i

python -m PyInstaller ^
  --onefile ^
  --console ^
  --clean ^
  --noconfirm ^
  --name "piyano-datapack-patcher_v%VERSION%" ^
  --icon "icon.ico" ^
  launcher.py

echo.
echo Build complete:
echo dist\piyano-datapack-patcher_v%VERSION%
pause
