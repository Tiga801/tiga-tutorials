---
name: digest-blog
description: Use when the user provides a URL and wants to extract the core essence of a blog post or tutorial into a minimal, functional reference note saved to the tiga-tutorials repository.
---

# digest-blog

给定一个网页 URL，抓取内容，提炼极简精华笔记，保存至本仓库。

## 执行流程

1. **抓取**：使用 `WebFetch` 获取 URL 内容
2. **判断分类**（见下方规则）
3. **提炼**四个区块（见输出模板）
4. **确认**：用 `AskUserQuestion` 向用户确认分类和文件名（用户可修改）
5. **写入**：`Write` 到对应目录（自动触发 README 更新）

## 内容类型判断

| 特征 | 目标目录 |
|------|----------|
| 含操作步骤、命令、代码块、配置 | `tutorials/` |
| 概念解析、观点、架构分析、经验总结 | `blog-summaries/` |

## 文件命名规则

从文章标题生成 slug：小写字母、数字，空格和特殊字符替换为连字符，去除首尾连字符。

示例：`"React Hooks: A Complete Guide"` → `react-hooks-a-complete-guide.md`

## 输出模板

```markdown
# <文章标题>

> **来源**：<URL>
> **存档日期**：<YYYY-MM-DD>

## 核心宗旨

<1-3 句话：这篇文章解决什么问题？核心观点或结论是什么？>

## 关键概念 / 步骤

- <要点 1>
- <要点 2>
- <...>

## 最小可用知识

<功能性精华：关键代码片段、命令、配置项、核心论点的支撑细节。无冗余示例。>

## 扩展阅读

<文章中提到的重要参考链接（若无可省略此节）>
```

## 提炼原则

| 保留 | 丢弃 |
|------|------|
| 核心论点 / 结论 | 引言铺垫、作者自我介绍 |
| 操作步骤和命令 | 重复举例（同一概念保留 1 个最佳示例）|
| 关键代码片段 | 广告、订阅引导、评论区内容 |
| 重要注意事项和陷阱 | 过渡句、填充词、客套语 |
| 文中提到的关键外链 | 导航栏、侧边栏、页脚 |

**目标**：读完笔记即可理解原文核心，不需要回头查阅原文完成实际操作。

## 常见错误

- **过度压缩**：代码示例被删光 → 保留至少 1 个可运行示例
- **漏掉注意事项**：原文的 warning/gotcha 必须保留
- **分类错误**：概念文章中偶尔有代码不代表是 tutorial；判断主体内容
