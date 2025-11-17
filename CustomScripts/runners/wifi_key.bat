@echo off
setlocal

:: If a network name is passed as argument:
if not "%~1"=="" (
    echo Showing key for Wi-Fi profile: %~1
    netsh wlan show profile name="%~1" key=clear
    goto :eof
)

:: No argument provided → list all profiles
echo No network name provided.
echo.
echo Available Wi-Fi profiles:
echo -------------------------------------
netsh wlan show profiles
echo.
echo Usage:
echo   wifi_key.bat "<WiFi-Name>"
echo.
echo Example:
echo   wifi_key.bat "MyHomeWiFi"

endlocal
