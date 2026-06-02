
直接扩展里搜索`python`-安装microsoft官方插件即可；

# 可能的问题
- Powershell脚本权限
windows的powershell默认没有执行脚本权限 导致无法自动激活虚拟环境 可以通过执行(管理员)
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned 
```
然后选择“Y”来激活权限-从而顺利地使用venv虚拟环境

同时可以通过(管理员)
```powershell
Set-ExecutionPolicy -Scope CurrentUser Undefined
```
来还原Powershell设置