#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
//树上差分需要LCA,先写最近公共祖先
const int N = 100010;
const int LOG = 20;
int n,k;
int diff[N];//差分数组
int dep[N];//每个点的深度
int fa[N][LOG+1];//第i个节点的2^k次级父亲
vector<int> tree[N];//邻接表标准写法,注意不是"()"而是"[]"!
int ans = 0;

void dfs1(int u,int f){//预处理深度
	fa[u][0] = f;
	dep[u] = dep[f]+1;
	for(int i = 1;i<LOG+1;i++){
		fa[u][i] = fa[fa[u][i-1]][i-1];
	}
	for(int v:tree[u]){
		if(v==f)continue;
		dfs1(v,u);
	}
}

int lca(int x,int y){//找公共祖先
	if(dep[x]<dep[y]){
		swap(x,y);
	}
	for(int i = LOG;i>=0;i--){
		if(dep[fa[x][i]]>=dep[y]){
			x = fa[x][i];
		}
	}
	if(x==y)return x;
	for(int i = LOG;i>=0;i--){
		if(fa[x][i]!=fa[y][i]){
			x = fa[x][i];
			y = fa[y][i];
		}
	}
	return fa[x][0];
}

void dfs2(int u,int f){//差分回溯
	for(int v:tree[u]){
		if(v==f)continue;
		dfs2(v,u);
		diff[u]+=diff[v];
	}
	ans = max(ans,diff[u]);
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cin>>n>>k;
	for(int i = 0;i<n-1;i++){
		int x,y;cin>>x>>y;
		tree[x].push_back(y);
		tree[y].push_back(x);
	}
	dfs1(1,0);
	while(k--){
		int s,t;cin>>s>>t;
		int w = lca(s,t);
		diff[s]++;
		diff[t]++;
		diff[w]--;
		if(fa[w][0])diff[fa[w][0]]--;
	}
	dfs2(1,0);
	cout<<ans<<endl;
	return 0;
}
