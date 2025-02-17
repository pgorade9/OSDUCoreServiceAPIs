@echo off
REM Navigate to the Python project directory
cd /d "C:\Users\pgorade\PycharmProjects\OSDUCoreServiceAPIs"
if %errorlevel% neq 0 (
    echo Failed to navigate to Python project directory.
    exit /b
)

REM Activate the virtual environment (if applicable)
call .venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate the virtual environment.
    exit /b
)

REM Run the Python script in a new process (daemon mode)
start "" python -m main
if %errorlevel% neq 0 (
    echo Failed to start the Python script in daemon mode.
    exit /b
)

REM Navigate to the Angular UI directory
cd /d "C:\Users\pgorade\PycharmProjects\OSDUCoreServiceAPIs\app\ui-app"
if %errorlevel% neq 0 (
    echo Failed to navigate to UI project directory.
    exit /b
)

REM Serve the Angular app
start "" ng serve --port 4200
if %errorlevel% neq 0 (
    echo Angular app failed to start.
    exit /b
)

@echo off
REM Launch Internet Explorer and open localhost:4200
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" http://localhost:4200

echo All tasks completed successfully!
