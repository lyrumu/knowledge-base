#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
//和Kruskal不同 Prim关注"点" 每次找到距离当前生成树最近的点加入树中
const int N=5010;
const ll INF = 4e18;
ll g[N][N];//邻接矩阵
bool vis[N];//是否已加入树中
ll dist[N];//每个点到当前生成树的最短距离
int main(){
	int n,m;
	cin>>n>>m;
	for(int i = 1;i<=n;i++){
		for(int j = 1;j<=n;j++){
			g[i][j] = INF;//初始每两点间距离都先设置为INF
		}
	}
	for(int i = 1;i<=m;i++){
		int u,v;
		ll w;
		cin>>u>>v>>w;
		g[u][v] = g[v][u] = min(g[u][v],w);//因为是找最小生成树 所以如果有重边 记录最短边权就好了
	}
	for(int i = 1;i<=n;i++){
		dist[i] = INF;
	}
	dist[1] = 0;//从一号点开始找最小生成树呗 其实都一样
	ll ans = 0;
	for(int i = 0;i<n;i++){
		//因为需要连接n个点 就要进行n次循环 每次找到当前距离树最近的点
		int t = -1;
		for(int j = 1;j<=n;j++){
			if(!vis[j]&&(t==-1||dist[j]<dist[t])){
				t = j;//不断找距=距离当前树最近的点
			}
		}
		if(dist[t]==INF){//如果不连通 后面也不用做了 生成不来的
			cout<<"orz"<<endl;
			return 0;
		}
		vis[t] = true;
		ans+=dist[t];
		for(int j = 1;j<=n;j++){//用t更新其他点的dist值
			if(!vis[j]&&g[t][j]<dist[j]){
				dist[j] = g[t][j];
			}
		}
	}
	cout<<ans<<endl;
	return 0;
}
