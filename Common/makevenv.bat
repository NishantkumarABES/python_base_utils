@echo off
:: Define base directory where all virtual environments are stored
set BASE_DIR=C:\Users\QSS\AppData\Local\Programs\Python\virtual_envs

:: Check if enough arguments were provided


if "%~1"=="" (
    echo Please provide a virtual environment name.
    echo Usage: makevenv [env_name] [version]
    exit /b 1
)

if "%~2"=="" (
    echo Please provide a Python version.
    echo Usage: makevenv [env_name] [version]
    exit /b 1
)

:: Extract arguments
set ENV_NAME=%~1
set VERSION_PATH=C:\Users\QSS\AppData\Local\Programs\Python\Python%~2\python.exe
                
:: Build the full path
set VENV_PATH=%BASE_DIR%\%ENV_NAME%

if exist "%VENV_PATH%" (
    echo The virtual environment %VENV_PATH% already exists.
    exit /b 1
)


:: Create the virtual environment
"%VERSION_PATH%" -m venv "%VENV_PATH%"

echo Virtual environment created at %VENV_PATH%
