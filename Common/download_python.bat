@echo off
setlocal

if "%~1"=="" (
    echo Usage: download_python ^<python_version^>
    echo Example: download_python 3.13.7
    exit /b 1
)

set PY_VER=%~1
set PY_FILE=python-%PY_VER%-amd64.exe
set PY_URL=https://www.python.org/ftp/python/%PY_VER%/%PY_FILE%

set TARGET_DIR=%LOCALAPPDATA%\Programs\Python\Python%PY_VER:~0,3%

echo Downloading Python %PY_VER% (64-bit) installer...
echo URL: %PY_URL%

:: Validate download URL exists
powershell -Command ^
  "$r=Invoke-WebRequest '%PY_URL%' -Method Head -ErrorAction SilentlyContinue;" ^
  "if($r.StatusCode -ne 200){Write-Host 'ERROR: Version not found on python.org' -ForegroundColor Red; exit 1}"

:: Download
powershell -Command "Invoke-WebRequest '%PY_URL%' -OutFile '%PY_FILE%'"

if not exist "%PY_FILE%" (
    echo Failed to download installer.
    exit /b 1
)

echo Installing Python to %TARGET_DIR% ...

:: Install for current user (user directory)
"%PY_FILE%" /quiet TargetDir="%TARGET_DIR%" Include_launcher=1 PrependPath=1

echo ✅ Python %PY_VER% installed successfully.
echo 📁 Location: %TARGET_DIR%
echo ℹ️ Run: python --version

pause
