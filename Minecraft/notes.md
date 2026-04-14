(详细完整内容请见Minecraft Wiki)

# <mark>Datapacks</mark>

---



## <mark>Simple Introductions</mark>

    数据包只针对`单个存档`，每一个存档都会有一个数据包文件夹`（游戏版本>saves>存档名>datapacks)`

    数据包以`文件夹或者压缩包`形式存在于datapacks文件夹中都可以运行，但推荐用`压缩包`的形式

    vscode所需插件：datapack helper plus by spyglass；syntax-mcfunction

这两个插件工作的前提是，所创建文件的结构符合官方数据包结构

    所有具体标签名称可以在游戏内先`F3+H`,鼠标悬浮在物品上就可以查看

---



## <mark>固定文件结构</mark>

data命名空间；

pack.mcmeta；

pack.png；



**json文件：**

[]数组：里面要放值。键值对，数组，字符串，数值都是值；

{}对象：里面要放键值对。键值对的值可以放任何值；

然后可以无限嵌套；

数据包内json文件基本就是这个格式编写；

---



## <mark>覆盖原版</mark>

想要覆盖原版内容或者是删除原版某个内容；

对于`recipes`来说：

则需要在数据包中创建`minecraft:`命名空间，在此命名空间添加的内容会覆盖掉`原版vanilla的同名内容`，若想删除，把`result`写成`air`,或者该json文件直接为空也可以；



---



## <mark>标签tag</mark>

**标签文件：**

将若干同类型的事物定义为一个集合，方便调用；使用json格式；

replace：false->取同名冲突路径文件的并集，挺友好；

replace：true->一般不用这个，会覆盖同路径文件；

引用标签文件：#命名空间+文件名；

---



## <mark>函数function</mark>

**函数文件：**

在大多数情况可以代替命令方块使用；

一行只写一条指令；

缩进可以加在左边 右边不能再加；

加“#”注释，但注意这里注释和命令不能处于同一行；同一行要么命令要么注释；

调用一个函数时，minecraft会在一个游戏刻内执行完该函数所有命令；

函数文件中一但有错误，整个文件都会失效。因此当数据包无法执行时，需要去确认error的位置，此时可以用二分法排错，先删去一般代码再/reload，根据提示继续排错；



**函数的执行：**

函数会继承命令的执行环境；

当由数据包执行函数时：

位置位于主世界出生点，可以/setworldspawn修改，x轴正方向；

玩家输入/function执行函数时：

于玩家所在位置执行，实体对象为该玩家，该玩家维度，该玩家朝向；



两个特殊的函数标签：load.json,tick.json；名称固定，且位于minecraft命名空间下

load.json:此标签指定的函数会在数据包加载时自动执行一次

tick.json:此标签指定的函数会在每个游戏刻都执行一次，tick要谨慎使用哦



/schedule function<路径><时间>< append或者replace >命令：设置一定时间后执行函数

(一堆图片待添加)

---



## <mark>配方recipes</mark>

配方的json文件都放在`recipes`命名空间内，可以在此命名空间内再分类几个文件夹，方便开发和维护;

(json文件其实不能带注释的，但为了学习用“//”注释一下)

**crafting配方：(工作台)**

**无序合成：**

以下添加配方：用一个钻石矿+金矿+绿宝石矿，合成一个圆石

```json
{
    "type":"minecraft:crafting_shapeless",//表示原料可以无序摆放，2*2工作台也可以                                 
    "ingredients":[
        {
            "item":"minecraft:diamond_ore"
        },
        {
            "item":"minecraft:gold_ore"
        },
        {
            "item":"minecraft:emerald_ore"
        }
    ],
    "result":{
        "item":"minecraft:stone",
        "count":1    //如果是1其实可以省略改行代码，默认合成数量就是1
    }
}
```

添加“用深层钻石矿或者普通钻石矿都可以合成”的两种写法：

（1）

```json
{
    "type":"minecraft:crafting_shapeless",
    "ingredients":[
        [
            {
                "item":"minecraft:diamond_ore"
            },
            {
                "item":"minecraft:deepslate_diamond_ore"
            }
        ],//第一项钻石矿用数组形式写，数组里再包含多个键值对
        {
            "item":"minecraft:gold_ore"
        },
        {
            "item":"minecraft:emerald_ore"
        }
    ],
    "result":{
        "item":"minecraft:stone",
        "count":1
    }
}
```

（2）

```json
{
    "type":"minecraft:crafting_shapeless",
    "ingredients":[
        {
            "tag":"minecraft:diamond_ores"//不使用item而是使用能包含这一类矿石的标签tag
        },
        {
            "item":"minecraft:gold_ore"
        },
        {
            "item":"minecraft:emerald_ore"
        }
    ],
    "result":{
        "item":"minecraft:stone",
        "count":1
    }
}
```

(原版不包含的标签也可以自己写，然后引用自己写的标签)

接下来是**有序合成：**

```json
{
    "type":"minecraft:crafting_shaped",
    "pattern":[
        "aaa",
        "aba",
        "aaa"
    ],
    "key":{
        "a":{
            "item":"minecraft:obsidian"
        },
        "b":{
            "item":"minecraft:diamond_ore"
        }
    },
    "result":{
        "item":"minecraft:totem_of_undying",
        "count":1
    }
}
```



**blasting&&smelting配方：（高炉&&熔炉）**

**熔炉，高炉，烟熏炉**都是差不多的，可以举一反三

**篝火**也可也编写的，也与上面三者类似，只不过**没有experience**可以编写

```json
{
    "type": "minecraft:blasting",
    "ingredient": {
        "item": "minecraft:diamond_block"
    },
    "result": "minecraft:coal",//这类result直接填id就好了
    "experience": 666,//获得经验值
    "cookingtime": 200//所需时间(游戏刻)
}
```

**切石机**比较特殊，**count必须写**，而且可以写**一对多**，就是完全一样的配方生成多种不同物品，其他的写法同上；

**锻造台(smithing)**：新版需要锻造模版；有点复杂放到后面再说；



---
