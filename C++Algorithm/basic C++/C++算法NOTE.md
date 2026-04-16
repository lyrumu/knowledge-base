# C++/C算法n0t3

---

## <<算法>>

---

### <mark>qsort快排(c语言)</mark>

1.qsort函数原型

```c++
void qsort(void *base, size_t nmemb, size_t size, 
           int (*compar)(const void *, const void *));
```

2.具体写法
（1）先写<mark>比较函数</mark> （返回的是整形）

```c++
// 升序排序（从小到大）
int cmp_asc(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}
// 降序排序  （从大到小）
int cmp_desc(const void *a, const void *b) {
    return (*(int*)b - *(int*)a);
}
```

解释：因为排序的类型可能是int,double等各种，所以用<u>const void*a</u>表示可以<u>指向任何类型</u>的指针，然后在return中先将a转化成对应题目类型的指针例如<u>（int*）</u> ，再<u>在前面加*</u> 表示指针所指的具体值
（2）再在<mark>主函数中调用</mark> 

```c++
qsort(a,n,sizeof(int),cmp);
```

a表示要排序的数组的首地址
n表示数组长度
sizeof（int）表示这个数组类型的数据长度
cmp是提前写好的比较函数的名称
3.原理
比较函数cmp中，（~~有点难理解~~但很重要！！）
若返回负值--->将参数a排在参数b前面
若返回0--->参数a，参数b顺序不变
若返回正值--->将参数a排在参数b后面
依此可以写各种其他不同排序：（待开发）

---

### <mark>GCD&LCM</mark>

最大公约数函数(gcd):

```c++
int gcd(int a,int b){
    if(b==0){
        return a;
    }
    return gcd(b,a%b);//欧几里得算法,辗转相除法,递归版
}//以上参数顺序不可以调换！
```

最小公倍数函数(lcm):

```c++
int lcm(int a,int b){
    if(a==0 || b==0){
        return 0;
    }
    //return (a*b)/gcd(a,b);为了防止溢出，先除以gcd，再乘：
    return a/gcd(a,b)*b;//***
}
```

---

### <mark>两两乘积之和化简</mark>

eg:一个数组a[n];计算数组中所有不同的两个元素的乘积之和（前后顺序相反的算同一组）

即a1​⋅a2​+a1​⋅a3​+⋯+a1​⋅an​+a2​⋅a3​+⋯+a(n−2)​⋅a(n−1)​+a(n−2)​⋅an​+a(n−1)​⋅an

算法思维：

​![乘积化简](./images/屏幕截图%202025-11-07%20231654.png)

具体代码：

```c++
ll a[n];//ll 表示long long
ll total_sum = 0;
ll square_sum = 0;
for(ll i = 0;i<n;i++){
    cin>>a[i];
    total_sum = total_sum+a[i];
    square_sum = square_sum+a[i]*a[i];
}
ll sum = (total_sum*total_sum-square_sum)/2;
```

---

### <mark>一维前缀和 </mark>

1.为何诞生？
Runtime Error：
个人是因为，在计算数组的各个子数组，各个元素之和时复杂度太大
前缀和算法能够帮助提高效率，处理更大更复杂的数据
2.定义前缀和
数组a[n];
令sum[i] = a1​+a2​+⋯+ai​（其中sum[0] = 0）
3.具体用法
计算一维数组的各个前缀和：

```c++
int a[n];//先定义一个大小乱序的数组
//这里省略数组初始化...
long long presum[n+1] = {0};//初始化前缀和先都为0,大小为n+1防止越界(一定要开足空间！！)
for(int i = 1;i<=n;i++){//i从1开始，更符合人类习惯，"前i个的和..."
    presum[i] = a[i-1]+presum[i-1];//第i个元素+前i-1个
}
```

4.结合例题
题目（一）：利用前缀和，计算数组的各个子数组中的各个元素之和
解法：

```c++
int a[n];
//这里省略初始化数组，省略前缀和公式
for(int l = 0;l<n;l++){
    for(int r = l;r<n;r++){
        //a[r]是第r+1个元素，a[l]是第l+1个元素***
        int sum = presum[r+1]-presum[l];//***
    }
}
```

---

### <mark>二维前缀和</mark>

1.定义二维前缀和

一个n*m的二维数组矩阵a【n】【m】；
令sum【i】【j】 = $\sum_{i=1}^{n} \sum_{j=1}^{m} \text{a}[i][j]$;

 2.具体用法

计算二维数组的各个前缀和

```c++
//注意！为了后续方便，若要计算二维数组前缀和
//初始化赋值时下标从1开始！！***
int a[n+5][m+5];
for(int i = 1;i<=n;i++){
    for(int j = 1;j<=m;j++){
        cin>>a[i][j];
    }
}
//计算前缀和
vector<vector<int>> presum(n+5,vector<int>(m+5,0));
for(int i = 1;i<=n;i++){
    for(int j = 1;j<=m;j++){
        presum[i][j] = a[i][j]+presum[i-1][j]+presum[i][j-1]-presum[i-1][j-1];//*** 
    }
}
```

3.结合例题

题目（一）：一个二维矩阵，计算其各个子矩阵的各个元素之和
解法：

```c++
//先枚举所有子矩阵
for(int r1 = 1;r1<=n;r1++){
    for(int r2 = r1;r2<=n;r2++){//r1,r2分别表示上下边
        for(int c1 = 1;c1<=m;c1++){
            for(int c2 = c1;c2<=m;c2++){//c1，c2表示左右边
                //计算子矩阵元素和
                int sum = presum[r2][c2]-presum[r1-1][c2]-presum[r2][c1-1]+presum[r1-1][c1-1];//***
            }    
        }
    }
}
```

```c++
//若子矩阵是边长为len的正方形
//以(i,j)坐标为子矩阵右下角
for(int i = len;i<n;i++){
    for(int j = len;j<n;j++){
        int sum = presum[i][j]-presum[i-len][j]-presum[i][j-len]+presum[i-len][j-len];
    }
}
```

题目（二）：

---

### <mark>滑动窗口</mark>

适用题型：

`固定长度的，或长度有限制的区间和等`

假设所需求求和的窗口区间长度为`len`

```c++
//初始化第一个窗口[0,len-1]的和
int window_sum = 0;
for(int i = 0;i<len;i++){
    window_sum += arr[i];
}
max_sum = window_sum;
//用i表示窗口左边界，逐个移动
//每移动一格，window_sum减去左边一个元素，加上右边一个元素哦
for(int i = 1;i+len-1<=n-1;i++){//理解限制条件
    window_sum = window_sum-arr[i-1]+arr[i+len-1];
    max_sum = (max_sum,window_sum); 
}
```

上面为什么是`i+len-1<=n-1`呢？？？

因为`len`表示整个窗口的元素数量，

例如i=0，若直接`i+len`,则最后整个窗口会包含`len+1`个元素.所以应该是`i+len-1<=n-1`（这很重要！！！）



eg：
![滑动窗口题目哦](./images/屏幕截图%202025-11-01%20230151.png)
解法：（只是为了~~拓展介绍~~此算法，实际仍是超时哦，还是需要用特殊的前缀和算法）

