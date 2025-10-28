@echo off
REM Simple Compilation Performance Test for WHILE Compiler
echo ========================================
echo WHILE Compiler Performance Test
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "compiler.py" (
    echo Error: compiler.py not found
    pause
    exit /b 1
)

if not exist "examples\good_syntax\example6-collatz.while" (
    echo Error: example6-collatz.while not found
    pause
    exit /b 1
)

if not exist "examples\good_syntax\example13-fibonacci.while" (
    echo Error: example13-fibonacci.while not found
    pause
    exit /b 1
)

echo Running compilation performance test...
echo.

REM Run the compilation test
python compilation_test.py

if errorlevel 1 (
    echo.
    echo Performance test failed!
    pause
    exit /b 1
)

echo.
echo Performance test completed successfully!
echo Check performance_tests directory for results.
echo.
pause