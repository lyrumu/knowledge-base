---
date: 2026-01-01
draft: false
description: ""
tags: []
categories: []
showHero: true
heroStyle: "background"
---
# Hermes API 网络连接修复记录 (APIConnectionError)

## 环境

- OS: Windows 11 + WSL2 (Ubuntu)
- WSL2 IP: `172.30.30.3`
- Windows Host (网关): `172.30.16.1`
- Proxy: Clash Verge Rev (allow-lan: true, mixed-port: 7890)
- API Provider: DeepSeek (`https://api.deepseek.com/v1`)
- Hermes Agent: 源码安装 (`~/.hermes/hermes-agent/`)

---

## 问题

`hermes` 会话中频繁出现：

```
API call failed (attempt 1/3): APIConnectionError
🔌 Provider: deepseek  Model: deepseek-v4-flash
🌐 Endpoint: https://api.deepseek.com/v1
📝 Error: Connection error.
⏳ Retrying in 2.3s (attempt 1/3)...
```

间歇性发生，有时能连上，有时超时重试。

---

## 根因分析

### 1. WSL2 DNS 不稳定（主要原因）

WSL2 默认 DNS 为 `10.255.255.254`（由 Windows/WSL 自动生成），该 DNS 对 `api.deepseek.com` 的解析**间歇性超时**。

**验证过程：**

| 测试 | 结果 | 结论 |
|------|------|------|
| `nslookup api.deepseek.com` | ✅ 返回 112.13.211.83 / 086 | DNS 有时正常 |
| `dig +short api.deepseek.com` | ❌ "communications error, timed out" 但仍返回结果 | DNS 不稳定 |
| `curl --resolve` 直连（跳过 DNS） | ✅ HTTP 401, 0.13s | API 服务本身正常 |
| `curl` 正常解析 DNS 后连接 | ❌ 超时 10s, exit 28 | 问题在 DNS 解析环节 |

`api.deepseek.com` 解析到中国移动 IP（112.13.x.x），但 WSL2 默认 DNS 解析该域名不可靠。

### 2. 未配置代理

WSL2 内无 `HTTP_PROXY` / `HTTPS_PROXY` 环境变量，Python 的 `httpx` 库直连 DeepSeek 时，如果恰好 DNS 解析失败就会连接超时。

### 3. Clash 网关 IP 识别错误

早期记录中 WSL 网关 IP 被误记为 `172.30.30.1`。正确网关 IP 需从 `ip route` 获取：

```
default via 172.30.16.1 dev eth0
```

正确网关为 `172.30.16.1`，属于 `172.30.16.0/20` 子网。

---

## 修复清单

| # | 修复项 | 操作 | 影响范围 |
|---|--------|------|----------|
| 1 | 固定 WSL2 DNS | 修改 `/etc/wsl.conf` + `/etc/resolv.conf` + `wsl --shutdown` | 全局 |
| 2 | 配置代理环境变量 | 手动设置 `HTTP_PROXY` / `HTTPS_PROXY` | 当前 Shell 会话 |

### 修复 1：固定 WSL2 DNS

**步骤：**

```bash
# Step 1: 修改 /etc/wsl.conf，阻止 WSL 自动覆盖 DNS
sudo tee -a /etc/wsl.conf <<< $'\n[network]\ngenerateResolvConf = false'

# Step 2: 删除旧的 resolv.conf，新建 DNS 配置
sudo rm /etc/resolv.conf
sudo tee /etc/resolv.conf << "EOF"
nameserver 223.5.5.5      # 阿里 DNS（国内快速稳定）
nameserver 114.114.114.114 # 114DNS（备用）
EOF

# Step 3（关键！）：在 Windows PowerShell 重启 WSL，使 wsl.conf 生效
# 在 Windows 终端执行：
#   wsl --shutdown
# 然后重新打开 Ubuntu WSL

# Step 4: 验证
cat /etc/resolv.conf
# 输出应为：
# nameserver 223.5.5.5
# nameserver 114.114.114.114
```

> **为什么一定要 `wsl --shutdown`？**
> `/etc/wsl.conf` 的修改需要 WSL 实例完全重启后才能生效。如果不执行这一步，WSL 会继续自动覆盖 `/etc/resolv.conf`，自定义 DNS 会在几分钟内被还原回 `10.255.255.254`。

选择这两个 DNS 的原因：

- `223.5.5.5` — 阿里公共 DNS，国内速度快，对国内域名解析准确
- `114.114.114.114` — 114DNS，老牌国内 DNS，作为备用

### 修复 2：手动配置代理（按需）

进入 WSL 后临时设置：

```bash
export HTTP_PROXY=http://172.30.16.1:7890
export HTTPS_PROXY=http://172.30.16.1:7890
export NO_PROXY=localhost,127.0.0.1,::1,.local
```

启动 Hermes 后 Python 的 `httpx` / `requests` / `openai` 库会自动使用该代理。

**为什么不写入配置文件？** 用户选择手动控制，灵活可控，避免某些场景下代理影响预期外的流量。

---

## 修复后验证

### DNS 稳定性

```
getent hosts api.deepseek.com
→ 112.13.211.83  api.deepseek.com.eo.dnse1.com api.deepseek.com
→ 112.13.210.86  api.deepseek.com.eo.dnse1.com api.deepseek.com
```

### 走代理后的连接速度

| 目标 | 耗时 | 路由规则 |
|------|------|----------|
| 百度 (国内) | 0.11s | Clash 识别 → DIRECT |
| 淘宝 (国内) | 0.08s | Clash 识别 → DIRECT |
| DeepSeek | 0.11s | Clash 识别 → DIRECT（国内 IP） |
| Google (国外) | 0.78s | Clash 识别 → 代理节点转发 |

国内网站完全不受影响，Clash 规则引擎自动分流。

---

## 经验教训

1. **WSL2 网关 IP 不是固定的** — 每次 `ip route` 确认 `default via` 的地址。之前 `172.30.30.1` 是错的，实际是 `172.30.16.1`。IP 末尾通常是 `.1`，但前缀（172.30.16 还是 172.30.30）不一定。
2. **DNS 优先排查** — 遇到 `APIConnectionError` 先测 `curl --resolve` 跳过 DNS 确认 API 本身是否可达，再查 DNS。
3. **Clash allow-lan 配置** — 确认 `allow-lan: true` 和 `bind-address: '*'` 在订阅配置中生效，否则 WSL 连不上 Windows 的 Clash 代理端口。
4. **确认子网范围** — WSL2 的子网是 `172.30.16.0/20`，即 `172.30.16.1` ~ `172.30.31.254` 都在同一个子网。

---

## 参考命令速查

```bash
# 查看 WSL2 网关 IP
ip route | grep default

# 查看 WSL2 自身 IP
hostname -I

# 测试 API 连通性（跳过 DNS）
curl --connect-timeout 5 --resolve api.deepseek.com:443:112.13.211.83 \
  https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY"

# 测试代理是否可用
export HTTP_PROXY=http://172.30.16.1:7890
curl -s -o /dev/null -w "%{http_code} (%{time_total}s)\n" https://www.google.com
```

