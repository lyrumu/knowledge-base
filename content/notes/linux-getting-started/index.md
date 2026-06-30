---
# =============================================================================
# 基础信息（必填）
# =============================================================================
title: "Linux Basics: WSL2 Installation to OpenCode / Hermes Agent Deployment"
date: 2026-06-23
draft: false
description: "WSL2 Ubuntu Installation → Linux Basic Commands → OpenCode Agent → Hermes Agent Deployment, and collect WSL2 Common Issues Fix Records"

# =============================================================================
# URL 与权重（slug 留空 = 使用文件夹名 linux-getting-started）
# =============================================================================
slug: ""
weight: 0

# =============================================================================
# 分类与标签
# =============================================================================
tags: [linux, wsl2, ubuntu, opencode, hermes, agent]
categories: [development, devops]
topics: []
series: [wsl2]

# =============================================================================
# 作者信息
# =============================================================================
showAuthor: true

# =============================================================================
# 日期
# =============================================================================
showDate: true
showDateUpdated: false
dateUpdated: ""

# =============================================================================
# Hero（顶部横幅）
# =============================================================================
showHero: true
heroStyle: "background"
heroBackground: ""
heroImage: ""
heroBackgroundImage: ""

# =============================================================================
# 目录
# =============================================================================
showTableOfContents: true

# =============================================================================
# 阅读信息
# =============================================================================
showReadingTime: true
showWordCount: true

# =============================================================================
# 其他功能
# =============================================================================
showZenMode: true
showRelatedContent: false
relatedContentLimit: 3
sharingLinks: []

# =============================================================================
# 面包屑导航
# =============================================================================
showBreadcrumbs: true

# =============================================================================
# 评论（暂不做）
# =============================================================================
showComments: false

# =============================================================================
# Open Graph / SEO
# =============================================================================
images: []
---

> 本文整合了Vault中，涵盖 WSL2 安装、Linux 常用命令、OpenCode / Hermes Agent 部署，以及 VMware 关机挂起、WinNAT 端口冲突、Dashboard 修复、API 网络修复等笔记.
> 
> 还在更新中

---

## 1. 为什么选择 WSL2

WSL2（Windows Subsystem for Linux 2）是微软官方的 Windows Linux 子系统，相比传统方案：

| 方案 | 启动速度 | 性能 | 资源占用 | 与 Windows 集成 |
|------|---------|------|---------|----------------|
| 原生双系统 | 慢（需重启） | 原生 | 占整盘 | ❌ 完全隔离 |
| VMware/VirtualBox | 慢 | 接近原生 | 重（需分配整块资源） | ⭕ 需配共享文件夹 |
| WSL1 | 即时 | 慢（API 翻译） | 轻 | ⭕ |
| **WSL2** | **< 2s** | **接近原生（虚拟化）** | **按需动态分配** | **✅ 文件系统互通** |

简单说：**WSL2 = Linux 体验 + Windows 便利**。文件系统互通意味着 Windows 上的项目可以在 WSL2 里用 Linux 工具链处理，反之亦然。

---

## 2. 安装 WSL2 Ubuntu

### 2.1 一键安装（推荐）

以 **管理员身份** 打开 PowerShell，执行：

```powershell
wsl --install
```

默认安装 Ubuntu LTS。安装完成后**重启电脑**。

### 2.2 验证安装

重启后打开"Ubuntu"应用（开始菜单搜索），首次启动会要求设置用户名和密码（Linux 账户，与 Windows 账户独立）。

进入终端后执行：

```bash
lsb_release -a
# 应输出 Ubuntu 22.04 LTS 或更高版本
```

### 2.3 重装 Ubuntu（环境彻底损坏时）

如果 Ubuntu 环境被搞乱（例如 PATH 污染严重、依赖混乱），最干净的办法是**重装**：

```powershell
# 在 PowerShell 中执行
wsl --unregister Ubuntu
```

然后重新打开 Ubuntu 图标，会自动触发重装。需要重新设置用户名和密码。

---

## 3. 基础配置

### 3.1 更新软件包

```bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
```

### 3.2 换源（国内加速）

默认源在国外，更新和装包都很慢。**清华源** 国内速度极快。

先备份原配置：

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

打开配置文件：

```bash
sudo nano /etc/apt/sources.list
```