```c++
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n,a,b;
    cin>>n,a,b;
    vector<char> s(n);
    for(int i = 0;i<n;i++){
        cin>>s[i];
    }
    int cnt = 0;//计数，表示满足条件的（l，r）的个数
    for(int l = 0;l<n;l++){//以下展现了滑动窗口思想***
        int cnta = 0;
        int cntb = 0;//在l固定的时候就初始化计数a，b的个数
        for(int r = l;r<n;r++){
        //扩展右边界时更新计数
        //即，r每更新一次，就假设此时的（l，r）为一组，立刻测试本组的cnta，cntb是否满足条件。
        //依此，可以省去第三重for循环（原本是要确定l，r后再遍历的）
            if(s[r]=='a') cnta++;
            else if(s[r]=='b') cntb++;
            if(cnta>=a && cntb<b){//每次都要判断哦
                cnt++;
            }
        }
    }
    cout<<cnt;
    return 0
```

---

### <mark>冒泡排序</mark>

```c++
#include <bits/stdc++.h>
using namespace std;
int a[n];
//这里省略对数组a的输入
for(int i = 0;i<n-1;i++){//n个数，则进行n-1次交换
    for(int j = 0;j<n-1-i;j++){//每一次的交换（因为已经完成了i次交换）
        if(a[j]>a[j+1]){//从小到大排序
            swap(a[j],a[j+1]);//交换
        }
    }
}
```

---  

### <mark>选择排序</mark>

核心思想：每次选择最大或最小的元素，将其排在正确位置。

```c++
using namespace std;
int arr[n];
for(int i = 0;i<n-1;i++){//n个元素交换n-1次，这次寻找第i小的元素
    int minindex = i;//假设当前i就是最小的索引
    for(int j = i+1;j<n;j++){//在之后的索引，寻找更小的元素
        if(arr[j]<arr[minindex]){
            minindex = j;//找到的话改变minindex
        }
    }
    if(minindex!=i){//优化一下
        swap(arr[i],arr[minindex]);//将第i小的元素放在相应位置
    }
}
```

---

### <mark>插入排序</mark>

我认为相对`选择排序`和`冒泡排序`，`插入排序`较难理解嗯.

`核心思想`：将一个元素按顺序插入到已经排好序的序列中！！

`Steps`:

1. 你左手一开始是空的（已排序区）。

2. 你用右手从桌上（未排序区）拿起一张牌。

3. 将这张牌与左手中**从右向左**的牌依次比较，找到它应该插入的位置。

4. 将比它大的牌都向右挪一个位置，然后把它插入到空位。

5. 重复步骤2-4，直到所有牌都拿到左手。

`Code`:

```c++
int a[n];
for(int i = 1;i<n;i++){//从1开始，默认第一个是排序好的
    int key = a[i];//存储当前需要排序的元素
    int j = i-1;//与其前面的元素一一比较
    while(j>=0 && a[j]>key){//只要j没有超出数组初始下标并且a[j]还是大于key
        a[j+1] = a[j];//向右移动
        j--;//比较下一个元素
    }
    //此时找到第一个小于等于key的元素下标   
    a[j+1] = key;//所以在那个元素的下一个地方插入key元素     
}
```



---

### <mark>Kadane最大子数组和</mark>

属于一种`动态规划`算法

```c++
int a[n];
for(int i = 0;i<n;i++){
    cin>>a[i];//初始化数组（包含负数）
}
int max_endhere = a[0];
int max_sum = a[0];
for(int i = 1;i<n;i++){
    max_endhere = max(a[i],max_endhere+a[i]);//精髓
    //即，如果当前值a[i]比前面局部最大值加上当前值还要大
    //则直接从当前值重新开始计算
    max_sum = max(max_sum,max_endhere);
}
cout<<max_sum;
```

对于每个位置i，需要决定是继续扩展前面的子数组；

还是从这里重新开始一个新的子数组！

`max_endhere`表示以元素`a[i]`结尾的子串中的最大字串和



**拓展：环形最大子数组和**(最小值法)

写成函数的形式（）嗯

环形数组时，若最大子数组和是跨越首位的情况，用总和减去最小子数组和就是答案

```c++
int max_sub_sum_circular(int *nums,int nums_size){
    if(nums==NULL || nums_size==0)return 0;
    int maxsum = nums[0];
    int max_endhere = nums[0];
    int minsum = nums[0];
    int min_endhere = nums[0];    
    int total = nums[0];
    for(int i = 1;i<nums_size;i++){
        total += nums[i];
        max_endhere = max(nums[i],max_endhere+nums[i]);
        min_endhere = min(nums[i],min_endhere+nums[i]);
        maxsum = max(maxsum,max_endhere);
        minsum = min(minsum,min_endhere);
    }
    if(maxsum<0){
        return maxsum;//必要的判断！防止数组全是负数时的bug
        //全是负数时，总和-最小和=0，但是数组中子数组和此时不可能为0对吧！
    }
    return max(maxsum,total-minsum);
}
```

---

### <mark>LIS</mark>

(LIS指longest increasing subsequencec,即最大上升子序列)

一.`最大上升子序列`(O(n^2))

```c++
int a[n];//初始化完一个随意的数字序列
int lis[n];//表示以第i个元素作为LIS最后一个元素时，的最长序列长度
int max_lis = 1;//全局最长LIS
for(int i = 0;i<n;i++){
    lis[i] = 1;//长度包含自己 至少为1
    for(int j = 0;j<i;j++){//每一个i，在i前逐一寻找
        if(a[j]<a[i]){//指如果满足升序
            lis[i] = max(lis[i],lis[j]+1);
        }
    }
    max_lis = max(max_lis,lis[i]);
}
cout<<max_lis<<endl;
```

二.`合唱队型（先升序后降序）`

![合唱队型](./images/屏幕截图%202025-11-17%20162454.png)

策略是：单独求最大升序列和最大降序列

```c++
int tall[n];//初始化n个同学身高
//最大升序
int lis[n];
for(int i = 0;i<n;i++){
    lis[i] = 1;
    for(int j = 0;j<i;j++){
        if(tall[j]<tall[i]){
            lis[i] = max(lis[i],lis[j]+1);
        }
    }
}
//最大降序
int lds[n];//表示第i个作为LDS最前面的元素时，的最大降序列
for(int i = n-1;i>=0;i--){
    lds[i] = 1;
    for(int j = n-1;j>i;j--){
        if(tall[j]<tall[i]){
            lds[i] = max(lds[i],lds[j]+1);
        }
    }
}
//寻找最合适的“峰值”，LIS和LDS可以以此首位相接哦
int max_len = 2;
for(int i = 0;i<n;i++){//遍历所有可能的峰值
    max_len = max(max_len,lis[i]+lds[i]-1);
}
cout<<n-max_len<<endl;//输出最少要抽出的人数
```

三.`Dliworth theory：`

`任意有限偏序集，最大反链的长度==最小正链划分数目`

eg：一个随机序列a。最大升序子序列的长度，就等于下面问题的答案哦----->

Q:将全部元素划分为若干个降序列，最少需要划分为多少个？？

---

### <mark>LIS二分优化</mark>

> 如果只是求LIS的长度 这个方法O(n log n)比较适合

> 核心是 用tail[k]数组维护 LIS长度为k时的结尾最小值(最优结尾值)

