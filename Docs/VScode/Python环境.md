
直接扩展商店里搜索`python`-安装microsoft官方插件即可；

---

# Flask

- Python多版本:
系统已经将py3.14安装并写进系统PATH，但是flask目前更适合3.10-3.12的python
因此再去官网安装python3.12 此时注意几点:

1.不要再添加进系统环境变量
2.参考的安装选项:
![](image/Python环境/file-20260609163603242.png)
(只需要pip就行了 其他都是多余的 因为已经安装过3.14的py)
![](image/Python环境/file-20260609163609280.png)
(推荐给所有用户安装 其后按照图示配置即可)


- 之后创建项目:
可以先检查py的安装
```bash
py -0
```
应该会输出3.14和3.12两个py版本

然后创建并激活虚拟环境venv
```bash
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```
最后`pip install flask`


---

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