将文件内容**全部替换**为（Ubuntu 22.04 Jammy 清华源）：

```bash
# 清华大学开源软件镜像站 - Ubuntu 22.04 LTS (Jammy)
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
```

> ⚠️ **注意版本号**：不同 Ubuntu 版本（focal / jammy / noble）源地址不同，自己是什么版本就用什么版本的源。

保存退出（`Ctrl+O` → `Enter` → `Ctrl+X`），然后：

```bash
sudo apt update
```

输出无报错即成功。

> 💡 **黑盒脚本**：也可以用 `bash <(curl -sSL https://linuxmirrors.cn/main.sh)` 一键换源，但脚本是黑盒的，建议了解原理后手动配。

### 3.3 优化环境变量（推荐）

WSL2 默认会**继承 Windows 的 PATH**，会把 Windows 的可执行文件都带进 Linux 环境。Python 装了多个版本时容易乱。

#### 优化前（查看现有 PATH）

![优化环境变量](image/优化环境变量.webp)
*`echo $PATH` 看到的 PATH 列表，可以看出 Windows 的路径混了进来*

#### 关闭继承

```bash
sudo nano /etc/wsl.conf
```

在文件末尾追加：

```bash
[interop]
enabled = true
appendWindowsPath = false
```

`Ctrl+O` 写入 → `Enter` 确认 → `Ctrl+X` 退出。

**在 Windows PowerShell** 里重启 WSL 让配置生效：

```powershell
wsl --shutdown
```

重新打开 Ubuntu，执行 `echo $PATH`，PATH 列表会干净很多。

### 3.4 备份 Ubuntu（强烈推荐）

环境配置相对干净后**务必导出一份备份**：

```powershell
# 在 Windows PowerShell 执行
wsl -l -v                          # 复制输出的完整 Ubuntu 名称（默认是 Ubuntu）
wsl --shutdown                     # 先关闭 WSL
wsl --export Ubuntu D:\wsl_backup\ubuntu_snapshot.tar
```

> ⚠️ **U盘备份坑**：U盘如果是 FAT32，单文件 > 4GB 会失败。先把 U盘格式化成 **exFAT** 再备份。

恢复备份：

```powershell
wsl --import Ubuntu D:\wsl_install D:\wsl_backup\ubuntu_snapshot.tar
```

---

## 4. 基础 Linux 命令入门

WSL2 默认用户是普通用户，需要 root 权限时加 `sudo`。

### 4.1 文件与目录

```bash
pwd                       # 显示当前目录
ls                        # 列出文件
ls -la                    # 列出所有文件（含隐藏）+ 详细信息
cd /path/to/dir           # 切换目录
cd ~                      # 回到家目录（/home/<username>）
cd ..                     # 返回上级目录
mkdir my_dir              # 新建目录
mkdir -p a/b/c            # 递归新建多级目录
rm file.txt               # 删除文件
rm -r my_dir              # 递归删除目录
rm -rf my_dir             # 强制递归删除（慎用！）
cp src.txt dst.txt        # 复制文件
cp -r src_dir/ dst_dir/   # 递归复制目录
mv old.txt new.txt        # 重命名 / 移动
cat file.txt              # 一次性打印整个文件
less file.txt             # 分页查看（q 退出，空格翻页）
head -n 20 file.txt       # 看前 20 行
tail -n 20 file.txt       # 看后 20 行
tail -f log.txt           # 实时追踪日志
```

### 4.2 文本处理

```bash
echo "hello"              # 打印字符串
echo "x" > file.txt       # 覆盖写入
echo "x" >> file.txt      # 追加写入
grep "pattern" file.txt   # 搜索文本
grep -rn "TODO" src/      # 递归搜索（含行号）
grep -i "error" log.txt   # 忽略大小写
sed -i 's/old/new/g' file.txt   # 全文替换
awk '{print $1}' file.txt        # 打印第 1 列
sort file.txt             # 排序
uniq file.txt             # 去重（需先 sort）
wc -l file.txt            # 统计行数
```

### 4.3 系统信息

```bash
uname -a                  # 内核信息
whoami                    # 当前用户
hostname                  # 主机名
uptime                    # 运行时长
date                      # 当前时间
df -h                     # 磁盘使用
du -sh dir/               # 目录大小
free -h                   # 内存使用
nproc                     # CPU 核心数
```

