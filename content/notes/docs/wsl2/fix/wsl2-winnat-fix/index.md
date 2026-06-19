---
date: 2026-01-01
draft: false
description: ""
tags: []
categories: []
showHero: true
heroStyle: "background"
---
# WinNAT 端口冲突修复

## 环境

| 项目 | 值 |
|------|-----|
| 操作系统 | Windows 11 (Hyper-V / WSL2) |
| WSL | wsl2, appendWindowsPath=false |
| 常用服务 | LM Studio (端口 1234)、Hermes (端口 8888)、Trae |

## 问题
服务报 `EACCES: permission denied 0.0.0.0:PORT`，端口被 WinNAT（Hyper-V NAT）随机保留占用。

## 排查

```powershell
# 1. 查进程占用
netstat -ano | findstr :PORT

# 2. 查 WinNAT 保留范围
netsh interface ipv4 show excludedportrange protocol=tcp
```

端口出现在排除范围中 → WinNAT 随机保留。

## 修复

⚠️ **必须按顺序，先停 WSL 再动 WinNAT**

```powershell
# 管理员 PowerShell
wsl --shutdown
net stop winnat
net start winnat
```

先动 WinNAT 后执行 wsl --shutdown 会损坏 WSL2 网络，必须重启 Windows 才能恢复。

## 验证

重启后打开 WSL 终端，启动服务，确认端口可正常绑定。

## 原理

WinNAT 每次开机随机申请一段端口（如 1139-1238），1234 正好落在范围内即报错。重启 WinNAT 重新随机分配，可能避开 1234。

