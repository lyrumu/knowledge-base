# scripts/ — 历史遗留脚本（已冻结）

⚠️ **本目录所有脚本已于 2026-06-25 起标记为"冻结不维护"**。

---

## 状态总览

| 脚本 | 状态 | 最后用途 |
|---|---|---|
| `vault-to-hugo.ps1` | 🟡 冻结 | Obsidian Vault → Hugo leaf bundle 同步 |
| `migrate-vault.ps1` | 🟡 冻结 | 一次性内容迁移 |
| `restructure-folders.ps1` | 🟡 冻结 | 目录重构 |
| `full-rebuild.ps1` | 🟡 冻结 | 完整重建 |
| `fix-images.ps1` | 🟡 冻结 | 修复 image 目录 |
| `fix-lines.ps1` | 🟡 冻结 | 行修复 |
| `add-bom.ps1` | 🟡 冻结 | UTF-8 BOM 处理 |
| `test-debug.ps1` | 🟡 冻结 | 测试脚本 |
| `test-hash.ps1` | 🟡 冻结 | 测试脚本 |
| `test-parse.ps1` | 🟡 冻结 | 测试脚本 |
| `test-utf8bom.ps1` | 🟡 冻结 | 测试脚本 |

---

## 冻结原因

未来新增内容改为**手动上架**（直接编辑 `content/<section>/` 和 `data/*.yaml`），不再自动同步。

## 保留原因

- 可能需要回退参考
- Vault 目录仍然在本地，仅不再自动同步

## 删除时机

确认不再需要回退时，可整体删除 `scripts/` 目录。

## 新内容上架流程（替代 vault-to-hugo.ps1）

1. 在 `content/<section>/<slug>/index.md` 手写 Markdown + frontmatter
2. 图片放到 `static/image/<section>/<slug>/*.png`
3. `hugo server` 验证
4. `git add` + `git commit` + `git push`

详见 [PROJECT_MAP.md §7](file:///f:/Notes/PROJECT_MAP.md) 加新内容 SOP。