```c++
const int N = 1000005;
int n;
int a[N];
int tail[N];
//tail是递增的 因为len越长 最优结尾值一般也需要更大
//也正因如此才能用二分查找
cin>>n;
for(int i = 0;i<n;i++){
    cin>>a[i];
    tail[i] = INT_MAX;//别忘了给tail初始化
}
int len = 0;//目前LIS的值
for(int i = 0;i<n;i++){
    int x = a[i];
    int l = 0;int r = len-1;
    while(l<=r){//在当前LIS范围内二分查找
        int mid = (l+r)/2;
        if(tail[mid]<x){//目标是在tail中找到第一个>=x的
        //如果序列是非严格上升 改为tail[mid]<=x
            l = mid+1;
        }else{
            r = mid-1;
        }
    }
    //二分结束后l就是第一个>=x的位置
    tail[l] = x;//找到后更新 最后为每一个LIS长度找到相应的最优结尾
    if(l==len)len++;
}
cout<<len<<endl;
```

二分可以用`lower_bound,upper_bound`等STL来写:

本质和上面是一样的

```c++
int len = 0;
for(int i = 0;i<n;i++){
    int x = a[i];
    int pos = lower_bound(tail,tail+len,x)-tail;//直接找到第一个>=x的位置 不需要手写二分
    //注意lower_bound返回的是指针 最后要减去tail 指针相减
    tail[pos] = x;
    if(pos==len)len++;
}
cout<<len<<endl;
```

注意 此时若不是严格上升的 改成`upper_bound`就好了

最后还有一种更好理解的写法:

```c++
int a[n];
vector<int> tail;//这里为空就好
for(int i = 0;i<n;i++){
    cin>>a[i];
}
for(int i = 0;i<n;i++){
    int x = a[i];
    auto pos = lower_bound(tail.begin(),tail.end(),x);
    if(pos==tail.end()){//找不到就追加在已知LIS后面
        tail.push_back(x);
    }else{
        *pos = x;//找到就更新当前长度更优结尾值
    }
}
cout<<tail.size()<<endl;
```

---

### <mark>编辑距离</mark>

A,B是两个字符串，有三种操作：

`1`在A中插入一个字符

`2`删除A中的一个字符

`3`替换A中的一个字符

`将A字符串变成B字符串所需的最小操作次数，就是A，B的编辑距离`

基础代码实现：（二维数组版，比较好理解）

```c++
string a;string b;
int lena = a.size();int lenb = b.size();//先确定两者长度
vector<vector<int>> dp(lena+1.vector<int>(lenb+1,0));
//dp[i][j]表示将a的前i个字符（子字符1）转换为b的前j个字符（子字符2）所需的最少操作次数
//最终得到的dp[lena][lenb]就是答案
for(int j = 0;j<=lenb;j++){
    dp[0][j] = j;//若a为空字符串，就是要插入j次
}
for(int i = 0;i<=lena;i++){
    dp[i][0] = i;//若b是空字符串，就需要a删除i次
}
for(int i = 1;i<=lena;i++){
    for(int j = 1;j<=lenb;j++){//遍历所有子情况
        if(a[i-1]==b[j-1]){//若两个字符串尾部相同
            dp[i][j] = dp[i-1][j-1];//当前编辑距离就等于前一次的了哦（即分别去掉两个串相同的那个字符）
        }else{
            dp[i][j] = min(min(dp[i-1][j]+1,dp[i][j-1]+1),dp[i-1][j-1]+1);//在插入，替换，删除三种操作中取最小的
        }
    }
}
cout<<dp[lena][lenb]<<endl;
```

进阶代码（优化）：（一维数组版）

写成函数形式，暂时理解不了就当黑盒先使用吧，最多也只能处理几千字符的文本

```c++
int EditDistance(string a,string b){
    int lena = a.size();
    int lenb = b.size();
    if(a==b)return 0;
    if(lena>lenb){//确保a是较短的字符，节省空间
        swap(a,b);
        swap(lena,lenb);
    }
//dp[j]表示在当前行中，将a的前i个字符转换为b的前j个字符的编辑距离
    vector<int> dp(lenb+1);
//初始化第0行，表示空字符串转换为b的前j个字符的编辑距离
    for(int j = 0;j<=lenb;j++){
        dp[j] = j;
    }
    for(int i = 1;i<=lena;i++){//表示a的前i个字符
        //prev表示"上一行左边"，即dp[i-1][j-1]
        int prev = dp[0];
        dp[0] = i;//表示i个字符的a转换为0个字符的b的编辑距离
        for(int j = 1;j<=lenb;j++){
            int temp = dp[j];//保存i个字符的a转换为上一个j的distance，类比dp[i-1][j]
            if(a[i-1]==b[j-1]){
                dp[j] =  prev;
            }else{
                dp[j] = min(min(dp[j]+1,dp[j-1]+1),prev+1);//dp[j-1]就类比二维时dp[i][j-1]
            }
            prev = temp;
        }
    }
    return dp[lenb];
}
```

---

### <mark>二分法查找</mark>

复杂度：nlog(n)?

- 标准二分：用于查找`有序`序列中的某个target，（是一次查询）

```c++
vector<int> arr;
int left = 0;int right = arr.size();
while(left<=right){
    int mid = (left+right)/2;
    if(arr[mid]==target)return mid;//找到就返回位置
    if(arr[mid]<target){
        left = mid+1;//目标在右边就向右移动左边界
    }else{
        right = mid-1;//反之向左移动右边界
    }
}
return -1;//没找到就返回-1
```

一般来说，查找**整数**值时，可以用

```c++
while(left<=right){
    //...
}
```

但是对于**浮点数**来说，由于精度问题，一般用

```c++
for(int i = 0;i<100;i++){//不断迭代，控制精度
    //...
}
```

- 与导弹例题结合，直接上例题：（对每个导弹多次查询）

![导弹拦截](./images/屏幕截图%202025-11-17%20210510.png)

- 由于题目的导弹数量n可能到达1e5，需要用`二分法：`

        首先求最长不上升子序列：

```c++
int heights[n];//初始化所有导弹的高度；
vector<int> tail1;
//tail1[i]表示长度为i+1的不上升子序列的最后一个元素的最大值！
//因为若想让整个不上升子序列最长，末尾的元素要尽可能大，这样才可能在后面排更多元素
//由tail1的定义可知，tail1本身是严格降序的
for(int i = 0;i<n;i++){//对于heights中的每个元素
    int left = 0;
    int right = tail1.size();
    while(left<right){
        int mid = (left+right)/2;//在tail1中寻找第一个小于heights[i]的元素
        if(tail1[mid]<heights[i]){
            //如果找到，那么再往tail1的左边再看看有没有更大的元素小于heights[i]，因为我们需要找的是第一个小于heights[i]的
            right = mid;
        }else{
            //如果没找到，往tail1右边更小的地方找
            left = mid+1;
        }
    }
    if(left==tail1.size()){//左边界到tail1最小值都仍没找到比heights[i]更小的
        tail1.push_back(heights[i]);//直接附加在后面
    }else{//若找到tail1中第一个比heights[i]小的元素
        tail[left] = heights[i];//为了得到最长不上升子序列，让tail1中每一个元素更大！
    }
}
int max_lis = tail1.size();//得到最长不上升子序列
```

