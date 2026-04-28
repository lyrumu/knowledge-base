@echo off
title Auto Shutdown at 2AM

for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set /a now_h=%%a
    set /a now_m=%%b
    set /a now_s=%%c
)

set /a now_h=10%now_h% %% 100
set /a now_total=%now_h%*3600 + %now_m%*60 + %now_s%

:: 2AM = 2*3600 = 7200 seconds
if %now_total% lss 7200 (
    set /a wait_seconds=7200 - %now_total%
) else (
    set /a wait_seconds=86400 - %now_total% + 7200
)

echo Current time: %time%
echo Target time: 02:00:00
echo Waiting %wait_seconds% seconds (approx %wait_seconds%/3600 hours)
echo.
echo Waiting... Press Ctrl+C to cancel
echo.

timeout /t %wait_seconds% /nobreak >nul

echo.
echo Time reached! Force closing LM Studio...
taskkill /im "LM Studio.exe" /f 2>nul

echo Waiting 3 seconds before shutdown...
timeout /t 3 /nobreak >nul

echo Shutting down...
shutdown /s /t 0