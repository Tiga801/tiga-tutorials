---
name: update-readme
description: Use when the user wants to manually update the README.md index, or after modifying files in tutorials/ or blog-summaries/. Reviews changed content to determine if README index needs updating before running the update script.
---

# update-readme

检查 `tutorials/` 和 `blog-summaries/` 目录下的文件变更，判断是否需要更新 README.md 索引，按需运行更新脚本。

## 执行流程

1. **检查修改状态**：运行 `git status --short`，过滤出 `tutorials/` 和 `blog-summaries/` 下的变更文件
2. **读取修改内容**：用 Read 工具读取变更文件，理解具体变化（新增/删除/内容修改）
3. **判断是否需要更新**：
   - **需要更新**：有新增文件、有文件被删除、文件名变化、文件内 `# 标题` 有变化、第一段描述有变化
   - **不需要更新**：仅修改正文中后续段落，不影响标题和描述
4. **执行或跳过**：
   - 需要更新 → 运行 `python3 .claude/hooks/update_readme.py`，再用 `git diff README.md` 确认结果
   - 不需要更新 → 告知用户无需更新，并说明原因

## 判断依据

`update_readme.py` 从每个文件提取以下信息写入 README 索引：

| 索引字段 | 来源 |
| -------- | ---- |
| 标题 | 文件内第一个 `# 标题`（无则用文件名） |
| 描述 | 第一个非空、非标题、非 blockquote（`>`）段落（前 100 字） |
| 最后修改 | 文件系统 mtime |

**只有上述字段发生变化时，README 才需要更新。**

## 注意事项

- 脚本会扫描 **所有** `tutorials/` 和 `blog-summaries/` 中的 `.md` 文件，不限于本次修改的文件
- 如果两个目录均无 `.md` 文件，索引显示"暂无文件"
- 运行后可直接执行 `commit` skill 提交变更
