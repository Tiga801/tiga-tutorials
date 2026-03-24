# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库用途

本仓库用于保存个人技术教程笔记和博客文章总结。所有内容文件均为 Markdown 格式。

- `tutorials/` — 存放技术教程笔记
- `blog-summaries/` — 存放博客文章总结

## README 自动更新机制

每次通过 Claude 的 Write 或 Edit 工具操作文件后，`.claude/hooks/update_readme.py` 会自动执行，扫描两个内容目录并重新生成 `README.md` 中的索引表格。

索引区块由 HTML 注释标记界定：

```
<!-- AUTO-INDEX:tutorials:START -->
...
<!-- AUTO-INDEX:blog-summaries:END -->
```

**不要手动编辑这两个标记之间的内容**，下次 hook 触发时会被覆盖。

如需在 Claude 之外手动触发更新：

```bash
python3 .claude/hooks/update_readme.py
```

## 文档编写规范

每篇 `.md` 文件建议遵循以下结构，以确保 README 索引能正确提取信息：

```markdown
# 文章标题

第一段为简短描述（100 字以内），会被提取到 README 索引的"描述"列。

## 正文内容...
```

- 第一个 `# 标题` 会作为 README 索引的"标题"列
- 第一个非空、非标题段落（前 100 字）会作为"描述"列
