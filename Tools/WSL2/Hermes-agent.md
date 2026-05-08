---

Hermes Agent 安装步骤（WSL）

> 文档强调：原生 Windows 不支持，必须在 WSL2 中运行。

---

一、前置条件
唯一硬性要求：git 已安装
git --version   # 确认 git 可用
其余所有依赖（Python 3.11、Node.js v22、ripgrep、ffmpeg、uv）均由安装器自动检测并安装，无需手动预装。

---

二、一键安装
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
安装器自动完成：

- 检测系统，设置依赖
- 克隆仓库到 ~/.hermes/hermes-agent/
- 创建 Python 虚拟环境
- 安装 Python 依赖
- 创建 ~/.local/bin/hermes 软链接
- 写入 PATH 到 ~/.bashrc
- 可选：LLM provider 配置引导

---

三、安装后的文件结构变化
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
与 OpenCode 零冲突：OpenCode 在 ~/.opencode/ 和 ~/.config/opencode/，Hermes 在 ~/.hermes/，二进制名也不同。

---

四、安装后首次配置
步骤 1：重新加载 shell
source ~/.bashrc   # 或 source ~/.zshrc
步骤 2：配置 LLM Provider（最关键的一步）
hermes model
支持的 provider（文档中列出的部分）：
Provider    认证方式
Nous Portal    OAuth 登录
OpenAI Codex    Device code OAuth
Anthropic    OAuth 或 API key
OpenRouter    API key
DeepSeek    DEEPSEEK_API_KEY
GitHub Copilot    OAuth
Custom Endpoint    base URL + API key（支持 Ollama/vLLM 等）
Alibaba Cloud / DashScope    DASHSCOPE_API_KEY

> 文档特别提示：模型至少需要 64K tokens 上下文窗口。

步骤 3：运行首次对话验证
hermes            # 经典 CLI
hermes --tui      # 推荐，现代 TUI 界面
步骤 4：验证会话持久化
hermes --continue    # 恢复最近会话
hermes -c            # 简写

---

五、后期配置建议（按优先级排列）
第一优先级：基础可用性
命令    作用
hermes model    更换/添加 LLM provider 和模型
hermes tools    配置启用的工具集（terminal、web、skills 等）
hermes config set terminal.backend local    终端后端（默认 local，可换 docker/ssh/modal 等）
hermes setup    完整配置向导
第二优先级：安全加固（文档强制建议）

1. 设置 .env 文件权限
      chmod 600 ~/.hermes/.env

2. 配置危险命令审批模式（~/.hermes/config.yaml）
      approvals:
     mode: manual    # manual | smart | off
     timeout: 60

3. 如果你以后用 gateway（消息平台），文档强调必须配置 allowlist，否则默认全部拒绝：
   
   # ~/.hermes/.env
   
   TELEGRAM_ALLOWED_USERS=你的用户ID

4. 生产部署 checklist（文档原文）：
   
   - 设置明确的 allowlist
   - 使用 Docker 后端做容器隔离
   - 设置资源限制（CPU/内存/磁盘）
   - API 密钥放 .env 并 chmod 600
   - 不要以 root 运行 gateway
   - 定期更新：hermes update
     第三优先级：进阶功能
     场景    命令/配置
     接入消息平台    hermes gateway setup（文档建议 CLI 跑通后再搞）
     Docker 隔离    hermes config set terminal.backend docker
     定时任务    hermes cron create "每天上午9点发日报"
     安装技能    hermes skills search kubernetes → hermes skills install ...
     MCP 集成    编辑 ~/.hermes/config.yaml 加 mcp_servers 段
     语音模式    pip install "hermes-agent[voice]" 然后 /voice on
     编辑器集成 (ACP)    pip install -e '.[acp]' → hermes acp，支持 VS Code/Zed/JetBrains
     配置自动压缩    默认已启用，compression.threshold: 0.50，到 50% 上下文时自动压缩
     故障排查工具（文档推荐顺序）
     hermes doctor              # 诊断一切
     hermes model               # 重新配置 provider
     hermes setup               # 全量配置向导
     hermes sessions list       # 列出所有会话
     hermes --continue          # 恢复会话测试
     hermes gateway status      # gateway 状态

---

六、更新与卸载
操作    命令
更新    hermes update（文档说会自动拉代码、更新依赖、跑 config migrate、重启 gateway）
预览更新    hermes update --check（只检查不更新，可用于脚本）
查看版本    hermes version
卸载    hermes uninstall（可选保留 ~/.hermes/ 配置）

---

总结一句话：先 curl ... | bash 装完，然后 hermes model 配 provider，再 hermes 跑起来验证，其他功能等基础对话稳定了再一层层往上加。
