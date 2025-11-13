@echo off
:: List all existing Python virtual environments
set BASE_DIR=C:\Users\QSS\AppData\Local\Programs\Python\virtual_envs

if not exist "%BASE_DIR%" (
    echo The base directory does not exist: %BASE_DIR%
    exit /b 1
)

echo ===============================================
echo   Existing Python Virtual Environments
echo ===============================================

pushd "%BASE_DIR%"
for /d %%D in (*) do (
    if exist "%%D\Scripts\activate.bat" (
        echo - %%D
    )
)
popd

echo ===============================================
echo Total environments found: 
dir "%BASE_DIR%" /ad /b | find /c /v ""
