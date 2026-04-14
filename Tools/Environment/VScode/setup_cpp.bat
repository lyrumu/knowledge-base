@echo off
chcp 65001 >nul
title 配置C++文件关联
echo ========================================
echo     配置 C++ 文件关联到 Dev-C++
echo     图标恢复为白纸样式
echo ========================================
echo.

:: 检查是否以管理员运行
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 请以管理员身份运行此脚本！
    echo 右键脚本 -> 以管理员身份运行
    pause
    exit /b 1
)

:: ========== 你的确切路径 ==========
set DEVPATH="F:\dev-c++\devcpp.exe"
set VSPATH="F:\VSCode\MicrosoftVSCode\Code.exe"
:: =================================

echo 检查路径是否存在...
if not exist %DEVPATH% (
    echo 错误：找不到 devcpp.exe
    echo 请确认路径：F:\dev-c++\devcpp.exe
    pause
    exit /b 1
)

if not exist %VSPATH% (
    echo 警告：找不到 VS Code
    echo 右键菜单的 VS Code 选项将不会添加
    set VSPATH=""
)

:: 处理的文件扩展名
set EXTENSIONS=.c .cpp .cc .cxx .h .hpp .hxx .inl

echo 正在配置文件关联...
echo.

for %%e in (%EXTENSIONS%) do (
    echo 处理 %%e 文件...
    
    :: 设置文件类型
    reg add "HKEY_CLASSES_ROOT\%%e" /ve /t REG_SZ /d "cppfile" /f
    
    :: 白纸图标
    reg add "HKEY_CLASSES_ROOT\cppfile\DefaultIcon" /ve /t REG_SZ /d "shell32.dll,0" /f
    
    :: 双击用 Dev-C++ 打开
    reg add "HKEY_CLASSES_ROOT\cppfile\shell\open\command" /ve /t REG_SZ /d "%DEVPATH% \"%%1\"" /f
    
    :: 右键菜单：用 VS Code 打开
    if not "%VSPATH%"=="" (
        reg add "HKEY_CLASSES_ROOT\cppfile\shell\vscode" /ve /t REG_SZ /d "用 VS Code 打开" /f
        reg add "HKEY_CLASSES_ROOT\cppfile\shell\vscode\command" /ve /t REG_SZ /d "%VSPATH% \"%%1\"" /f
    )
)

echo.
echo 正在刷新图标缓存...
taskkill /f /im explorer.exe >nul 2>&1
timeout /t 2 /nobreak >nul
start explorer.exe

echo.
echo ========================================
echo     配置完成！
echo ========================================
echo.
echo 效果：
echo 1. .cpp 文件图标 -> 白纸 ✓
echo 2. 双击 -> 用 Dev-C++ 打开 ✓
echo 3. 右键 -> 有"用 VS Code 打开" ✓
echo 4. 拖拽到 VS Code 图标 -> 也能打开 ✓
echo.
pause