- 总结一下上面：

        就是遍历heights的所有元素，根据条件，要么直接夹在tail1后面来延长序列，要么替换掉tail1中的元素使其能够在之后延申得更长.

tail1最后的size就是所求序列的长度

- 再依据`Dliworth theory`算最长上升子序列

```c++
//把tail[mid]<heights[i]改成tail[mid]>=heights[i]即可
```



---

### <mark>贪心</mark>



---



### <mark>差分</mark>

差分可以先理解为`前缀和`的`逆过程`

- 前缀和：给定数组`a`,需我们创建数组`presum`
  其中`presum[i]=a[1]+a[2]+..+a[i]`,用于计算区间和

- 差分：
  将给定的数组`a`视为一个`presum`,创建一个数组`b`
  使得`a[i]=b[1]+b[2]+..+b[i]`,数组b就是a的差分

定义差分数组：

`chafen[i] = a[i]-a[i-1]`

应用：

`将对一个数组区间修改的操作，转化为对其差分数组两个单点的修改操作`

eg：

需要对数组`a`的区间`[l.r]`上的每一个元素都加上`c`

```c++
//进行两个单点操作即可
chafen[l] = chafen[l]+c;
chafen[r+1] = chafen[r+1]-c;
```

注意，修改后要对差分数组求一次**前缀和**，进行还原，作为新的修改后的数组`a`

---

### <mark>"实时"差分</mark>

传统差分VS实时差分:

| 场景     | 传统差分   | "实时"差分       |
| ------ | ------ | ------------ |
| 需要全部结果 | ✅适合    | ❌浪费(只关心当前结果) |
| 只需当前结果 | ❌多余    | ✅完美匹配        |
| 需要中途判断 | ❌不方便   | ✅实时可用        |
| 空间使用   | 需要结果数组 | 只需差分数组       |

适用场景：

需从左到右顺序处理；

当前影响后续；

区间修改；

可能提前结束；



**模板**:

```c++
vector<int> diff(n+2);//差分数组空间稍微开大一点
int current = 0;//当前累计值(实时值)
for(int i = 1;i<=n;i++){//遍历每个位置
    current += diff[i];//current作为全局变量，此时就是当前位置的值！
    //使用current作为当前位置的值，做相应判断和处理...
    //...
    diff[l] += val;
    diff[r+1] -= val;//进行对应区间修改
    if(对当前立即生效){
        current += val;//由于diff只对将来位置的值产生影响，有时需要给current也+val
    }
}
```

eg:

![实时差分例题](./images/屏幕截图%202025-12-05%20151447.png)

```c++
#include<bits/stdc++.h>
using namespace std;
int main(){
    int t;
    cin>>t;
    while(t--){
        int n,k;
        cin>>n>>k;
        string s;
        cin>>s;
        vector<int> condition(n+1);
        for(int i = 0;i<=n-1;i++){
            condition[i+1] = s[i]-'0';
        }
        vector<int> cf(n+1,0);//差分数组
        int flips = 0;//翻转次数
        bool possible = true;
        for(int i = 1;i<=n;i++){
            flips += cf[i];//此刻flips就是当前灯的对应累计翻转次数
            int current = condition[i]^(flips%2);//初次接触位运算哈
            if(current==1){
                if(i+k-1>n){//注意是i+k-1！！！
                    possible = false;
                    break;
                }
                cf[i]++;//进行区间修改
                if(i+k<=n){
                    cf[i+k]--;
                }
                flips++;//当前结果立即生效
            }
        }
        if(possible){
            cout<<1<<endl;
        }else{
            cout<<0<<endl;
        }
    }
    return 0;
}
```

---



### <mark>二维数组差分</mark>

标准模板：

```c++
#include<bits/stdc++.h>
using namespace std;
int main(){
    int n,m,q;//n*m的数组，q次操作
    cin>>n>>m>>q;
    //原数组
    vector<vector<long long>> a(n+5,vector<long long>(m+5));
    for(int i = 1;i<=n;i++){
        for(int j = 1;j<=m;j++){
            cin>>a[i][j];//初始化原数组
        }
    }
    //差分数组
    vector<vector<long long>> di(n+5,vector<long long>(m+5,0));
    for(int i = 1;i<=n;i++){
        for(int j = 1;j<=m;j++){
            di[i][j] = a[i][j]-a[i-1][j]-a[i][j-1]+a[i-1][j-1];//初始化差分数组
        }
    }
    while(q--){//进行q次操作
        int x1,y1,x2,y2;
        long long k;
        cin>>x1>>y1>>x2>>y2>>k;
        di[x1][y1]+=k;
        di[x2+1][y1]-=k;
        di[x1][y2+1]-=k;
        di[x2+1][y2+1]+=k;
        
    }
    vector<vector<long long>> re(n+5,vector<long long>(m+5,0));//求一次前缀和，还原差分数组
    for(int i = 1;i<=n;i++){
        for(int j = 1;j<=m;j++){
            re[i][j] = di[i][j]+re[i-1][j]+re[i][j-1]-re[i-1][j-1];
        }
    }
    for(int i = 1;i<=n;i++){
        for(int j = 1;j<=m;j++){
            cout<<re[i][j]<<" ";//输出操作后的新数组
        }
        cout<<endl;
    }
    return 0;
}
```

eg：

![二维数组差分例题](./images/屏幕截图%202025-11-09%20215629.png)

```c++
#include<bits/stdc++.h>
using namespace std;
int main(){
    int n,m;
    cin>>n>>m;
    //int gezi[n+5][n+5] = {0};//这个只会把第一行第一列初始化为0！！！
    vector<vector<int>> gezi(n+5,vector<int>(n+5,0));
    for(int i = 0;i<m;i++){//直接将gezi数组视为其自身的差分数组，进行处理
        int x1,y1,x2,y2;
        cin>>x1>>y1>>x2>>y2;
        gezi[x1][y1]++;//***
        gezi[x1][y2+1]--;//***
        gezi[x2+1][y1]--;//***
        gezi[x2+1][y2+1]++;//二维差分的处理
    }
    vector<vector<int>> presum(n+5,vector<int>(n+5,0));//进行还原，计算差分数组的前缀和
    for(int i = 1;i<=n;i++){
        for(int j = 1;j<=n;j++){
            presum[i][j] = gezi[i][j]+presum[i-1][j]+presum[i][j-1]-presum[i-1][j-1];
        }
    }
    for(int i = 1;i<=n;i++){
        for(int j = 1;j<=n;j++){
            cout<<presum[i][j]<<" ";
        }
        cout<<endl;
    }
    return 0;
}
```

细节注意二维数组的初始化哦~

由于gezi数组初始化全为0，因此不必定义创建差分数组，其本身就可以视为其自身的差分数组



---



### <mark>DFS深度优先搜索</mark>

(Depth-first search)

**回溯算法**普通模板：

```c++
return_type dfs(参数){
    //终止条件
    if(达到终止条件){
        处理结果;
        return 对应结果;
    }
    //遍历所有选择
    for(每个可能的选择){
        //做出选择
        标记状态改变；
        //递归进入下一层
        dfs(新的参数);
        //回溯到之前的状态，来进行其他选择
        恢复状态;
    }
    return 对应结果;
}
```

eg：

![走方格](./images/屏幕截图%202025-12-05%20140621.png)