### 4.4 进程管理

```bash
ps aux                    # 列出所有进程
ps aux | grep python      # 过滤进程
top                       # 实时进程监控（q 退出）
htop                      # top 的升级版（更友好，需 apt install htop）
kill PID                  # 结束进程
kill -9 PID               # 强制结束
pkill -f process_name     # 按名字杀进程
```

### 4.5 文件权限

```bash
ls -l file.txt
# -rw-r--r-- 1 user user 1234 Jan 1 12:00 file.txt
# ↑ 类型  ↑ 所有者  ↑ 用户组   ↑ 大小

chmod 755 script.sh       # rwxr-xr-x（所有者全权，其他人读+执行）
chmod +x script.sh        # 加可执行权限
chmod 600 ~/.ssh/id_rsa   # 仅所有者可读写
chown user:group file.txt # 改变所有者和组
```

权限数字速记：`r=4 / w=2 / x=1`，三位数字分别代表 **所有者 / 用户组 / 其他人**。

### 4.6 网络

```bash
ip addr                   # 查看 IP 地址（替代 ifconfig）
ip route                  # 查看路由表
curl https://example.com  # 发起 HTTP 请求
curl -I url               # 只看响应头
wget url                  # 下载文件
ping example.com          # 测试连通性
ssh user@host             # 远程登录
scp file user@host:/path  # 远程拷贝
nslookup domain.com       # DNS 查询
```

### 4.7 软件包管理（apt）

```bash
sudo apt update                       # 刷新软件源
sudo apt install package              # 安装
sudo apt remove package               # 卸载
sudo apt search keyword               # 搜索
sudo apt list --installed             # 列出已安装
sudo apt upgrade                      # 升级所有
```

### 4.8 压缩解压

```bash
tar -czvf archive.tar.gz dir/         # 打包 + gzip 压缩
tar -xzvf archive.tar.gz              # 解压 .tar.gz
tar -xjvf archive.tar.bz2             # 解压 .tar.bz2
unzip file.zip                        # 解压 zip
zip -r archive.zip dir/               # 打包 zip
```

### 4.9 服务管理（systemd）

