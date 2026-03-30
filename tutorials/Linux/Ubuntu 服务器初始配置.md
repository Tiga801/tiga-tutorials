# Ubuntu 服务器初始配置

> **环境**：Ubuntu Server（适用于 aarch64 / x86_64）
> **最后更新**：2026-03-24

## 概述

Ubuntu 服务器初始化配置清单，涵盖用户管理、Docker 权限、SSH 免密登录、Zsh 定制和 Clash 代理部署。内容保持简洁，直接提供可执行指令。

## 1. 用户管理（新增 `tiga` 并授权）

在 root 用户下执行：

```bash
# 新增用户并根据提示设置密码
adduser tiga

# 将用户添加到 sudo 组
usermod -aG sudo tiga
```

## 2. Docker 权限配置

将用户 `tiga` 加入 `docker` 用户组，使其无需 `sudo` 即可运行容器：

```bash
# 添加用户到组
sudo usermod -aG docker tiga

# 刷新组权限 (或重新登录)
newgrp docker
```

## 3. 本地免密登录配置

**在本地机器执行：**

```bash
# 如果本地没有密钥对，先生成：ssh-keygen -t ed25519
# 将公钥拷贝至服务器
ssh-copy-id tiga@服务器IP
```

## 4. Zsh 深度定制（Theme: ys）

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

## 5. Clash 配置代理（使用 Mihomo/Clash Meta）

建议使用更现代的内核。这里以二进制部署为例。

### 准备二进制文件

```bash
mkdir -p ~/.config/mihomo
mkdir -p ~/clash && cd ~/clash

# 下载 mihomo 核心 (aarch64 版本)
wget https://github.com/MetaCubeX/mihomo/releases/download/v1.19.20/mihomo-linux-amd64-v1.19.20.gz
gunzip mihomo-linux-amd64-v1.19.20.gz
mv mihomo-linux-amd64-v1.19.20 mihomo
chmod +x mihomo
```

### 获取并转换配置文件

订阅链接通常为 HTTP 链接，需转换为 mihomo 兼容的 `yaml` 格式。

将 `YOUR_LINK` 替换为实际订阅地址：

```bash
curl -L -o ~/.config/mihomo/config.yaml "https://sub.xeton.dev/sub?target=clash&url=YOUR_LINK&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online.ini"
```

### 下载 Geo 数据库

`mihomo` 依赖 `geoip.dat` 和 `geosite.dat` 识别国内外流量：

```bash
cd ~/.config/mihomo

wget https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.dat
wget https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geosite.dat
```

### 验证配置文件

```bash
~/clash/mihomo -t -d ~/.config/mihomo
```

输出 `configuration file ... test is successful` 表示配置无误。

### 配置 Systemd 开机自启

```bash
sudo vi /etc/systemd/system/mihomo.service
```

```ini
[Unit]
Description=Mihomo Daemon, A rule-based tunnel in Go.
After=network.target

[Service]
Type=simple
User=tiga
Group=tiga
ExecStart=/home/tiga/clash/mihomo -d /home/tiga/.config/mihomo
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mihomo
sudo systemctl start mihomo

# 查看状态
sudo systemctl status mihomo
```

### 终端代理开关

在 `~/.zshrc` 末尾添加：

```bash
alias proxy="export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890"
alias unproxy="unset https_proxy http_proxy all_proxy"
```

```bash
source ~/.zshrc
```

### 验证代理

```bash
proxy
curl -I https://www.google.com
```

## 注意事项

- **Web 控制面板**：如需通过网页管理节点，确保 `config.yaml` 中设置 `external-controller: 0.0.0.0:9090`，然后在本地浏览器访问 [metacubexd](https://metacubex.github.io/metacubexd/)，填入服务器 IP 和端口 `9090` 即可远程切换节点。
- **nohup 替代方案**：如不配置 systemd，可用 `nohup ~/clash/mihomo -d ~/.config/mihomo > ~/clash/clash.log 2>&1 &` 后台运行，但不如 systemd 稳定。
