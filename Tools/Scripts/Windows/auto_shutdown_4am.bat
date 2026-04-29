@echo off
title 定时关机脚本 - 凌晨4点自动关机

:: 计算距离凌晨4点还有多少秒
for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set /a now_h=%%a
    set /a now_m=%%b
    set /a now_s=%%c
)

:: 处理小时数（去掉前导零，比如08变成8）
set /a now_h=10%now_h% %% 100

:: 计算当前总秒数
set /a now_total=%now_h%*3600 + %now_m%*60 + %now_s%

:: 目标凌晨4点 = 4*3600 = 14400 秒
:: 如果当前时间超过凌晨4点，则顺延到明天凌晨4点
if %now_total% lss 14400 (
    set /a wait_seconds=14400 - %now_total%
) else (
    set /a wait_seconds=86400 - %now_total% + 14400
)

echo 当前时间: %time%
echo 目标时间: 04:00:00
echo 还需等待 %wait_seconds% 秒（约 %wait_seconds%/3600 小时）
echo.
echo 正在等待... 期间可按 Ctrl+C 取消
echo.

:: 等待到凌晨4点
timeout /t %wait_seconds% /nobreak >nul

echo.
echo 时间到！正在强制关闭 LM Studio...
taskkill /im "LM Studio.exe" /f 2>nul

echo 等待3秒后关机...
timeout /t 3 /nobreak >nul

echo 执行关机...
shutdown /s /t 0