```c++
#include<bits/stdc++.h>
using namespace std;
const int dx[3] = {0,1,-1};
const int dy[3] = {1,0,0};//每次可以向上，左，右走一步，此为对应坐标的增加值
int dfs(int x,int y,int step,int n,vector<vector<int>>& visited,int offset){//step表示已经走过的步数，若达到n，dfs就结束了
//visited前加"&"是因为要在函数内部改变实际的visited的值，要引用一下
    if(step==n){
        return 1;//走到头，记为1种方法
    }
    int total = 0;
    for(int i = 0;i<3;i++){//每次都有三种选择，进行遍历
        int nx = x+dx[i];
        int ny = y+dy[i];//更新进行当前选择后的新坐标
        if(nx<-n || nx>n || ny<0 || ny>n){
            continue;//如果超出边界，跳过并进行下一个选择
        }
        if(visited[nx+offset][ny]){
            continue;//如果新坐标是塌陷的，不能走，跳过并进行下一个选择
        }
        visited[nx+offset][ny] = true;//将能走到的新坐标标记为塌陷，下次不能走了
        total += dfs(nx,ny,step+1,n,visited,offset);//以这个选择为基点，递归累加所有走法
        visited[nx+offset][ny] = false;//回溯到基点前的状态，搜索其他选择是否可行
    }
    return total;
}
int main(){
    int n;
    cin>>n;
    int offset = n;//偏移法
    vector<vector<int>> visited(2*n+1,vector<int>(n+1,false));//由于有负数横坐标
  //利用offset做一个偏移，即将0+offset视为原点，0视为最左边的点
    visited[0+offset][0] = true;//起始点直接标记为已经走过的状态
    int result = dfs(0,0,0,n,visited,offset);
    cout<<result<<endl;
    return 0;
}
```

虽说方格无限大，但是能走的步数是有限的，那么最大方格其实也就确定为有限的了.



---

### <mark>快速幂</mark>

用来计算类似`3^100000000000`这种东西

把`3*3*3*3*3.....*3`转变成`9*9*9*9..9`.....

总之就是把乘法任务两两打包，指数级减少操作次数

`核心思想`：

能把底数价值翻倍打包就一直先打包（来降低指数次数）

直到指数变为奇数，就将翻倍后的新底数乘上result

```c++
long long fastpower(long long base,long long exponent){
    //base,exponent分别表示底数和指数
    long long result = 1;
    while(exponent>0){
        if(exponent%2==1){//不能再直接打包了
            result *= base;//若指数是奇数就先单独乘上一个底数
        }
        base = base*base;//把底数两两打包,能打包就一直打包
        exponent = exponent/2;//因此指数也要减半
    }
    return result;
}
```

---

### <mark>埃式筛(素数)</mark>

筛到一个素数，那它的倍数就全部都是合数

筛到合数，直接continue跳过进行下一轮

```c++
const int n = 1000000;//测试数据范围
bool st[n+1];//标记每个数，false为素数，true为合数
vector<int> primes;//存储所有素数
fill(st,st+n+1,false);//初始全为素数
for(int i = 2;i<=n;i++){
    if(st[i]){
        continue;
    }
    primes.push_back(i);//不是合数就插入素数里了
    if((long long)i*i>n)continue;//用ll防止溢出
    for(long long j = (long long)i*i;j<=n;j += i){
        st[j] = true;//该素数的倍数均为合数
    }
}
```

若追求极致高效，可以**只处理奇数**，因为偶数除了2都不是素数;

---

### <mark>欧拉筛(线性筛)</mark>

> 基于埃式筛 发现有些合数会被它的不同因子筛去多次
> 
> 因此还有优化空间
> 
> 让每个合数只被它最小的因数筛去
> 
> 达到线性的复杂度

```c++
vector<int> primes;
bool st[N];//false为素数 true为合数
fill(st,st+n+1,false);//初始话全部标记素数
for(int i = 2;i<=n;i++){
    if(st[i])continue;
    primes.push_back(i);
    for(auto x:primes){//枚举已经筛出的素数
        if(i*x>n)break;//超出范围就终止
        st[i*x] = true;//素数的倍数标记为合数
        if(i%x==0)break;//代码核心 保证线性性质
    }
}
```

关于`i%x==0`:

因为是从小到大枚举所有已经筛出的素数x;

当i%x==0的时候 x就是最小质因子 此时break就好了;

---

### <mark>区间筛</mark>

> 适合找区间[l,r]之间的所有素数 
> 
> 其中l，r很大 但区间范围其实并不大



---

### <mark>逆康托展开</mark>

这里用`求第m小的排列`为例子;

由不重复的数字`1-n`组成的所有排列中，按`字典序`从小到大求出`第m小`的排列:

> 以1,2,3,4组成的排列为例              (字典序)
> 
> - 1开头的排列-->(4-1)!=6种           |(小)
> 
> - 2开头的排列-->(4-1)!=6种           |
> 
> - 3开头的排列-->(4-1)!=6种           |
> 
> - 4开头的排列-->(4-1)!=6种           |(大)
> 
> then，比如求第9小的排列，先转换为0-based=>9-1=8;
> 
> 8/6=1:该排列在第2组,也就是一个2开头的排列;
> 
> 8%6=2,该排列在2开头的排列中的第2小
> 
> (以此类推递归)

```c++
#include<bits/stdc++.h>
using namespace std;
#define ll long long
vector<int> get_permutation(int n,int m){
    //预先做一个1-n排列的可用数字
    vector<int> nums;
    for(int i = 1;i<=n;i++){//注意索引是从0开始
        nums.push_back(i);
    }
    ll k = m-1;//因此要转换成0-based
    vector<int> ans;//到时候用来存储结果
    //接下来从第一位开始,确定排列的每一位
    for(int i = n;i>=1;i--){
        //每确定一个数之前,单独确定阶乘结果(如果直接计算所有阶乘会溢出的)
        ll fact = 1;
        bool overflow = false;
        for(int j = 1;j<=i-1;j++){//计算该位的阶乘
            if(fact>k/j){//判断是否"溢出"，等价于fact*j>k
                overflow = true;
                break;
            }
            fact = fact*j;
        }
        if(overflow){
            ans.push_back(nums[0]);//fact>k,则idx=k/fact=0
            nums.erase(nums.begin());//去掉当前数组及其索引
            //确定第一个数字的时候索引和值相等,后续的话,表示的是当下第几小的数
        }else{
            ans.push_back(nums[k/fact]);
            nums.erase(nums.begin()+k/fact);
            k %= fact; //更新k
        }
    }
    return ans;
}
int main(){
    ll n,m;
    while(cin>>n>>m){
        vector<int> result = get_permutation(n,m);
        int len = result.size();
        for(int i = 0;i<len;i++){
            cout<<result[i];
            if(i!=len-1){
                cout<<" ";
            }
        }
        cout<<'\n';
    }
    return 0;
}
```

计算机一般都是从0开始的,理解不了就记住一般都要转换为0-based

---

### <mark>排序+去重</mark>

- 方法一:利用set(边读入边处理)
  
  ```c++
  set<int> b;//先创建一个集合
  for(int i = 0;i<n;i++){
    int x;cin>>x;
    b.insert(x);
  }
  vector<int> a(b.begin(),b.end());//这样,a就是一个排序且去重的数组了
  ```

