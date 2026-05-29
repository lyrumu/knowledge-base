# Hermes Dashboard WSL2 修复记录

## 环境

- OS: Windows 11 + WSL2 (Ubuntu)
- WSL IP: `172.30.30.3`
- Proxy: Clash Verge Rev（系统代理模式）
- Hermes Agent: 源码安装（`~/.hermes/hermes-agent/`）
- `.wslconfig`: `localhostForwarding=true`

---

## 问题

`hermes dashboard` 启动后，Windows 浏览器无法正常加载页面。

---

## 根因分析

### 1. 默认端口 9119 在 WSL2 下不可用

**现象**：dashboard 绑定 `127.0.0.1:9119`，在 WSL 内 `curl 127.0.0.1:9119` 正常，但 Windows 浏览器访问 `http://localhost:9119` 无响应。

**原因**：WSL2 的 localhost 自动转发机制在系统长时间运行、休眠/唤醒后可能失效。Windows Hyper-V 虽然不保留 9119 端口，但 WSL2 的转发代理（`wslrelay` / `localhostForwarding`）可能出现状态异常。

**修复**：换用 `--port 8888`。实测 8888 端口可以通过 WSL2 localhost 转发正常访问。如果 8888 也不通，可用 `wsl --shutdown` 重启 WSL2 恢复转发。

> 注：Windows Hyper-V 保留端口范围 `7991-8090`，其中 `8020` 已被占用。8888 不在保留范围内。

### 2. 示例插件 404 导致 React 无限渲染卡死

**现象**：页面能打开但内容空白，浏览器 Console 报错：

```
GET http://172.30.30.3:9119/dashboard-plugins/example/dist/index.js net::ERR_ABORTED 404 (Not Found)
[plugins] Failed to load example from /dashboard-plugins/example/dist/index.js
```

伴随大量 `bx → Vn → bx → Vn` 递归调用栈（React 错误边界循环）。

**原因**：`plugins/example-dashboard/dashboard/manifest.json` 中 `"entry": "dist/index.js"` 引用了不存在的文件。该插件由 monorepo 的测试套件使用，未被构建到 `web_dist` 中。

**修复**：创建空桩文件 `plugins/example-dashboard/dashboard/dist/index.js`（仅含注释），消除 404 即可。

### 3. Clash 代理干扰（非主要原因）

**现象**：即使关闭 Clash 系统代理，问题依然存在。

**原因**：Clash Verge Rev 的系统代理 bypass 存在已知 bug（#1243），`localhost;127.0.0.1;::1` 绕过规则未生效。但这不是主要问题——关闭系统代理后仍不可用，说明根本原因在其他地方（见 #1）。

**结论**：Clash 问题为次要因素，换端口后自动绕过。

### 4. WSL2 NAT 安全性说明

`--host 0.0.0.0 --insecure` 在 WSL2 内实际上**只对 Windows 本机开放**：

```
[Windows 本机] ──┬── 可访问 172.30.30.3:9119 ✅
                  │
                  └── [WSL2: 172.30.30.3] ← NAT 隔离
                  
[局域网其他机器] ── 到不了 172.30.30.3 ❌
```

WSL2 使用 NAT 虚拟交换机，`172.30.30.x` 是内部私有 IP，外部不可路由。因此 `--insecure` 的"暴露风险"在 WSL2 环境下微乎其微。

---

## 修复清单

| # | 修复项 | 文件 | 操作 |
|---|--------|------|------|
| 1 | 默认端口改为 8888 | `hermes_cli/main.py:13556` | `default=9119` → `default=8888` |
| 2 | 示例插件桩文件 | `plugins/example-dashboard/dashboard/dist/index.js` | 新建空桩文件 |

---

## 最终可用命令

```bash
# 方案 A（推荐）—— 默认端口 8888，localhost 访问
hermes dashboard --no-open
# → 浏览器打开 http://127.0.0.1:8888

# 方案 B —— 直连 WSL IP（绕过 localhost 转发）
hermes dashboard --host 0.0.0.0 --insecure --no-open
# → 浏览器打开 http://172.30.30.3:9119
```

> `--no-open` 在 WSL2 中用于跳过自动打开浏览器（WSL2 无图形界面），不加也不会报错，只是多一次无用尝试。

---

## 未来建议

1. **持久化配置**：可将 `dashboard.port` 加入 `config.yaml` 的 DEFAULT_CONFIG，让用户通过 `hermes config set dashboard.port 8888` 配置，无需改源码。
2. **插件构建**：CI 流程中应确保所有 `manifest.json` 中引用的 `entry` 文件实际存在，或构建脚本覆盖所有插件。
3. **WSL2 健康检查**：`hermes doctor` 可增加 WSL2 localhost 转发检测。
