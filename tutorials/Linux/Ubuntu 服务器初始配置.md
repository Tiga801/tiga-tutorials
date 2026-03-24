这是一份为你整理的 Ubuntu 服务器初始化配置清单。手册内容保持简洁，直接提供可执行指令。

---

## 1. 用户管理 (新增 `tiga` 并授权)

在 root 用户下执行：

```bash
# 新增用户并根据提示设置密码
adduser tiga

# 将用户添加到 sudo 组
usermod -aG sudo tiga
```

---

## 2. Docker 权限配置

将用户 `tiga` 加入 `docker` 用户组，使其无需 `sudo` 即可运行容器：

```bash
# 添加用户到组
sudo usermod -aG docker tiga

# 刷新组权限 (或重新登录)
newgrp docker
```

---

## 3. 本地免密登录配置

**在你的本地机器 (Local Machine) 执行：**

```bash
# 如果本地没有密钥对，先生成：ssh-keygen -t ed25519
# 将公钥拷贝至服务器
ssh-copy-id tiga@服务器IP
```

---

## 4. Zsh 深度定制 (Theme: ys)

登录到 `tiga` 用户后执行：

### 安装 Zsh 及 Oh My Zsh
```bash
sudo apt update && sudo apt install zsh git curl fzf -y
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### 安装插件
```bash
# 自动建议
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# 语法高亮
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### 修改配置文件
编辑 `~/.zshrc`：
```bash
# 修改主题
ZSH_THEME="ys"

# 修改插件列表 (fzf 和 vi-mode 是内置的，无需额外克隆)
plugins=(git zsh-autosuggestions zsh-syntax-highlighting fzf vi-mode)

# 生效配置
source ~/.zshrc
```

---

## 5. Clash 配置代理 (使用 Mihomo/Clash Meta)

建议使用更现代的内核。这里以二进制部署为例。

### 下载与解压
```bash
mkdir ~/clash && cd ~/clash
# 请根据架构下载对应版本，此处以 amd64 为例
wget https://github.com/MetaCubeX/mihomo/releases/download/v1.18.3/mihomo-linux-amd64-v1.18.3.gz
gunzip mihomo-linux-amd64-v1.18.3.gz
mv mihomo-linux-amd64-v1.18.3 mihomo
chmod +x mihomo
```

### 配置文件
将你的订阅转化后的 `config.yaml` 放入 `~/.config/mihomo/config.yaml`。

### 设置系统代理 (写入 `~/.zshrc`)
```bash
# 在 ~/.zshrc 末尾添加
alias proxy="export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890"
alias unproxy="unset https_proxy http_proxy all_proxy"

# 生效
source ~/.zshrc
```

### 启动
```bash
# 屏幕后台运行或配置 Systemd
nohup ./mihomo -d ~/.config/mihomo > /dev/null 2>&1 &
```

---

需要我帮你把这些指令封装成一个自动化安装的 `.sh` 脚本，还是需要我为你编写 Systemd 服务来实现 Clash 的开机自启？