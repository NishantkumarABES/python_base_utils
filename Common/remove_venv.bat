@echo off
:: Remove an existing Python virtual environment
set BASE_DIR=C:\Users\QSS\AppData\Local\Programs\Python\virtual_envs

if "%~1"=="" (
    echo Please provide an environment name to remove.
    echo Usage: remove_venv [env_name]
    exit /b 1
)

set ENV_NAME=%~1
set TARGET_DIR=%BASE_DIR%\%ENV_NAME%

if not exist "%TARGET_DIR%" (
    echo Virtual environment not found: %TARGET_DIR%
    exit /b 1
)

echo You are about to delete: %ENV_NAME%
echo Full path: %TARGET_DIR%
set /p CONFIRM=Are you sure you want to delete this environment (Y/N)? 

if /I "%CONFIRM%"=="Y" (
    echo Deleting %ENV_NAME%...
    rmdir /s /q "%TARGET_DIR%"
    if exist "%TARGET_DIR%" (
        echo ❌ Failed to delete %ENV_NAME%.
    ) else (
        echo ✅ Successfully deleted %ENV_NAME%.
    )
) else (
    echo Operation cancelled.
)
