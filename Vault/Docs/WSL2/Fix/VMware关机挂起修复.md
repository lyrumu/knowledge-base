# VMware 导致关机挂起修复

## 环境

| 项目 | 值 |
|------|-----|
| 操作系统 | Windows 11 (Hyper-V / WSL2) |
| VMware Workstation | 17.6.4 (F:\VMware\) |
| IDE | Trae (ByteDance) / VS Code — WSL Remote 模式 |
| WSL | wsl2, memory=6GB, processors=8 |

## 问题
Trae / VS Code 连接 WSL 后关机/重启：屏幕熄灭，风扇转，电源灯常亮，需强制关机。

## 根因（两个）

### 1. vmx86 内核驱动（主因）
VMware 的核心驱动 vmx86.sys 开机自动加载，且带 `IGNORES_SHUTDOWN` 标志 → 关机时阻塞系统断电。

### 2. VMnet 网卡 + VMware 服务（次要）
VMnet1/VMnet8 虚拟网卡和 VMware 服务在关机时也可能阻塞。

## 修复

### 第一步：禁用 vmx86 驱动

```powershell
# 管理员 PowerShell
sc.exe stop vmx86
sc.exe config vmx86 start= demand
# 或用: Set-Service vmx86 -StartupType Manual
```
下次重启后，不跑 VMware 虚拟机时不加载。开 VMware 会自动加载，不影响使用。

### 第二步：禁用 VMware 服务

```powershell
Stop-Service VMAuthdService, VMnetDHCP, VMUSBArbService, "VMware NAT Service" -Force
Set-Service VMAuthdService, VMnetDHCP, VMUSBArbService, "VMware NAT Service", VmwareAutostartService -StartupType Disabled
```

### 第三步：禁用虚拟网卡

```powershell
Disable-NetAdapter -Name "VMware Network Adapter VMnet8" -Confirm:$false
Disable-NetAdapter -Name "VMware Network Adapter VMnet1" -Confirm:$false
```

### 验证（立即执行后）

```powershell
sc.exe query vmx86
# → STATE: 1 STOPPED（刚跑过 sc stop 的结果）

Get-NetAdapter | Where-Object Name -match 'VMware|VMnet'
# → 应为 Disabled 或 Not Present

Get-Service | Where-Object DisplayName -match 'VMware' | Select Name,Status,StartType
# → 全部 Stopped + Disabled
```

### 验证（重启后）

```powershell
# 重启后打开管理员 PowerShell

sc.exe query vmx86
# → STATE: 1 STOPPED  ← 正确，驱动未加载
# → STATE: 4 RUNNING  ← 说明没生效，重跑 sc.exe config vmx86 start= demand

Get-NetAdapter | Where-Object Name -match 'VMware|VMnet'
# → 不出任何结果  ← 正确，网卡已禁用

Get-Service | Where-Object DisplayName -match 'VMware' | Select Name,Status,StartType
# → 全部 Stopped, Disabled  ← 正确

# 关机测试
wsl --shutdown
shutdown /s /t 0
# → 电源灯应在 30 秒内熄灭，无需强制关机
```

## 恢复 VMware 使用

```powershell
# 网卡
Enable-NetAdapter "VMware Network Adapter VMnet8"
Enable-NetAdapter "VMware Network Adapter VMnet1"

# 服务
Set-Service VMAuthdService, VMnetDHCP, VMUSBArbService, "VMware NAT Service" -StartupType Automatic
Start-Service VMAuthdService, VMnetDHCP, VMUSBArbService, "VMware NAT Service"

# 驱动（vmx86 会在开 VMware 时自动加载）
```

## 效果

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 重启耗时 | ~3 分钟或卡死 | ~38 秒 |
| Trae WSL 后关机 | 挂起 | ✅ 正常 |
| BSOD 0x9f | 5 月 3 次 | 无 |

## 备注
- VMware 17.6.4 未卸载，仅禁用网络组件和驱动
- 如果 Clash 卡死导致网络断 + 关机挂起，先关 Clash 再重启
- 与 Hyper-V、WSL 本身无关
