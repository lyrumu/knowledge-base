
>官方docs:[Windows (WSL) | OpenCode](https://opencode.ai/docs/windows-wsl)
---
# Setup
![[image/WSL内安装opencode.png]]

如果网络不好,可以按如下图临时配置WSL代理端口,然后重新输入
`curl -fsSL https://opencode.ai/install | bash`
我使用的是windows clashcerge的混合端口
用`curl ipinfo.io`检查是否配置成功
![[image/设置WSL代理端口.png]]

显示下载完成后 运行`opencode --help`
如果有输出就是安装成功

```bash
lyrumu@LAPTOP-ARJGE44Q:~$ opencode --help
opencode: command not found
lyrumu@LAPTOP-ARJGE44Q:~$ ls ~/.local/bin | grep opencode
lyrumu@LAPTOP-ARJGE44Q:~$ find ~ -type f -name "opencode*" 2>/dev/null
/home/lyrumu/.opencode/bin/opencode
lyrumu@LAPTOP-ARJGE44Q:~$ ls ~/.opencode
bin
lyrumu@LAPTOP-ARJGE44Q:~$ ls ~/.local
ls ~/.local/bin
bin  lib  share
blind_watermark   dul-upload-pack  git-dumper  z3
dul-receive-pack  dulwich          normalizer
lyrumu@LAPTOP-ARJGE44Q:~$ find ~ -name opencode 2>/dev/null
/home/lyrumu/.opencode/bin/opencode
lyrumu@LAPTOP-ARJGE44Q:~$ export PATH=$HOME/.opencode/bin:$PATH
lyrumu@LAPTOP-ARJGE44Q:~$ opencode --help
```
这配置环境变量之后 我才能使用`opencode --help`命令;

然后才考虑统一配置wsl环境变量
```bash
echo 'export PATH=$HOME/.opencode/bin:$PATH' >> ~/.bashrc
source ~/.bashrc 
```
为opencode设置
```bash
echo 'export PATH=$HOME/.opencode/bin:$HOME/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```
为所有工具设置

具体操作:
```bash
nano ~/.bashrc
```
然后按`向下键`一直到底部
复制粘贴这一行:
```bash
export PATH=$HOME/.opencode/bin:$HOME/.local/bin:$PATH
```
然后按`Ctrl+O`写入,再按`Enter`,最后按`Ctrl+X`退出即可
最后可以`source ~/.bashrc`让配置立即生效


在`echo $PATH`测试后 发现我的windows环境变量和wsl污染严重
因此:
```bash
sudo nano /etc/wsl.conf
```
写入:
```bash
[interop]
enabled = true
appendWindowsPath = false
```
保存退出 重启wsl 再测试echo path 就干净很多了


---
# Use

在WSL终端操作windows项目:
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
