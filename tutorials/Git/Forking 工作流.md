# Forking 工作流

> **环境**：Git
> **最后更新**：2026-03-30

## 概述

**Forking Workflow（复刻工作流）** 适用于在他人项目（上游仓库）基础上维护私有定制版本的场景。核心原则：主分支（`main`）只用于镜像上游更新，所有自定义开发在独立的功能分支上进行，从而实现"随时同步上游更新，又能独立开发自定义功能"。

## 1. 分支管理策略：保持主分支"纯净"

- **`main` 分支（镜像分支）：** 仅用来同步上游项目的主分支，**不做任何本地修改**。
- **`feat/*` 或 `custom` 分支（开发分支）：** 所有自定义的文档、功能模块，都应基于 `main` 创建新分支（如 `custom-features` 或 `docs-update`）进行开发和提交。

## 2. 初始化：配置上游远程仓库

克隆 Fork 后，默认远程仓库 `origin` 指向自己的仓库。需将原始项目添加为 `upstream`。

```bash
# 查看当前远程仓库状态（应该只有 origin）
git remote -v

# 添加上游仓库
git remote add upstream <上游项目的 Git 地址>

# 再次查看，确认同时存在 origin 和 upstream
git remote -v
```

## 3. 日常操作一：同步上游更新

当上游项目有新更新时，将其拉取到本地并推送到自己的仓库。

```bash
# 1. 切换到本地主分支
git switch main

# 2. 从上游拉取最新信息
git fetch upstream

# 3. 将上游更新合并到本地 main（因为 main 无本地提交，通常是 Fast-forward 合并）
git merge upstream/main

# 4. 推送同步后的状态到自己的仓库
git push origin main
```

## 4. 日常操作二：开发自定义功能

主分支更新完成后，基于 `main` 创建功能分支进行开发。

```bash
# 1. 基于最新的 main 创建并切换到自定义分支
git switch -c custom-docs

# 2. 正常开发，add 并 commit
git add .
git commit -m "Add my custom documentation"

# 3. 推送到自己仓库的自定义分支
git push origin custom-docs
```

## 5. 日常操作三：将上游更新并入自定义分支

上游再次更新后，先按步骤 3 更新 `main`，再用 `rebase` 将自定义分支的提交"变基"到最新的 `main` 上，保持提交历史整洁。

```bash
# 1. 确保 main 已是最新状态（参考步骤 3）

# 2. 切换到自定义分支
git switch custom-docs

# 3. 变基，将最新 main 作为基础
git rebase main

# 如果遇到冲突，解决冲突后继续：
# git add <冲突文件>
# git rebase --continue

# 4. 强制推送（rebase 重写了历史，必须加 -f）
git push origin custom-docs -f
```

> **注意：** `rebase` 会重写提交历史，`-f` 强制推送有风险。仅在自己独立维护的分支上操作，切勿对共享分支执行。
