openEuler 是一款非常稳健的企业级 Linux 发行版。虽然它与 Ubuntu 的包管理（dnf vs apt）和部分权限组（wheel vs sudo）有所不同，但整体逻辑是一致的。

openEuler 软件源中没有收录 `fzf`。在 openEuler (特别是 aarch64 架构) 上，最稳妥的方法是通过源码或官方脚本安装 `fzf`。

以下是针对 **openEuler (aarch64/ARM 架构)** 的完整配置教程：

---

## 1. 用户管理 (新增 `tiga` 并授权)

在 root 用户下执行，openEuler 使用 `wheel` 组管理 sudo 权限：

```bash
# 新增用户并设置密码
adduser tiga
passwd tiga

# 将用户添加到 wheel 组
usermod -aG wheel tiga
```

---

## 2. Docker 权限配置

允许 `tiga` 用户免 sudo 运行 Docker：

```bash
# 添加用户到 docker 组
sudo usermod -aG docker tiga

# 刷新组权限
newgrp docker
```

---

## 3. 本地免密登录配置

**在你的本地机器 (Mac/Windows/Linux) 执行：**

```bash
# 将公钥拷贝至服务器
ssh-copy-id tiga@服务器IP
```

---

## 4. Zsh 深度定制 (针对 openEuler 修复 fzf)

登录 `tiga` 用户后执行：

### 安装基础组件
```bash
sudo dnf install zsh git -y

# 安装 Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### 解决 fzf 安装问题 (通过官方 Git 方式)
```bash
# 克隆并运行 fzf 安装脚本
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --all
```

### 安装插件 (Suggestions & Highlighting)
```bash
# 自动建议
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# 语法高亮
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### 修改 `.zshrc` 配置文件
```bash
# 编辑配置文件
vi ~/.zshrc

# --- 修改以下内容 ---
ZSH_THEME="ys"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting fzf vi-mode)

# 生效
source ~/.zshrc
```

---

## 5. Clash 配置代理 (针对 aarch64 架构)

你的系统是 **aarch64 (ARM)** 架构，需要下载对应的二进制文件。

### 下载 Mihomo (原 Clash Meta)
```bash
mkdir -p ~/clash && cd ~/clash
# 下载 linux-arm64 版本
wget https://github.com/MetaCubeX/mihomo/releases/download/v1.19.20/mihomo-linux-arm64-v1.19.20.gz
gunzip mihomo-linux-arm64-v1.19.20.gz
mv mihomo-linux-arm64-v1.19.20 mihomo && chmod +x mihomo
```

### 运行与代理设置
将你的 `config.yaml` 放入 `~/.config/mihomo/`。

```bash
# 后台运行
nohup ./mihomo -d ~/.config/mihomo > clash.log 2>&1 &

# 在 ~/.zshrc 末尾添加快捷开关
alias proxy="export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890"
alias unproxy="unset https_proxy http_proxy all_proxy"

# 生效配置
source ~/.zshrc
```

---

**下一步建议：**
由于服务器重启后 Clash 会失效，需要我为你提供一个 **Systemd 服务脚本** 来实现 Clash 的开机自启吗？