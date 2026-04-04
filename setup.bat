@echo off
echo ====================================
echo   SeniorShield - First Time Setup
echo ====================================
echo.

echo Installing Python requirements...
python -m pip install psutil Pillow twilio

echo.
echo Done! Now run:
echo   python senior_shield.py
echo.
pause
