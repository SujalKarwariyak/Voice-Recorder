@echo off
setlocal

cls
echo.
echo ============================================================================
echo                   VOICE RECORDER - SETUP AND LAUNCH
echo ============================================================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not available in PATH.
    echo Install Python from https://www.python.org/ and enable Add Python to PATH.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo Found %%i

echo.
echo [2/4] Checking pip installation...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: pip is not installed.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python -m pip --version 2^>^&1') do echo %%i

echo.
echo [3/4] Installing dependencies...
if not exist requirements.txt (
    echo ERROR: requirements.txt was not found.
    echo.
    pause
    exit /b 1
)
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    echo Try: python -m pip install --upgrade pip
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] Checking audio input and launching the application...
python -c "import sounddevice as sd; device = sd.query_devices(kind='input'); print('Audio input device: ' + device['name'])" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: No usable audio input device was found.
    echo Connect or enable a microphone and try again.
    echo.
    pause
    exit /b 1
)

python -m voice_recorder
if errorlevel 1 (
    echo.
    echo ERROR: The application could not start or exited with an error.
    echo Run "python -m voice_recorder" from Command Prompt for details.
    echo.
    pause
    exit /b 1
)

endlocal
exit /b 0
