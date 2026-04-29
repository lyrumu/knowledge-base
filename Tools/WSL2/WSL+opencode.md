
>官方docs:[Windows (WSL) | OpenCode](https://opencode.ai/docs/windows-wsl)
---
# Settings

---
## Proxy

打开WSL运行`curl -fsSL https://opencode.ai/install | bash
来安装opencode;
![[image/WSL内安装opencode.png]]

如果网络不好,可以临时配置WSL代理端口,然后重新输入:
`curl -fsSL https://opencode.ai/install | bash`

我使用的是`windows clashverge`的混合端口;
要查看`Clash Verge`端口 比如是7890;
先运行`ip route`，获取`your_host_ip`;
然后执行:
```bash
export http_proxy="http://your_host_ip:7890"
export https_proxy="http://your_host_ip:7890"
```
最后可以用`curl ipinfo.io`检查是否配置成功
显示下载完成后;
先刷新一下配置`source ~/.bashrc` ,然后运行`opencode --help`;
如果有输出就是安装成功啦;

为了解决网络问题 可以考虑给WSL永久配置上Windows的代理;(其实临时更好)
先检查Clash Verge里的端口，比如混合端口是7890：
```bash
nano ~/.bashrc # 进入配置页面
```
在配置页面最后加上如下内容
```bash
# 自动获取 Windows Host IP  
HOST_IP=$(ip route | awk '/default/ {print $3}')  
# HTTP / HTTPS Proxy
export http_proxy="http://$HOST_IP:7890"  
export https_proxy="http://$HOST_IP:7890"  
# SOCKS5 Proxy（按 Clash 实际端口修改）  
export all_proxy="socks5://$HOST_IP:7898"
```
加载配置
```bash
source ~/.bashrc
```
简单测试:
```bash
env | grep proxy # 有输出对应变量即可
```


---

## 重装Ubuntu
>出现难以解决的问题可以考虑

### 重装第一步
彻底删除旧的Ubuntu;
```powershell
wsl --unregister Ubuntu
```

重新安装Ubuntu:
可以直接点击任务栏Ubuntu图标 很快就会自动重装
需要重新设置用户名和密码
然后先更新软件包
```bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
```

### 换源
> 个人认为不必要切换root用户,先换源就好

先备份配置文件
```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```
再更改国内镜像源:(参考)
先打开配置文件
```bash
sudo nano /etc/apt/sources.list
```
将编辑器内内容替换为下面的内容(仅供参考)
```bash
# 清华大学开源软件镜像站 - Ubuntu 22.04 LTS (Jammy)
# 官方帮助文档：https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
# 以下为可选：Proposed（预发布更新，一般不建议启用）
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
# # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
```
注意自己Ubuntu的版本 版本不同源也不同;
最后运行;
```bash
sudo apt update
```
输出没有报错即可;
也可以使用脚本`bash <(curl -sSL https://linuxmirrors.cn/main.sh)`直接完成配置 但黑盒;

### env
优化环境变量,运行下图命令,(可选)
![[image/优化环境变量.png]]

在`echo $PATH`测试后 发现我的WSL由于继承windows环境变量后污染严重;
决定关闭继承;
因此:
```bash
sudo nano /etc/wsl.conf
```
在最后写入:
```bash
[interop]
enabled = true
appendWindowsPath = false
```
然后按`Ctrl+O`写入,再按`Enter`,最后按`Ctrl+X`退出即可
最后可以运行`source ~/.bashrc`让配置立即生效
或者在windows的Powershell里输入;
```powershell
wsl --shutdown
```
再重启WSL;
再在WSL内测试`echo $PATH` 就干净很多了;

### 安装nodejs
推荐先装nvm:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
```
然后`source ~/.bashrc`加载配置，检测`nvm --version`;
接着安装稳定版nodejs:
```bash
nvm install --lts
```
最后用`nvm ls`,`node -v`,`npm -v`检测是否安装成功;


### 备份Ubuntu
>在确认当前Ubuntu环境配置相对干净后,可以导出一个备份;

在windows打开终端:
```bash
wsl -l -v #复制输出的完整Ubuntu名称 
wsl --shutdown #先关闭wsl
```
然后先建立好你想保存备份的文件夹;
最后运行下面指令即可
```bash
wsl --export YOUR_UBUNTU_NAME D:\wsl_backup\ubuntu_snapshot.tar #示例路径
```

---
# Use
---
## project area

在WSL终端操作Windows项目:
```bash
cd /mnt/c/Users/YourName/project
opencode
```

全部在WSL内工作:(性能更好)
```bash
cd ~
mkdir opencode_projects
cd opencode_projects
mkdir test
cd test
opencode
```

---
## opencode functions

- `/timeline`-选择对话记录-`revert undo messages and file changes`;
将对话和代码回退到当时状态重新修改;(WSL内文件不可回退);
- `/share`-对话链接自动进入粘贴板-浏览器打开链接可分享,`/unshare`关闭链接;
- `/export`将对话导出为文件;
 - `/undo`撤销操作 可多次进行 这个可能比较有用;

### AGENTS.md

![[image/opencode AGENTS.md.png]]
按上图配置AGENTS.md即可;
不过优先考虑通过改变工程架构来提升agent能力;

### skills





### LCP




### plugins

`Oh My Opencode`:




---