- 方法二:利用unique函数(适合已经有vector的情况)
  
  ```c++
  sort(a.begin(),a.end());//先排好序
  a.erase(unique(a.begin(),a.end()),a.end());//再利用unique,并结合erase完成去重
  //此时vector<int> a就完成去重和排序了
  ```
  
  

---

## <<语法>>

---

### <mark>位运算</mark>

- 优先级最低,建议加括号;

- 左移:`x<<k = x*(2^k)`;

- 右移:`x>>k = x/(2^k)`;(向下取整,取不大于结果的最大整数)

---

### <mark>异或</mark>

> 先将数值转换为二进制
> 
> 然后对每一位进行异或
> 
> 相同为0
> 
> 不同为1
> 
> 异或符号^是可以直接使用的 不需要自己实现

- 1^1=0

- 0^0=0

- 1^0=1

性质:

- a^b=b^a;(交换律)

- (a^b)^c=a^(b^c);(结合律)

- a^b^b=a^(b^b)=a^0=a;(与0异或 结果等于本身)

应用:

- 变量交换

```c++
a=3;b=4;
a=a^b;
b=a^b;
a=a^b;
cout<<a<<b<<endl;
```

- 排除偶次重复

在一个整数数组中 只有一个不重复的数字 其余均出现偶数次 找出不重复的那个数字

```c++
int ans = 0;
for(int i = 0;i<arr.size();i++){
    ans ^= arr[i];//偶数次的都会被抵消完 ans保持为0
    //直到遇到不重复的数字 ans保持那个不重复的数
}
return ans;
```

---



### <mark>cin&cout </mark>

1.输入cin：

混合输入字符串和数字要注意ignore缓冲区：

```c++
int a;
string str;
cin>>a;
cin.ignore.();//清空缓冲区，否则无法正常使用getline
getline(cin,str);
//注意，cin中不能使用endl换行符；
```

2.输出cout:

```c++
int a;
cin>>a;
cout<<a;
int s[n];
for(int i = 0;i<n;i++){//在需要高性能的环境中
    //cout<<s[i]<<endl;
    cout<<s[i]<<'\n';//是循环中更好的换行方式
}
```

3.关闭输入输出同步流，提升程序效率

```c++
ios::sync_with_stdio(false);
cin.tie(0);
cout.tie(0);
```

4.输出小数

```c++
cout<<fixed<<setprecision(n)<<double_num<<endl;//保留n位小数
```



---



### <mark>类型转换</mark>

首先方便起见，初学使用`using namespace std;`

```c++
//字符串-->数值
string str = "123";
int num1 = stoi(str);
double num2 = stod(str);
float num3 = stof(str);
long long num4 = stoll(str);
//数值-->字符串
string str1 = to_string(num1);
```

注意`stoi()`这种的参数需要是`字符串`,不能直接转换单个字符哦.

对于单个字符的情况：

```c++
int num = str.back()-'0';//也能完成对最后一个元素的转换
```



---

### <mark>数学函数</mark>

| 数学函数                   | 库中对应函数语法       |
|:----------------------:|:--------------:|
| f(x)=lnx               | log(x)         |
| f(x)=lgx               | log10(x)       |
| f(x)=\|x\|(int,double) | abs(x),fabs(x) |
| f(x)=向下取整              | floor(x)       |
| f(x)=向上取整              | ceil(x)        |
| f(x)=$\sqrt(x)$        | sqrt(x)        |
| 取大                     | max(a,b)       |
| 取小                     | min(a,b)       |

注意：*三角函数*在库中都以<u>弧度制</u>表示，即传入的参数应该是$\pi$ 之类的，而不是180°之类的。

---

### <mark>++i&i++的区别</mark>

注：理解两者的区别对于提高<u>代码效率</u>非常重要！！！

1.++i：

先将i的值加一，再返回i.

2.i++:

 先返回i本身的值，再将i加一.

---

### <mark>"&"引用</mark>

引入一个重要的符号：**<u>&</u>**

在c++中，&除了有取地址的作用外，还可以**表示引用**！

```c++
//&表示引用的基本含义
//&引用的本质就是给变量取别名
int a = 10;
int &b = a;// b是a的引用（别名）
b = 20;// 现在a也变成了20
cout << a;// 输出20
```

主要用于函数的参数部分：

```c++
//一.要通过函数修改外部变量
void func(变量类型 &变量名){}//类似*，但更方便
//二.不修改外部变量且是简单类型，不考虑性能
void func(变量类型 变量名){}
//三.不修改外部变量，但数据类型大，性能要求高
void func(const 变量类型 &变量名){}//能避免拷贝
```

**总之，**

**问自己：我需要修改这个参数吗？**

* **要修改** → 用 `&`

* **不修改** → 继续问：这个参数大吗？
  
  * **大**（结构体、字符串、数组）→ 用 `const &`
  
  * **小**（int、double、char）→ 什么都不加
    
    

---



### <mark>fgets(c语言)</mark>



---

### <mark>struct结构体</mark>

是一种`自定义数据类型`

基本结构：将多个**不同类型变量组合**在一起，形成一个逻辑上的整体

```c++
// 定义结构体
struct Student {//定义Student是一种数据类型！！
    string name;// 姓名
    int age;// 年龄  
    double score;// 分数
};//别忘了有分号！！！
```

然后，可以在主函数中使用`Student`这个数据类型

例如`Student Xiaoming`;

那么如何访问一个结构体中的各个成员？

答案是`用“.”来访问`.

```c++
Student Xiaoming;
Xiaoming.name = Xiaoming;
Xiaoming.age = 18;
Xiaoming.score = 100.0;
```

当然也可以直接按结构体内的顺序初始化：

```c++
Student a = {Xiaoming,18,100.0};
```

或指定成员初始化：

```c++
Student a = {.name = Xiaoming,.age = 18,.score = 100.0};
```

---

### <mark>bitset</mark>

> 可以看为更省内存的bool数组 值为0或1
> 
> 局限是 编译时大小必须是常量 可以预先开好足够空间

```c++
bitset<100> b1;//大小为100的bitset 默认值全为0
b1.set();//将其全部设为1
b1.reset();//全部设为0
b1.flip();//0变成1 1变成0
//括号内加数字i的话 就是对第i位进行相应操作
b1.count();//返回1的个数
b1.test(i);//测试第i位是否为1 会检查越界 返回是bool值
```

---

### <mark>fill,memset函数</mark>

> memset一般只用于C风格数组或者结构体,或者通过new的动态数组;
> 
> fill可用于STL;
> 
> 但两者都不能用于bitset;

```c++
fill(起始迭代器，结束迭代器，填充值)；
```

即不管序列原来每个元素的值是多少，`fill函数`能够将范围内的所有元素值都一律变为`填充值`.

```c++
fill(arr.begin(),arr.end(),10);//将arr全部变为10
```

`memset`主要用于**快速清空**或**初始化**很大的内存空间,比较高效.

```c++
memmset(需要填充的内存块的指针,int ch,要设置的字节数);
memset(arr,0,sizeof(arr));//数值全变为0
memset(str,0,sizeof(str));//字符串全变为空!!!
memset(str,'a',sizeof(str));//字符串全变为字符a
memset(flags,true,sizeof(flags));//布尔值全变为true
//注意，对于数值型，只能修改为0或-1！！！！
```

