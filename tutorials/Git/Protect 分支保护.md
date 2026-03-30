# GitHub 分支保护配置

> **环境**：GitHub
> **最后更新**：2026-03-30

## 概述

保护 `main` 分支是保障代码库健康、防止意外覆盖或删除代码的最有效手段。设置保护后，所有代码必须通过 Pull Request 才能合并，彻底避免"手滑"造成的线上事故。

---

## 1. 找到分支保护设置入口

1. 打开 GitHub 仓库主页。
2. 点击顶部导航栏的 **Settings** 选项卡。
3. 左侧边栏 **Code and automation** 区域下，点击 **Branches**。
4. 在 "Branch protection rules" 区域，点击 **Add branch protection rule**。

## 2. 基础定义与范围

1. **命名规则集（Ruleset Name）**：填写 `Protect-Main`。
2. **设置执行状态（Enforcement status）**：选为 **Active**（激活）。
3. **绕过名单（Bypass list）**：
   - 个人项目若担心规则把自己锁死，可点击 `Add bypass` 添加自己的账号。
   - 为养成良好开发习惯，建议保持为空，强制自己也走 PR 流程。
4. **配置目标分支（Target branches）**：
   - 点击 `Add target` 并选择 `Default branch`（即 `main` 分支）。
   - 系统下方应显示 `Applies to 1 target: main`。


## 3. 规则详细配置

**Restrict deletions**、**Require a pull request before merging**、**Block force pushes** 是最经典的"黄金组合"。

**核心保护规则（建议保持勾选）：**

- **Restrict deletions**：防止任何人误删 `main` 分支。
- **Block force pushes**：极其重要！防止 `git push -f` 覆盖远程历史，避免代码丢失。
- **Require a pull request before merging**：强制所有代码必须通过 PR 进入主分支，不能直接推送到 `main`。

**进阶质量控制（根据需求勾选）：**

- **Require status checks to pass**：若配置了自动化测试（如 GitHub Actions），务必勾选。
- **Require linear history**：若希望提交历史是一条直线（无交叉 merge 线），可勾选，通常配合 Squash merge 使用。
- **Automatically request Copilot code review**：拥有 Copilot 权限时，勾选可让 AI 在 PR 提交时自动进行初步代码审查。

## 4. 保存与验证

1. 点击 **Save changes** 蓝色按钮。
2. 返回 Rulesets 列表页面，确认 `Protect-Main` 旁边的标签从 `Disabled` 变为绿色的 `Active`。
3. 在本地终端尝试直接推送到主分支：

   ```bash
   git push origin main
   ```

   **预期结果**：GitHub 拒绝推送，提示必须创建 Pull Request。
