param (
    [Parameter(Mandatory = $true)]
    [string]$EnvName
)

$BASE_DIR = "C:\Users\QSS\AppData\Local\Programs\Python\virtual_envs"
$ACTIVATE_PATH = Join-Path $BASE_DIR "$EnvName\Scripts\Activate.ps1"
$PYTHON_PATH = Join-Path $BASE_DIR "$EnvName\Scripts\python.exe"

if (Test-Path $ACTIVATE_PATH) {
    Write-Host "Activating virtual environment: $EnvName"
    Write-Host "Interpreter Path: $PYTHON_PATH"
    . $ACTIVATE_PATH  # Note the DOT — this runs the script in current PowerShell session
} else {
    Write-Host "Virtual environment not found or invalid path: $ACTIVATE_PATH"
}