---

### <mark>lower_bound/upper_bound函数</mark>

使用前记得先将范围序列**排序**哦

```c++
sort(arr,arr+n);
```

这两个函数是基于`二分`的思想写的，可以直接调用

用于**查找**序列中的值，区间依旧左闭右开哦

`lower_bound(arr,arr+n,value);`返回第一个**大于等于**value元素的位置;

`upper_bound(arr,arr+n,value);`返回第一个**大于**value元素的位置;

若找不到，都会返回last这个位置（last是序列最后一个元素的再下一个位置）

```c++
int a[n];//初始化省略了
sort(a,a+n);//记住一定要先排序
auto left = lower_bound(a,a+n,1);//auto可以自动判断表达式的类型哦，此处即为指针类型了
auto right = upper_bound(a,a+n,1);
int cnt = right-left;//统计1在a中出现次数
```

```c++
auto left = lower_bound(a,a+n,1);
int index = left-a;//获取第一个元素1的具体索引(指针相减)
int value = *left;//获取指针所指的值
```

---



### <mark>sort函数(c++)</mark>

基本形式：

```c++
// 基本形式1：使用默认的升序排序
sort(first, last);
//更通用的形式：比较函数：
sort(first,last,cmp);
```

`first`表示要排序的范围的开始位置，`end`则是结束位置，区间可理解为**左闭右开**.

基本语法&示例：

```c++
#include <bits/stdc++.h>
using namespace std;
int a[n];
for(int i = 0;i<n;i++){
    cin>>a[i];//初始化一个数组，对数组中的元素进行排序
}
sort(a,a+n);//升序排列
//如果是vector
sort(a.begin(),a.end());
//由于要一直排序到索引为n-1的元素，且左闭右开，因此写结束位置为(n-1)+1--->n！
return a<b;//升序
}
```

降序排序比较器`greater<>()`

```c++
#include<functional>
sort(a,a+n,greater<数组值类型>());//这样就会降序排序
```

部分排序`nth_element`

```c++
nth_element(a,a+k,a+n);//升序，挑出a中前k小的元素
nth_element(a,a+k,a+n,greater<>());//降序，挑出a中前k大的元素
```

比较函数：(与c的qsort原理不同)

`bool`返回`true`，sort函数会将`参数a`排在`参数b`前面;

反之`bool`若返回`false`则会把`参数a`排在`参数b`后面;

```c++
bool cmp(int a,int b){
    return a<b;//升序
}

bool cmp1(int a,int b){
    return a>b;//降序
}
```

复杂度：n*log(n);

---

### <mark>swap(交换函数)</mark>

基本语法&示例：

```c++
#include <bits.stdc++.h>//万能头文件
using namespace std;//要用swap的话一定要写std库！！

int x = 5, y = 10;
swap(x, y);//交换基本类型
------------------------------
string s1 = "Hello", s2 = "World";
swap(s1, s2);//交换字符串
------------------------------
int arr[] = {1,2,3,4,5};
swap(arr[0], arr[4]);// 交换第一个和最后一个元素
```

---

### <mark>getline(c++)</mark>

只适用于`string`类型!主要用于读取需要包括`空格`的文本.

```c++
#include <bits/stdc++.h>
using namespace std;
string names;
getline(cin,names);//基本格式，能读取空格，默认读到换行符为止！！
```

自定义分隔符（类似scanf的扫描集）

```c++
#include <bits/stdc++.h>
using namespace std;
string data;
getline(cin,data,',');//读到逗号为止
```

`cin.ignore()`清空混合输入缓冲区.eg:

```c++
int num;
string text;
cin>>num;
cin.ignora();//必须调用，清除缓冲区的换行符
getline(cin,text);
```



---

### <mark>set容器(c++)</mark>

介绍：

`set`是一个有序的关联容器，包含`唯一键`(元素不允许重复)的集合

特性：

元素唯一性；自动排序(升序)；不可修改元素(均为const)；查找效率高(logn)

用法：

```c++
set<变量类型> 变量名；
//eg:
set<int> myset;
myset.insert(1);
myset.insert(2);
myset.insert(3);
myset.insert(1);//因为1已经有了，这个1就无效了
//可用于统计集合的实际元素个数
int len = myset.size();
myset.erase(x)//删除值为x的元素
myset.find(x)//查找是否存在x元素，返回相应迭代器
cout<<*myset.begin()<<'\n';//输出第一个元素(最小)
cout<<*myset.rbegin()<<'\n';//输出最后一个元素(最大)
```

```c++
//利用其自动升序排序的原理，我们可以用set同时完成去重和排序！！！
set<type> setname(iterator first,iterator last);
//这个构造函数会遍历[first,last)的所有元素并插入到set中
```



---

### <mark>string(c++)</mark>

string是一个封装了**字符数组**的类，自动管理内存。专门存放**字符序列**.
string类型的变量，**下标索引也是从0开始**。



首先注意`string`和普通数组`a[n]`的区别：

空的`string`最好使用`+=`或`.push_back()`来添加元素;

若想如`a[n]`一样通过`for`循环用`a[i]`赋值，则需要先`resize()`!!!!



- 特性1：变量之间可以**直接相加+**，自动管理内存哦！

```c++
string s1 = "Hello";
string s2 = "World";
string s3 = s1 + " " + s2;//直接使用+运算符，也可以用于循环不断增加！
```

- 特性2：**初始化**较便利

```c++
string s1 = "Hello";//C风格字符串字面量
string s2 = 'A';//错误！不能直接存放单个字符
string s3(1,'A');//正确！创建包含1个字符'A'的字符串
string s3 = "A";//但可以用字符串字面量
string s4 = "中文";//可以存放中文字符（在合适的编码下）
string s5 = "Hello\x20World";//可以包含转义字符
string s6 = ""; //空字符串
```

（但注意，（1）string类型也是**不能由cin直接输入空格和换行符**的！！！需要使用一个getline()哦（2）混合输入时，要在合适位置使用cin.ignore()清空缓冲区）

- 特性3：运算符重载，可直接比较**字典序**大小

```c++
string s1 = "hello";
string s2 = "world";
if(s1>s2){
    //.....
}
```

- 特性4：丰富的成员**函数**(下面不是所有的哦)

```c++
string str = "Hello World";

int len = str.size();//len = 11
cout<<str.find("World");//--->6
str.push_back('!');//str = "Hello World!",用于添加单个字符
str.pop_back();//删除最后一个字符
str.append(" world");//功能更强大，可追加多字符
str.append(100,'!');//添加100个感叹号哦

str.front();//访问第一个元素
str.back();//访问最后一个元素
str.find_first_of("aeiou");//查找第一个出现的元音字母的索引位置
str.find_last_of("aeiou");//查找最后一个出现的元音字母的索引位置
str.empty();//检查字符串是否为空，空返回true，非空false
cout<<str.substr(提取的起始索引位置，提取字符数量)；//若提取数量不写，则默认提取到末尾哦
string str1(str);//将str的内容拷贝到新创建的str1

str.clear()//清空
str.erase(n,m)//删除从索引为n开始，往后共m个字符
str.erase(str.begin()+1);//删除单个字符
str.erase(str.begin()+2,str.begin()+5)//删除一个范围

reverse(str.begin(),str.end());//反转字符串
str.replace(起始索引，需替换长度，"新内容")；//新字符串长度可不同

str.reserve(n)//不改变字符串大小，只分配内存容量
str.resize(n)//分配空间的同时也改变字符串大小
```

