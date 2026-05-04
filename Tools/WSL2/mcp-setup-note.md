# OpenCode 全局 MCP 配置笔记

## 环境要求

- Node.js ≥ 18
- OpenCode ≥ 1.14

## 1. 创建配置文件

```bash
mkdir -p ~/.config/opencode
```

`~/.config/opencode/opencode.json`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "shadcn": {
      "type": "local",
      "command": ["npx", "-y", "shadcn@latest", "mcp"],
      "enabled": true
    }
  }
}
```

## 2. 预热 npx 缓存

避免首次启动时下载失败：

```bash
npx -y shadcn@latest mcp &
sleep 2 && kill %1
```

## 3. 验证

重启 OpenCode，检查日志确认加载成功：

```bash
rg "mcp.*shadcn" ~/.local/share/opencode/log/$(ls -t ~/.local/share/opencode/log/ | head -1)
```

应出现 `service=mcp key=shadcn type=local found`，且**无** `Connection closed` 报错。

## 使用

Prompt 中加上 `use shadcn` 即可调用 shadcn MCP 工具。

---

## 添加其他 MCP

同目录 `opencode.json` 中追加即可，格式：

```json
{
  "mcp": {
    "another-mcp": {
      "type": "local",
      "command": ["npx", "-y", "some-mcp-server"],
      "enabled": true
    }
  }
}
```

远程 MCP 示例：

```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {}
    }
  }
}
```

## 参考

- [OpenCode MCP 文档](https://opencode.ai/docs/mcp-servers/)
- [OpenCode 配置文档](https://opencode.ai/docs/config/)
- [shadcn MCP](https://ui.shadcn.com/docs/cli#mcp)
