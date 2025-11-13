@echo off
:: Define the base directory where virtual environments are stored
set BASE_DIR=C:\Users\QSS\AppData\Local\Programs\Python\virtual_envs
             
:: Check arguments

if "%~1"=="" (
    echo Please provide an environment name.
    echo Usage: activatevenv [env_name]
    exit /b 1
)

:: Build the full path to the activation script
set ENV_NAME=%~1
set ACTIVATE_PATH=%BASE_DIR%\%ENV_NAME%\Scripts\activate.bat
@REM set ACTIVATE_PATH=%BASE_DIR%\%ENV_NAME%\Scripts\activate.ps1

:: Check if the activate script exists
if exist "%ACTIVATE_PATH%" (
    echo Activating virtual environment: %ENV_NAME%
    echo Interpreter Path: %BASE_DIR%\%ENV_NAME%\Scripts\python.exe
    call "%ACTIVATE_PATH%"
) else (
    echo Virtual environment not found or invalid path: %ACTIVATE_PATH%
)
