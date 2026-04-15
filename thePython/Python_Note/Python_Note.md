# <mark>Environment</mark>

---



## <mark>安装Python解释器</mark>

`win+r`输入`cmd`

在命令行窗口输入`python`回车

若输出python版本信息就说明安装成功

若无法识别就去微软商店安装,记得点击`add to path`

注：

新建`文本文件`,更改文件后缀为`.py`,然后在编译器或者记事本里写好python代码,就可以进行`多行python`文件运行了

---

## <mark>安装Python开发工具</mark>

`VScode` or `Pycharm`;

这里安装Pycharm:

网址[PyCharm，您需要的唯一 Python IDE](https://www.jetbrains.com/zh-cn/pycharm/);

`创建.py关联`选项，如果只有pycharm一个开发工具那是建议勾选的,如果有多个开发环境那一般不勾选;

`更新上下文菜单`可以右键文件用Pycharm打开,挺好的,建议勾选;

`更新path变量`使Pycharm可以便利地在终端打开,与其他开发工具协作运行,推荐勾选;

---

## <mark>Pycharm使用指南</mark>

### 设置

文件-设置-编辑-常规-自动换行：

勾选`对这些文件进行软换行`,然后把后面默认的那些文件格式都先删掉，

最后输入一个`*.*`，代表对所有文件格式进行软换行



### 项目创建

首先,文件夹名称保持`全英文`,并且`不要带空格`

先在磁盘中`创建Python_projects文件夹`,再在Pycharm中新建项目,选择存储在这个文件夹，选择后不要直接创建项目,要在路径后再加上`\Projects_name`,这样结构会更好

**解释器类型：**

项目venv：虚拟环境运行

基础conda：

自定义环境：



### 项目配置文件

`.venv`为每个项目存放环境，工具信息

`.idea`为每个项目存放配置信息，比如光标最后位置等

一般不需要动这两个文件夹



### 调试

(1)设置断点：

点击代码左侧的行数数字，使该行代码变成红色，表示标记为断点；

后续开发工具会运行到该断电为止，之后可以手动调试

(2)debug调试：

点击“调试”按钮，待程序运行到断点后，可以选择“步过，步入，单步执行，步出”等调试方式

步过就是一步步执行后续代码；



### 快捷键

在代码某一行的任意位置按`Ctrl+/`，该行代码就会被注释("#"),再次按Ctrl+/就会取消注释;

`shift+alt+.`放大代码文字大小,`shift+alt+,`减小代码文字大小;

`Ctrl+d`复制粘贴一次当前行代码到下一行;

`shift+enter`快速创建新的一行，即使光标正处于某行代码中间(这个很有用);

`alt+shift`按住不动,拖动鼠标光标,能进行`列编辑`,同时对多行进行编辑;

`ctrl+y`删除当前行代码;

`alt+p`强制大模型插件智能推荐代码

---

# <mark>Syntax</mark>

---

## 语句结束

**回车**代表语句结束，除非两部分代码写在了同一行，一般不用分号.

## 变量

Python是动态变量，**同一个变量可以存储不同类型的数据**

但还是建议一个变量就存储一个类型的数据

变量必须**赋值后**才能使用

---

# <mark>Modules</mark>

---

## streamlit

> 一个python库 通过它可以依据python语言开发交互式Web界面
> 
> 无需学习所有前端代码知识
> 
> 主要用于数据科学和机器学习



在Pycharm中打开终端PowerShell输入以下安装命令

```powershell
pip install streamlit
```

详情学习前往官方网址[Streamlit documentation](https://docs.streamlit.io/)



运行streamlit文件需要在IDE中用终端打开文件 然后输入:

`streamlit run xxxx.py`

默认占用端口是`8501` 如果出现端口异常被占用;

可以尝试其他端口例如`8000,8502,8888,8503`

在终端输入`streamlit run xxx.py --server.port 端口号`来修改使用的端口;

---

## requests

> 发送请求 用于爬虫

---

## json

---

## openai

---



---

# <mark>Problems</mark>

## lingma插件

在Pycharm中安装该插件后重启IDE

报错(1):

```powershell
updateCustomSuggestPrompt error
java.lang.NullPointerException: Cannot invoke "com.alibabacloud.intellij.cosy.db.DataSourceService.isDatasourceExist()" because "dataSourceService" is null
    at com.alibabacloud.intellij.cosy.chat.context.DatabaseContextRefProvider.register(DatabaseContextRefProvider.java:97)
    at com.alibabacloud.intellij.cosy.util.SuggestPromptUtil.updateCustomSuggestPrompt(SuggestPromptUtil.java:192)
    at com.alibabacloud.intellij.cosy.core.lsp.LanguageClientImpl.lambda$pushCustomCommand$18(LanguageClientImpl.java:515)
    at com.intellij.util.concurrency.ChildContext$runInChildContext$1.invoke(propagation.kt:167)
    at com.intellij.util.concurrency.ChildContext$runInChildContext$1.invoke(propagation.kt:167)
    at com.intellij.util.concurrency.ChildContext.runInChildContext(propagation.kt:173)
    at com.intellij.util.concurrency.ChildContext.runInChildContext(propagation.kt:167)
    at com.intellij.util.concurrency.ContextRunnable.lambda$run$0(ContextRunnable.java:26)
    at com.intellij.concurrency.ThreadContext.resetThreadContext(threadContext.kt:294)
    at com.intellij.util.concurrency.ContextRunnable.run(ContextRunnable.java:25)
    at java.desktop/java.awt.event.InvocationEvent.dispatch(InvocationEvent.java:318)
    at java.desktop/java.awt.EventQueue.dispatchEventImpl(EventQueue.java:781)
    at java.desktop/java.awt.EventQueue$4.run(EventQueue.java:728)
    at java.desktop/java.awt.EventQueue$4.run(EventQueue.java:722)
    at java.base/java.security.AccessController.doPrivileged(AccessController.java:400)
    at java.base/java.security.ProtectionDomain$JavaSecurityAccessImpl.doIntersectionPrivilege(ProtectionDomain.java:87)
    at java.desktop/java.awt.EventQueue.dispatchEvent(EventQueue.java:750)
    at com.intellij.ide.IdeEventQueue.defaultDispatchEvent(IdeEventQueue.kt:664)
    at com.intellij.ide.IdeEventQueue._dispatchEvent(IdeEventQueue.kt:517)
    at com.intellij.ide.IdeEventQueue.dispatchEvent$lambda$0$0$0$0(IdeEventQueue.kt:337)
    at com.intellij.openapi.progress.impl.CoreProgressManager.computePrioritized(CoreProgressManager.java:901)
    at com.intellij.ide.IdeEventQueue.dispatchEvent$lambda$0$0$0(IdeEventQueue.kt:336)
    at com.intellij.ide.IdeEventQueueKt.performActivity$lambda$1(IdeEventQueue.kt:1065)
    at com.intellij.openapi.application.TransactionGuardImpl.performActivity(TransactionGuardImpl.java:109)
    at com.intellij.ide.IdeEventQueueKt.performActivity(IdeEventQueue.kt:1065)
    at com.intellij.ide.IdeEventQueue.dispatchEvent$lambda$0(IdeEventQueue.kt:331)
    at com.intellij.ide.IdeEventQueue.dispatchEvent(IdeEventQueue.kt:371)
    at java.desktop/java.awt.EventDispatchThread.pumpOneEventForFilters(EventDispatchThread.java:207)
    at java.desktop/java.awt.EventDispatchThread.pumpEventsForFilter(EventDispatchThread.java:128)
    at java.desktop/java.awt.EventDispatchThread.pumpEventsForHierarchy(EventDispatchThread.java:117)
    at java.desktop/java.awt.EventDispatchThread.pumpEvents(EventDispatchThread.java:113)
    at java.desktop/java.awt.EventDispatchThread.pumpEvents(EventDispatchThread.java:105)
    at java.desktop/java.awt.EventDispatchThread.run(EventDispatchThread.java:92)
```

报错(2):

```powershell
updateCustomSuggestPrompt error
java.lang.NullPointerException: Cannot invoke "com.alibabacloud.intellij.cosy.db.DataSourceService.isDatasourceExist()" because "dataSourceService" is null
    at com.alibabacloud.intellij.cosy.chat.context.DatabaseContextRefProvider.register(DatabaseContextRefProvider.java:97)
    at com.alibabacloud.intellij.cosy.util.SuggestPromptUtil.updateCustomSuggestPrompt(SuggestPromptUtil.java:192)
    at com.alibabacloud.intellij.cosy.core.lsp.LanguageWebSocketService.refreshCustomCommands(LanguageWebSocketService.java:880)
    at com.alibabacloud.intellij.cosy.core.Cosy.lambda$asyncActionAfterCosyStart$5(Cosy.java:294)
    at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1144)
    at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:642)
    at java.base/java.lang.Thread.run(Thread.java:1583)updateCustomSuggestPrompt error
```

官方更新后已解决

---

## 依赖库路径

> 在本地直接修改项目文件夹名称后重新打开pycharm
> 
> 发现很多依赖第三方库的程序无法运行

- 根本原因:虚拟环境中有绝对路径

```textile
F:\Python_projects\Learn_python\.venv\Scripts\python.exe  ❌不存在了
F:\Python_projects\AIweb调用\.venv\Scripts\python.exe      ✅实际位置
```

`streamlit`,`lxml`等就找不到正确的python解释器了

点击项目文件夹根目录->用终端打开->

```bash
Remove-Item -Recurse -Force .venv #删除旧的虚拟环境
```

```bash
#创建新环境（.venv就是相对路径）
python -m venv .venv
#激活环境
.venv\Scripts\activate
```

```bash
#根据项目import语句重新安装所有依赖的第三方库
pip install streamlit openai requests lxml
#或者如果有requirements.txt
pip install -r requirements.txt
```

最后重新设置解释器:

在pycharm中 英文模式下双击`Shift`,输入`python interpreter`

进入后点击`添加解释器`

选择`项目文件夹/.venv/Scripts/python.exe` 作为新的解释器

然后重新运行程序试试

以后可以在根目录终端输入

```bash
pip freeze > requirements.txt
```

导出依赖文件目录

---
