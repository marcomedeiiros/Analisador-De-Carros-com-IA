@echo off
echo ========================================
echo Instalando OpenCV (cv2)
echo ========================================
echo.

python -m pip install opencv-python

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo Instalacao concluida com sucesso!
    echo Execute: python scripts/run_api.py
) else (
    echo Erro na instalacao. Tente:
    echo   pip install opencv-python-headless
)
echo ========================================
pause