注意：
`.end()`和`.begin()`是一对：

表示指向最后一个元素的下一个位置，和指向第一个元素

`.front()`和`.back()`是一对：

表示第一个和最后一个元素，可直接引用



---

### <mark>map(c++)</mark>

对插入的**键值对**自动**按键升序**排序

```c++
#include<map>
map<键类型,值类型> 变量名;
//添加键值对
map<int,string> student;
student[1] = "jaychou";
student.insert({2,"neyo"});
//查找访问
//find():若查找发现有这个键，it就是指向该元素的迭代器
//如果没找到,it会指向.end()
auto it = student.find(键);
if(it!=student.end()){
    cout<<it->second;//输出对应值
}
//删除元素
//erase()会将这整个键值对都删掉
student.erase(键);
```

利用**迭代器遍历**map中的键值对:
因为不一定知道起始的键 也不知道键之间的间隔 也不知道末尾的键

```c++
for(auto it = m.begin(),it!=m.end(),it++){
    cout<<it->first<<" "<<it->second;//不是成对的值,而是单个值的时候,需要用*it
}
//这里it是迭代器 要用->来表示具体的键和值
for(const auto& item:m){//总之就是for(const auto& it:container)来遍历
    cout<<item.first<<" "<<item.second;
}
//这里item是一个值,用.来表示具体的键和值
```

值要用.
迭代器要用->

补充：对于频率统计的问题,`map`和`unordered_map`都可以直接`m[键]++`,都会自动初始化该键的值为0;

---

### <mark>unordered_map</mark>

一.语法：

`unordered_map<键类型，值类型> 变量名;`

eg:

```c++
//基本初始化
unordered_map<int,string> student_id;// 学号→姓名
unordered_map<string,double> product_price;//产品名→价格
unordered_map<ll,ll> freq;// 数值→出现次数
//插入键值对
scores["Alice"] = 100;//Alice为键，100为其对应的值
scores.insert({"Bob",60});//插入一个键值对
//访问元素
cout<<scores["Alice"];//输出的是100
cout<<scores["David"];//自动创建{"David":0}并输出0
```

```c++
//函数
if(scores.count("Alice")){
    //键存在
}
scores.erase("Alice");//删除键为Alice的元素
```

二.特性：

1.无序性。

相对map来说，map是有序的键值对，但访问速度没有哈希表快速。元素的存储顺序与插入顺序无关，遍历时顺序也不确定。

2.自动初始化。

eg：

```c++
unordered_map<int,int> m;
cout<<m[5];//输出0,同时自动创建{5:0}
```

即，即使哈希表的一些键值对还没有被初始化时，此时若直接输出或者访问某个键，会自动创建键值对，并初始化键的值为0。

三.用法：

1.统计频率等

---



### <mark>pair(c++)</mark>

作用：
可以把两个值打包成一个对象（一个变量名，类似成为一个组合），两个值可以是不同的数据类型

```c++
pair<类型1，类型2> 变量名；
```

用法：

```c++
//方式1:先声明后赋值
pair<string,int> p1;
p1.first = "Bob";//这里first，second是pair专用的访问元素方法
p1.second = 80;
// 方式2:声明时直接初始化
pair<string,int> p2("Cathy", 88);
//方式3:表达一系列pair对，例如n个学生的姓名以及对应成绩
vector<pair<string,int>> student(n);
for(int i = 0;i<n;i++){
    cin>>student[i].first>>student[i].second;//对其进行输入
}
//方式4:初始化pair序列
vector<pair<int,int>> biggest(m,{0,0});//表示有m个{0，0}对序列
```

---

### <mark>priority_queue</mark>

> 一种能够随时`插入新数据`，并且随时知道`最大值或者最小值`，并且随时`删除`当下`最大值或最小值`的容器(优先队列)

- 大顶堆(默认):`priority_queue<int> pq;`(获取,删除最大值)

- 小顶堆:`priority_queue<int,vector<int>,greater<int>> pq;`(获取,删除最小值)

- 常用方法:
  
  ```c++
  int value = pq.top();//获取最大/小值
  pq.pop();//删除最大/小值
  pq.push(x);//插入新的值x
  ```

---

### <mark>stack栈</mark>

> 像一个只有一个开口的管道，
> 只能从顶部存入或者取出东西,
> `先进后出`

```c++
#include <stack>
stack<int> s;
//新添加的元素始终在栈顶
s.push(1);//[1]
s.push(2);//[1,2]
s.push(3);//[1,2,3]
int x = s.top();//x=3
//只能从栈顶逐个删除元素
s.pop();//[1,2]

```

---

### <mark>queue队列</mark>

> 像一个有上下开口的管道,
> 先存入的元素会先出来
> `先进先出`

```c++
queue<int> q;
q.push(1);//[1]
q.push(2);//[1,2]
q.push(3);//[1,2,3]
int x = q.front();//x=1
int y = q.back();//y=3
//弹出最先插入的元素
q.pop();//[2,3]

```

---

## <<细节问题>>

---

### <mark>字符串需主动添加'\0'(NULL)的情况</mark>

(1)使用<u>循环对逐个字符赋值</u>，构造字符串时：

```c++
char dest[10];
for(int i=0; i<3; i++) {
    dest[i] = source[i];
}
dest[3] = '\0';  // 必须手动添加****
```

(2)<u>手动逐个字符赋值</u>，构造字符串时：

```c++
char str[10];
str[0] = 'H';
str[1] = 'i';
str[2] = '\0';  // 必须手动添加****
```

(3)使用<u>非字符串函数</u>操作时：

```c++
char str[10];
memcpy(str, "Hello", 5);  // 只复制5个字符，不包括\0
str[5] = '\0';  // 必须手动添加****
```

---

### <mark>二维数组的初始化</mark>

目标：初始化`a[n][n]`的每个元素都为0

错误示例：

```c++
int a[n][n] = {0};//这样只会让第一行第一列为0
```

正确示例：

```c++
int a[n][n];
for(int i = 0;i<n;i++){
    for(int j = 0;j<n;j++){
        a[i][j] = 0;    
    }
}
```

```c++
//或者使用vector
vector<vector<int>> a(n,vector<int>(n,0));
```

---

### <mark>栈溢出</mark>

在oj或者算法竞赛上，数组在合适情况下就**开在全局**，或者使用`vector`;防止发生栈溢出(但实际开发中一般不推荐使用)

```c++
const int MAXN = 200005; 
long long len[MAXN];//开在全局 
int main(){
    //... 
    int n; 
    cin>>n; 
    vector<long long> len1(n);//或者使用vector 
}   
```

---

### <mark>vector</mark>

```c++
vector<int> graph[N];//写图论题的时候,这样写表示N个vector<int>
vector<vector<int>> graph(N);//上面的写法更好
```

> vector<>是一种数据结构，用`[]`就表示`vector<>`这种类型的数组;
> 用`()`就表示vector的一种构造元素个数的函数

---
