#include<bits/stdc++.h>
//https://www.luogu.com.cn/problem/P4551
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
const int N = 100010;
vector<pair<int,int>> g[N];
int dist[N];//存储从根节点到i点的边权异或乘积
//then u，v点间路径边权异或乘积就是dist[u]^dist[v];(lca公共路径异或抵消)
int trie[N*31][2];//*31是什么意思？ 2应该就是0或1
int tot = 1;//当前节点(根节点) 写成0可以吗？ 其实只要统一用0或1都行
int n;

void dfs(int u,int fa){//既然是dfs 能确保预处理所有点吗?
	for(auto [v,w]:g[u]){
		if(v==fa)continue;
		dist[v] = dist[u]^w;//预处理得到dist数组
		dfs(v,u);
	}
}

//关于Trie
//每一层表示一个位
//每一条路径表示一个完整对象(字符串 数字)
void ist(int x){//把每个dist[i]按位存进trie
	int p = 1;
	for(int i = 30;i>=0;i--){
		int b = (x>>i)&1;//取这个数的第i位 准备存入trie
		if(!trie[p][b]){
			trie[p][b] = ++tot;
		}
		p = trie[p][b];
	}
}

int que(int x){//查询当前dist[i]能匹配到的最大异或和
	int p = 1;
	int res = 0;//最终xor结果
	for(int i = 30;i>=0;i--){
		int b = (x>>i)&1;
		int want;//dist[i]当前位是1 就希望得到0
		//当前位是0 就希望得到1 这样异或结果最大
		if(b==0)want = 1;
		else want = 0;
		if(trie[p][want]!=0){
			res+=(1<<i);
			p = trie[p][want];//want存在就走向want
		}else{
			p = trie[p][b];//不存在就只能走原路
		}
	}
	return res;
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cin>>n;
	for(int i = 0;i<n-1;i++){
		int u,v,w;
		cin>>u>>v>>w;
		g[u].push_back({v,w});
		g[v].push_back({u,w});
	}
	int ans = 0;
	dist[1] = 0;
	dfs(1,0);
	
	ist(dist[1]);
	for(int i = 2;i<=n;i++){
		int val = que(dist[i]);
		if(val>ans)ans = val;
		ist(dist[i]);//采用一边插入新的idst[i] 一边查询更新最大值
	}
	cout<<ans<<endl;
	return 0;
}
