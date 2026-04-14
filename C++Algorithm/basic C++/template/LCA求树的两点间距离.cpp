#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long

const int N = 100010;
const int LOG = 17;
vector<int> g[N];//邻接表
int dep[N];
int fa[N][LOG];
int n,q;

void dfs(int u,int f){
	fa[u][0] = f;
	for(int v:g[u]){
		if(v==f)continue;
		dep[v] = dep[u]+1;
		dfs(v,u);
	}
}

int lca(int x,int y){
	if(dep[x]<dep[y]){
		swap(x,y);
	}
	int diff = dep[x]-dep[y];
	for(int i = LOG-1;i>=0;i--){
		if(diff>=(1<<i)){
			x = fa[x][i];
			diff-=(1<<i);
		}
	}
	if(x==y)return x;
	for(int i = LOG-1;i>=0;i--){
		if(fa[x][i]!=fa[y][i]){
			x = fa[x][i];
			y = fa[y][i];
		}
	}
	return fa[x][0];
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cin>>n;
	for(int i = 1;i<=n-1;i++){
		int x,y;
		cin>>x>>y;
		g[x].push_back(y);
		g[y].push_back(x);
	}
	cin>>q;
	//以下三步顺序不能写错 否则会出问题
	dep[1] = 0;//（1）
	dfs(1,1);//（2）
	for(int j = 1;j<LOG;j++){//（3）
		for(int i = 1;i<=n;i++){
			fa[i][j] = fa[fa[i][j-1]][j-1];
		}
	}
	while(q--){
		int x,y;
		cin>>x>>y;
		int anc = lca(x,y);
		int dist = dep[x]+dep[y]-2*dep[anc];//记住公式 理解
		//如果是带权值的树 虽然可以用bfs/dfs做
		//如果也用lca预处理来计算两点间距离
		//公式:dist(u,v) = dist(u,root)+dist(v,root)-2*dist(root,lca(u,v))
		cout<<dist<<endl;
	}
	return 0;
}