WSL2 Ubuntu 默认没有 systemd，要先用 `service` 命令；如需 systemd 见 [WSL2 systemd 启用](https://learn.microsoft.com/en-us/windows/wsl/systemd)。

```bash
sudo service nginx start              # 启动服务
sudo service nginx stop               # 停止服务
sudo service nginx status             # 查看状态
sudo service nginx restart            # 重启
```

### 4.10 实用技巧

```bash
# 历史命令
history                                # 查看历史命令
Ctrl + R                               # 反向搜索历史（输入关键字）

# 快捷键
Ctrl + C                               # 终止当前命令
Ctrl + D                               # 退出当前 shell
Ctrl + L                               # 清屏
Ctrl + A / E                           # 跳到行首 / 行尾

# 管道与重定向
cmd1 | cmd2                            # 管道：cmd1 输出作为 cmd2 输入
cmd > file                             # 覆盖重定向
cmd >> file                            # 追加重定向
cmd < file                             # 从文件读取输入

# 后台运行
nohup python app.py &                  # 后台运行，关闭终端不影响
```

---

## 5. 安装 Node.js（OpenCode / Hermes 都需要）

OpenCode 和 Hermes Agent 都需要 Node.js（Hermes 还需要 Python 3.11+）。

### 5.1 用 nvm 管理多版本（推荐）

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc                      # 加载配置
nvm --version                         # 验证

nvm install --lts                     # 安装最新 LTS
nvm ls                                # 列出已安装版本
node -v                               # 验证 node
npm -v                                # 验证 npm
```

---

## 6. OpenCode Agent

> 官方文档：[Windows (WSL) | OpenCode](https://opencode.ai/docs/windows-wsl)

OpenCode 是一款终端 AI 编码 Agent，支持多 LLM Provider，类似 Claude Code。

### 6.1 一键安装

在 WSL2 终端执行：

```bash
curl -fsSL https://opencode.ai/install | bash
```

![WSL 内安装 OpenCode](image/WSL内安装opencode.webp)
*OpenCode 安装脚本执行中*

安装完成后加载配置并验证：

```bash
source ~/.bashrc
opencode --help                       # 有输出即安装成功
```

### 6.2 解决网络问题

如果安装脚本报网络错误（DNS 污染或被墙），需要**给 WSL 配置 Windows 代理**。

#### 临时配置

先在 Windows 的 Clash Verge（或同类代理软件）里看代理端口（一般是 `7890`），然后：

```bash
# 在 WSL 内执行
ip route                              # 获取 Windows 主机 IP（default via 后的 IP）
export http_proxy="http://<your_host_ip>:7890"
export https_proxy="http://<your_host_ip>:7890"
curl ipinfo.io                        # 有输出即代理生效
```

代理生效后重新执行 `curl -fsSL https://opencode.ai/install | bash`。

#### 永久配置（写入 ~/.bashrc）

```bash
nano ~/.bashrc
```

在文件末尾追加：

```bash
# 自动获取 Windows Host IP
HOST_IP=$(ip route | awk '/default/ {print $3}')
# HTTP / HTTPS Proxy
export http_proxy="http://$HOST_IP:7890"
export https_proxy="http://$HOST_IP:7890"
# SOCKS5 Proxy（按 Clash 实际端口修改）
export all_proxy="socks5://$HOST_IP:7898"
```

加载配置：

```bash
source ~/.bashrc
env | grep proxy                      # 应输出三个 proxy 变量
```

### 6.3 在 WSL 中使用 OpenCode

#### 操作 Windows 上的项目

```bash
# /mnt/c/ 是 WSL 访问 Windows C 盘的固定挂载点
cd /mnt/c/Users/YourName/project
opencode
```

#### 纯 WSL 内项目（性能更好）

```bash
cd ~
mkdir opencode_projects
cd opencode_projects
mkdir test
cd test
opencode
```

### 6.4 OpenCode 实用命令

| 命令 | 作用 |
|------|------|
| `/timeline` | 查看对话记录，可 `revert undo messages and file changes` 回退到当时状态（**WSL 内文件不可回退**） |
| `/share` | 生成分享链接，自动复制到剪贴板，浏览器打开即可分享 |
| `/unshare` | 关闭分享链接 |
| `/export` | 导出当前对话为文件 |
| `/undo` | 撤销操作（可多次进行） |
| `/session` | 管理当前项目下的历史会话 |

### 6.5 AGENTS.md

在项目根目录创建 `AGENTS.md`，告诉 Agent 项目约定：

![AGENTS.md 配置示例](image/opencode-AGENTSmd.webp)
*AGENTS.md 的推荐配置方式*

> 不过优先考虑通过**改变工程架构**来提升 Agent 能力，而不是堆指令。

### 6.6 Skills（技能扩展）

Skills 是 OpenCode 的可插拔能力扩展，类似 Claude Code 的 MCP。

```text
全局 skills：~/.config/opencode/skills/各 skill 文件
项目 skills：<project_root>/.opencode/skills/各 skill 文件
```

可以在 OpenCode 中输入 `/skill` 检查安装情况。推荐社区：[SkillHub](https://www.skillhub.cn/)。

### 6.7 MCP 集成

在 `~/.config/opencode/opencode.json` 中配置：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "shadcn": {
      "type": "local",
      "command": ["npx", "-y", "shadcn@latest", "mcp"],
      "enabled": true
    },
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "enabled": true,
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

Prompt 中说 `use shadcn` 即可调用对应 MCP 工具。

### 6.8 插件：Oh My OpenCode

如果有 Claude / Codex / Go 订阅，强烈推荐：

把以下 prompt 发给 OpenCode：

```textline
Install and configure oh-my-opencode by following the instructions here:
https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/dev/docs/guide/installation.md
```

来源：[code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)

### 6.9 OpenCode 使用最佳实践

> ⚠️ **Session 与目录绑定**：session 绑定到 `cwd / absolute path / workspace path`，改名或移动后 session 找不到。

推荐做法：

- **不要在深层子目录启动** OpenCode
- **在 project root 启动**，Agent 自己 `cd` 子目录
- **先想好项目结构再开发**，后期再改结构会让旧 session 失效

```bash
# 推荐：在 project root 启动
cd project_root
opencode

# 错误：在深层子目录启动
cd project/backend
opencode
```

如果已改名导致 session 丢失：要么改回原目录名，要么从 project root 启动（不要进改名后的子目录）。

---

## 7. Hermes Agent

> 官方文档：[Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs)

Hermes Agent 是 Nous Research 出品的开源 AI Agent，定位类似 Claude Code 但更开放。

### 7.1 前置条件

唯一硬性要求：**git 已安装**。

```bash
git --version                          # 确认 git 可用
```

其余所有依赖（Python 3.11、Node.js v22、ripgrep、ffmpeg、uv）均由安装器自动检测并安装。

### 7.2 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

安装器自动完成：

- 检测系统，设置依赖
- 克隆仓库到 `~/.hermes/hermes-agent/`
- 创建 Python 虚拟环境
- 安装 Python 依赖
- 创建 `~/.local/bin/hermes` 软链接
- 写入 PATH 到 `~/.bashrc`
- 可选：LLM provider 配置引导

### 7.3 安装后的目录结构

```text
~/.hermes/
├── config.yaml          # 配置（模型、终端、工具等）
├── .env                 # API 密钥和 secrets
├── auth.json            # OAuth 凭据
├── SOUL.md              # agent 人格定义
├── hermes-agent/        # 代码仓库
├── memories/            # 持久记忆
├── skills/              # 技能
├── cron/                # 定时任务
├── sessions/            # 会话
└── logs/                # 日志
~/.local/bin/hermes      # 可执行文件软链接
```

> ✅ **与 OpenCode 零冲突**：OpenCode 在 `~/.opencode/` 和 `~/.config/opencode/`，Hermes 在 `~/.hermes/`，二进制名也不同。

### 7.4 首次配置

#### Step 1：重新加载 shell

```bash
source ~/.bashrc                       # 或 source ~/.zshrc
```

#### Step 2：配置 LLM Provider

```bash
hermes model
```

支持的 provider：

| Provider | 认证方式 |
|----------|----------|
| Nous Portal | OAuth 登录 |
| OpenAI Codex | Device code OAuth |
| Anthropic | OAuth 或 API key |
| OpenRouter | API key |
| DeepSeek | `DEEPSEEK_API_KEY` |
| GitHub Copilot | OAuth |
| Custom Endpoint | base URL + API key（支持 Ollama / vLLM 等） |
| Alibaba Cloud / DashScope | `DASHSCOPE_API_KEY` |

> 📌 文档特别提示：模型至少需要 **64K tokens** 上下文窗口。

#### Step 3：运行首次对话

```bash
hermes                                  # 经典 CLI
hermes --tui                            # 推荐：现代 TUI 界面
```

可以让 Hermes 默认启动 TUI（修改配置）：

![Hermes TUI 配置](image/hermes-tui-config.webp)
*在 Hermes 配置中默认使用 TUI*

#### Step 4：验证会话持久化

```bash
hermes --continue                       # 恢复最近会话
hermes -c                               # 简写
```

### 7.5 基础交互命令

```bash
/help              # 查看所有命令列表
/title 我的会话    # 给当前会话起名字
/new               # 开始新会话（工具变更后需要这个才能生效）
/retry             # 重新发送上一条消息
/undo              # 撤销上一轮对话
/resume            # 恢复之前命名的会话
/compress          # 手动压缩对话历史（省 token）
/stop              # 停止正在运行的进程
/model grok-4      # 切换模型（不用退出）
/reasoning medium  # 设置推理深度（none/low/medium/high）
/clear             # 清屏
```

快捷键：`Alt+Enter` 或 `Ctrl+J` 换行。

### 7.6 高级功能命令

```bash
# 配置相关
hermes config                              # 查看当前配置
hermes config edit                         # 用编辑器打开配置文件
hermes config set key val                  # 设置某个值

# 工具管理
hermes tools                               # 交互式启用/禁用工具
hermes tools list                          # 查看所有工具状态

# 技能管理
hermes skills list                         # 已安装技能
hermes skills search 关键词                # 搜索技能市场
hermes skills install 名称                 # 安装技能

# MCP 服务器
hermes mcp add 名称 --command "npx ..."    # 添加 MCP
hermes mcp list                            # 列出所有 MCP

# 诊断与配置
hermes doctor                              # 健康检查
hermes doctor --fix                        # 自动修复能修的问题
hermes setup                               # 交互式配置向导
hermes sessions list                       # 列出所有会话
hermes gateway status                      # gateway 状态
hermes gateway setup                       # 配置远程平台
hermes dashboard                           # 打开网页端（端口见下）
hermes --tui sessions browse               # TUI 方式选择历史对话
```

![Hermes TUI 历史会话浏览](image/hermes-tui-sessions.webp)
*`hermes --tui sessions browse` 的界面效果*

### 7.7 安全加固（生产部署必做）

**1. 限制 .env 文件权限**

```bash
chmod 600 ~/.hermes/.env
```

**2. 配置危险命令审批模式**

编辑 `~/.hermes/config.yaml`：

```yaml
approvals:
  mode: manual          # manual | smart | off
  timeout: 60
```

**3. 配置 gateway allowlist（如果使用消息平台）**

```bash
# ~/.hermes/.env
TELEGRAM_ALLOWED_USERS=你的用户ID
```

**4. 生产部署 checklist**

- 设置明确的 allowlist
- 使用 Docker 后端做容器隔离
- 设置资源限制（CPU / 内存 / 磁盘）
- API 密钥放 .env 并 chmod 600
- 不要以 root 运行 gateway
- 定期更新：`hermes update`

### 7.8 进阶功能

| 场景 | 命令 / 配置 |
|------|-------------|
| 接入消息平台 | `hermes gateway setup`（文档建议 CLI 跑通后再搞） |
| Docker 隔离 | `hermes config set terminal.backend docker` |
| 定时任务 | `hermes cron create` "每天上午9点发日报" |
| 安装技能 | `hermes skills search kubernetes` → `hermes skills install ...` |
| MCP 集成 | 编辑 `~/.hermes/config.yaml` 加 `mcp_servers` 段 |
| 语音模式 | `pip install "hermes-agent[voice]"` 然后 `/voice on` |
| 编辑器集成 (ACP) | `pip install -e '.[acp]'` → `hermes acp`（支持 VS Code / Zed / JetBrains） |
| 配置自动压缩 | 默认已启用，`compression.threshold: 0.50`，到 50% 上下文时自动压缩 |

### 7.9 更新与卸载

```bash
hermes update                  # 更新（自动拉代码 + 更新依赖 + config migrate + 重启 gateway）
hermes update --check          # 只检查不更新
hermes version                 # 查看版本
hermes uninstall               # 卸载（可选保留 ~/.hermes/ 配置）
```

---

## 8. WSL2 + OpenCode + Hermes 组合的优势

### 8.1 相比原生 Windows

| 维度 | Windows + PowerShell | WSL2 + 工具链 |
|------|---------------------|---------------|
| 包管理 | 无统一方案（scoop/chocolatey/winget 三分天下） | apt 一行搞定 |
| 工具链 | 路径分隔符、shell 语法与 Unix 差异大 | 完整 Linux 工具链 |
| AI Agent 兼容 | 多数 Agent 原生支持 Linux，Windows 体验差 | 全部原生支持 |
| 性能 | 单 OS | WSL2 接近原生 |
| 文件路径 | `C:\` 反斜杠 | `/mnt/c/` 正斜杠，WSL 内 `/` |

### 8.2 相比 Mac

| 维度 | Mac | WSL2 |
|------|-----|------|
| Linux 体验 | ✅ 原生 | ✅ 几乎原生 |
| 与 Windows 协作 | ❌ 无 Windows | ✅ 同一台机器双系统 |
| 游戏 / 日常软件 | ✅ 体验好 | ✅ Windows 仍然主导 |
| 价格 | 💰 较贵 | 💰 用现有 Windows 机器 |

### 8.3 相比传统 VM（VMware / VirtualBox）

| 维度 | VMware | WSL2 |
|------|--------|------|
| 启动速度 | 30s - 2min | **< 2s** |
| 资源占用 | 预分配（占整盘） | 动态分配 |
| 与 Windows 文件互通 | 需配共享文件夹 | **直接 `/mnt/c/` 访问** |
| 剪贴板 / 网络 | 需装 VMware Tools | **直接复用 Windows** |

### 8.4 OpenCode vs Hermes

| 维度 | OpenCode | Hermes |
|------|----------|--------|
| 定位 | 终端 AI 编码 Agent | 通用 AI Agent（编码 / 任务 / 定时） |
| 默认模型 | 需手动配 | 需手动配 |
| Skills | ✅ 项目级 + 全局 | ✅ 全局 + 持久记忆 |
| MCP | ✅ | ✅ |
| 定时任务 | ❌ | ✅ `hermes cron` |
| 消息平台 | ❌ | ✅ `hermes gateway` |
| 持久记忆 | ❌ | ✅ `memories/` |
| TUI | ❌ | ✅ `hermes --tui` |
| 仪表盘 | ❌ | ✅ `hermes dashboard` |

**最佳实践**：两个都装，按需切换。WSL 内路径不同时也不冲突（`~/.opencode/` vs `~/.hermes/`）。

---

## 9. 常见问题修复

### 9.1 VMware 导致 WSL 关机挂起

> 来源：[VMware关机挂起修复.md](file:///f:/Notes/Vault/Docs/WSL2/Fix/VMware关机挂起修复.md)

**症状**：Trae / VS Code 连接 WSL 后关机/重启，屏幕熄灭，风扇转，电源灯常亮，需强制关机。

**根因**：

1. `vmx86.sys` 驱动开机自动加载且带 `IGNORES_SHUTDOWN` 标志（主因）
2. VMnet1 / VMnet8 虚拟网卡 + VMware 服务关机时阻塞（次因）

**修复（管理员 PowerShell）**：

```powershell
# 1. 禁用 vmx86 驱动
sc.exe stop vmx86
sc.exe config vmx86 start= demand

# 2. 禁用 VMware 服务
Stop-Service VMAuthdService, VMnetDHCP, VMUSBArbService, "VMware NAT Service" -Force
Set-Service VMAuthdService, VMnetDHCP, VMUSBArbService, "VMware NAT Service", VmwareAutostartService -StartupType Disabled

# 3. 禁用虚拟网卡
Disable-NetAdapter -Name "VMware Network Adapter VMnet8" -Confirm:$false
Disable-NetAdapter -Name "VMware Network Adapter VMnet1" -Confirm:$false
```

**恢复 VMware**（需要用时）：

```powershell
Enable-NetAdapter "VMware Network Adapter VMnet8"
Enable-NetAdapter "VMware Network Adapter VMnet1"
Set-Service VMAuthdService, VMnetDHCP, VMUSBArbService, "VMware NAT Service" -StartupType Automatic
Start-Service VMAuthdService, VMnetDHCP, VMUSBArbService, "VMware NAT Service"
```

**效果**：关机耗时 ~3 分钟 → ~38 秒。

### 9.2 WinNAT 端口冲突

> 来源：[WinNAT端口冲突修复.md](file:///f:/Notes/Vault/Docs/WSL2/Fix/WinNAT端口冲突修复.md)

**症状**：服务报 `EACCES: permission denied 0.0.0.0:PORT`，端口被 WinNAT 随机保留占用。

**排查**：

```powershell
# 1. 查进程占用
netstat -ano | findstr :PORT

# 2. 查 WinNAT 保留范围
netsh interface ipv4 show excludedportrange protocol=tcp
```

端口出现在排除范围 → WinNAT 随机保留。

**修复（必须按顺序）**：

```powershell
# 管理员 PowerShell
wsl --shutdown                  # 先停 WSL
net stop winnat                 # 再停 WinNAT
net start winnat                # 再起 WinNAT
```

> ⚠️ **顺序错误会损坏 WSL2 网络**：先动 WinNAT 再 `wsl --shutdown` 会导致必须重启 Windows 才能恢复。

### 9.3 Hermes Dashboard 修复

> 来源：[hermes-dashboard-fix.md](file:///f:/Notes/Vault/Docs/WSL2/Hermes/hermes-dashboard-fix.md)

**问题**：`hermes dashboard` 启动后 Windows 浏览器无法加载页面。

**根因**：

1. 默认端口 `9119` 在 WSL2 下不可用（localhost 转发可能失效）
2. 示例插件 404 导致 React 无限渲染卡死

**修复**：

```bash
# 方案 A：换端口 8888
hermes dashboard --no-open
# 浏览器打开 http://127.0.0.1:8888

# 方案 B：直连 WSL IP
hermes dashboard --host 0.0.0.0 --insecure --no-open
# 浏览器打开 http://172.30.30.3:9119
```

如果 8888 仍不通：`wsl --shutdown` 后重启 WSL2 可恢复 localhost 转发。

**进阶修复**（修改源码）：把 `hermes_cli/main.py` 的 `default=9119` 改为 `default=8888`；并在 `plugins/example-dashboard/dashboard/dist/` 下创建空 `index.js` 桩文件消除 404。

> 📌 **WSL2 NAT 安全性**：`--host 0.0.0.0 --insecure` 在 WSL2 内**只对 Windows 本机开放**。WSL2 用 NAT，`172.30.x.x` 是内部私有 IP，外部不可路由。

### 9.4 Hermes API 网络连接修复

> 来源：[hermes-api-network-fix.md](file:///f:/Notes/Vault/Docs/WSL2/Hermes/hermes-api-network-fix.md)

**症状**：`hermes` 会话中频繁出现 `APIConnectionError`，间歇性超时重试。

**根因**：

1. WSL2 默认 DNS `10.255.255.254` 对 `api.deepseek.com` 解析**间歇性超时**
2. 未配置代理，Python `httpx` 直连时遇到 DNS 失败就超时

**修复 1：固定 WSL2 DNS**

```bash
# 阻止 WSL 自动覆盖 DNS
sudo tee -a /etc/wsl.conf <<< $'\n[network]\ngenerateResolvConf = false'

# 重建 resolv.conf
sudo rm /etc/resolv.conf
sudo tee /etc/resolv.conf << "EOF"
nameserver 223.5.5.5
nameserver 114.114.114.114
EOF

# 关键：在 Windows PowerShell 重启 WSL
# wsl --shutdown
```

> ⚠️ **必须 `wsl --shutdown`**：`/etc/wsl.conf` 的修改需要 WSL 实例完全重启后才能生效，否则自定义 DNS 会被自动还原。

**修复 2：手动配置代理**

```bash
export HTTP_PROXY=http://172.30.16.1:7890
export HTTPS_PROXY=http://172.30.16.1:7890
export NO_PROXY=localhost,127.0.0.1,::1,.local
```

**WSL2 网关 IP 每次都不同**：

```bash
ip route | grep default            # 找 "default via" 后面的 IP
```

常见误区：早期记录把网关记为 `172.30.30.1`，实际是 `172.30.16.1`，子网是 `172.30.16.0/20`。

---

## 10. 速查命令汇总

```bash
# WSL 状态
wsl -l -v                          # 列出已安装的 Linux 发行版
wsl --shutdown                     # 关闭所有 WSL 实例
wsl --export Ubuntu <path.tar>     # 导出备份
wsl --import Ubuntu <install_path> <path.tar>   # 恢复备份

# OpenCode
opencode                           # 启动
opencode --help                    # 帮助
/opencode: --continue              # 恢复会话（具体看版本）

# Hermes
hermes                             # CLI
hermes --tui                       # TUI（推荐）
hermes model                       # 配置 LLM
hermes doctor                      # 诊断
hermes doctor --fix                # 自动修复
hermes update                      # 更新
hermes skills list                 # 技能列表
hermes dashboard --no-open         # 仪表盘
hermes --tui sessions browse       # 浏览历史会话

# 代理（WSL 临时）
export http_proxy="http://$(ip route | awk '/default/ {print $3}'):7890"
export https_proxy="http://$(ip route | awk '/default/ {print $3}'):7890"

# DNS 检查
nslookup api.deepseek.com          # DNS 查询
curl --resolve api.deepseek.com:443:112.13.211.83 https://api.deepseek.com/v1/models  # 跳过 DNS
```

---

### 官方文档

- [Windows (WSL) | OpenCode](https://opencode.ai/docs/windows-wsl)
- [OpenCode MCP 文档](https://opencode.ai/docs/mcp-servers/)
- [OpenCode 配置文档](https://opencode.ai/docs/config/)
- [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs)
- [oh-my-opencode (插件)](https://github.com/code-yeongyu/oh-my-openagent)
- [SkillHub - 中国用户 Skills 社区](https://www.skillhub.cn/)
