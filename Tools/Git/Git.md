# <mark>Git</mark>

---

`git`是代码和项目的存储管理工具 可以保存历史版本 

每次提交修改都拥有独立的存档点

---

## <mark> Git安装</mark>

 首先cmd打开终端输入

```bash
where git
```

判断一下系统有无安装git

没有的话去官网安装即可

[Redirecting&hellip;](https://git-scm.com/download/win)

安装过程~~还挺麻烦的~~

可以一步步问AI该选择哪些选项......

---

## <mark>网站选择</mark>

首选`Github`

但是方便起见 打算先用国内的`Gitee`练手

---

## <mark>仓库创建</mark>

以下操作在github/gitee内进行.

- 初始化仓库：
  (1)选择语言:
  按需或不选，主要是给仓库打上一个“主要编程语言”的标签
  (2)添加.gitigore:
  一般推荐添加，用于告诉git哪些文件不需要管理
  (3)添加开源许可证：
  一般选择`MIT-license`(开源)
  （以上内容后期应该都是可以再添加的，可以先不选）
- 设置模板：
  (1)`readme文件`:
  仓库的**门面和说明书**，按需选择，后期可再添加
  
  (2)`issue模板文件`:
  便于别人给你的仓库提交**bug或功能建议**
  (3)`pull request模板文件`:
  当别人想为你**贡献代码**时用这个模板来请求
- 选择模型分支：
  可以先默认选择“main”或“master”分支

---

## <mark>本地文件上传</mark>

本地已有仓库 将其上传gitee 利于保存和管理 防止文件丢失；

适用于个人项目；

即先本地建立文件 再上传；

不过一般是先创建仓库再clone到本地进行开发；

注：选择本地已有的文件上传时 新建仓库**不要勾选readme和license**

因为会导致仓库和本地的初始化内容不统一；

如果已经勾选了 建议之后使用**强制推送**，使用本地内容覆盖仓库；

```bash
#首先在github新建仓库
#再在文件资源管理器中进入所需上传的文件
#然后右键文件空余处，点击在终端中打开
#然后确保终端中显示的目录就是当前想要上传的文件，then：
git init
#个人开发者的话可以用global全局设置 即所有项目用同一个身份
git config user.name "你的用户名"
git config user.email "你的邮箱@example.com"
#以下具体内容在gitee中复制即可
git remote add origin https://gitee.com/你的用户名/仓库名.git
#上传
git add .
git commit -m "初始提交：上传项目文件"
git push -u origin master -f #"强制推送(只在个人仓库初始化时使用)"
#注意，上传github不能用master分支，要用main
#git push --force-with-lease适合多人开发时使用，防止覆盖他人提交
```

push前最好`git branch`查看当前所在分支以及所有本地分支，避免推送到其他分支上，当前所在分支会在前面显示`*`符号

如果分支不匹配，用`git branch -M main`移动到正确分支上

关于获取自己github邮箱：

点击头像->settings->email；

后续在本地编辑更新完项目后 再更新上传到git：

```bash
git add .
git commit -m "更新内容给介绍"
git push
```

后期git配置状态检查：

```bash
git config --list
#或者
git config --global --list
```

---

## <mark>同步本地和仓库</mark>

首先进入本地对应文件 在此打开终端:

```bash
git fetch origin#获取远程最新状态（安全，不合并本地文件）
git status#查看本地与远程差异
git diff#查看具体文件内容差异
```

`git status`后的几种可能状态:

- `up to date with 'origin/master'`---已同步，无需操作
- `behind 'origin/master' by X commit`---本地落后，执行`git pull`
- `ahead of 'origin/master' by X commit`---本地领先，执行`git push`

---

## <mark>GitCommit优化</mark>

> 通常每次 `git commit` 只能有一个提交信息，这个信息会附加到整个提交上，而不是单个文件夹或文件上，以下尝试优化

- 推荐办法:

每次想要提交前,先`git status`;

查看当前哪些文件需要被提交;

然后依次:

```bash
git add filename1/
git commmit -m "该文件的修改内容"

git add filename2/
git commit -m "该文件修改内容"
#...
#最后统一进行git push
git push
#这样就能在github上看到对每个文件不同的提交信息了
```



---

## <mark>.Gitignore</mark>

> 被gitignore的文件,在本地依然会随着修改而变化,但每次提交不会被上传到github,即只在本地变化;

- 创建`.gitignore`文件:

在根目录右键新建文本文件-将整个文件重命名为`.gitignore`(后缀也要一起删掉!!!)

在文件内写入需要忽略的文件的路径,比如`.obsidian/workspace.json`,这样该文件就会被忽略;

检查:

```bash
#输入
ls .gitignore*
#理想输出类似
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         2026/4/18     13:36            109 .gitignore
#若输出文件名显示".gitignore.txt" 那是不正确的
```

- 使用`.gitignore`:

先提交更新后的`.gitignore`文件至github;

然后通过`git status`检查是否有已经被GIT跟踪但是需要ignore的文件;

```textile
⚠️.gitignore 只能忽略未被跟踪的文件,如果文件已经被 Git 跟踪过,需要先 git rm --cached 再忽略;
```

所以如果有,通过`git rm --cached config/secret.json`让git忘记这个文件;

之后就可以正常add-commit-push了;

---

## <mark>多平台同步</mark>

首先进入本地需要同步的文件夹，右键**在终端中打开**；
(后续操作均需在此环境下进行)

```bash
git remote -v#查看当前文件夹关联的所有远程仓库
```

需要将同一本地文件同步到不同远程仓库时，建议使用**相同的仓库名**（仓库名即为-v后显示的“仓库名.git”）在平台先建立相同名称的仓库，不要设置readme等文件；

以下以已经同步到gitee的文件，再同步到github为例：

```bash
git remote add github https://github.com/用户名/仓库名.git
```

然后根据**分支名**推送：

```bash
git push github master
```

最后再用`git remote -v`检查一下，应该会多出origin之外的仓库；

![多平台同步](./image/同步两个git.png)

后续更新时，用以下命令推送到两个仓库：

```bash
git add .
git commit -m "内容"
git push origin master#第一个一般都为origin吧
git push github master
```

后期若要定期检查本地和两个仓库同步状态：

```bash
git status#仅用来检查本地和origin的同步状态
```

![git status](./image/git%20status.png)

（up to date! 就说明本地和origin是正确同步的）；

```bash
git fetch --all#用来检查三方是否都正确同步，以下一步步执行
git log --oneline HEAD#本地最新提交
git log --oneline origin/master#gitee最新提交
git log --oneline github/master#github最新提交
```

![git fetch --all](./image/git%20fetch.png)

![log HEAD](./image/gitloghead.png)

![log origin](./image/gitlogorigin.png)

![log github](./image/gitloggithub.png)

检查三个输出内容是否相同即可；

---

## <mark>Wrong1</mark>

`wrong`:

由于在gitee上给仓库添加了`license`文件；

此时仓库有license文件 但本地并没有；

and 我并未记得；

直接更新了新的本地内容；

于是乎：
![wrong1](./image/wrong1.png)

在进行`git push`时出现报错；

处理方法：

```bash
git pull origin master#拉取远程仓库的变化更新文件，并合并到本地
```

此时终端可能会进入另一个界面，叫做"vim编辑器"；

此时要先按一下`Esc`键，再输入`:wq`,最后按一下`Enter` 应该就会恢复正常了；

最后再输入：

```bash
git push origin master
#或者这里直接用git push更好
```

---
