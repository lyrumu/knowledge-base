#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
const int N = 200010;
const int LOG = 20;
int n,m,root;
vector<vector<int>> e(N);//邻接表
int dep[N];//每个节点的深度
int fa[N][LOG+1];//表示从节点i向上2^j个的祖先
void dfs(int u,int father){//dfs处理深度
	fa[u][0] = father;
	dep[u] = dep[father]+1;
	for(int v:e[u]){
		if(v==father)continue;
		dfs(v,u);
	}
}
int lca(int x,int y){//LCA
	if(dep[x]<dep[y]){
		swap(x,y);//保证x是较深或与y相同深度的点
	}
	//拉平深度,此后x,y在同一深度
	for(int i = LOG;i>=0;i--){//如果i从0开始不行吗？NO！
	//LCA倍增循环变量必须从大到小跳跃
		if(dep[fa[x][i]]>=dep[y]){
			//如果更深的节点的父亲节点的深度仍然更大，让x不断向上移
			x = fa[x][i];
		}
	}
	if(x==y)return x;//如果此时x==y,说明此前较浅的点就是较深的点的祖先,就是LCA
	for(int i = LOG;i>=0;i--){//i从0开始不行吗？NO！
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
	cin>>n>>m>>root;
	for(int i = 1;i<n;i++){
		int x,y;cin>>x>>y;
		e[x].push_back(y);
		e[y].push_back(x);
	}
	dfs(root,0);//加载深度处理
	for(int j = 1;j<=LOG;j++){
		for(int i = 1;i<=n;i++){
			fa[i][j] = fa[fa[i][j-1]][j-1];
			//节点i的第2^j级父亲=i的2^(j-1)级父亲的2^(j-1)级父亲
		}
	}
	while(m--){
		int x,y;
		cin>>x>>y;
		cout<<lca(x,y)<<endl;
	}
	//从大开始跳，虽然一开始可能跳到太上面甚至0，但是不满足if条件，x没变化，就可以继续跳；
	//若从小开始跳，x一般就会直接网上了，很快就会结束循环
	return 0;
}
