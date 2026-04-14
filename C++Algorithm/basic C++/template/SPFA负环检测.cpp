#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
//SPFA能处理负权边最短路 能检测负环
//SPFA是 只要某个点的当前dist变小了 就用它去更新其他点 而Dijkstra是当前点确定最小 
//才会用它去更新其他点
//在没有负环的图中 从源点到任意点的最短路 最多经过n-1条边
//所以到某个点的最短路 所使用的边数一但大于等于n 就说明有负环
//以下是检测任意负环的代码
struct edge{
	int to;
	ll w;
};
const int N = 2010;
vector<edge> g[N];
int dis[N];
int cnt[N];
bool inq[N];
int n,m;
bool spfa(){
	queue<int> q;
	for(int i = 1;i<=n;i++){//所有点一开始都当作起点
		dis[i] = 0;//为了覆盖整张图 想象一个超级源点s 到每个点的距离都初始化为0
		cnt[i] = 0;
		inq[i] = true;
		q.push(i);//一开始全部入队列 因为要找任意的负环
	}
	//如果是判断是否存在 从某点s可达的负环
	//dis[i]都初始化为inf,inq[i]都都初始化为false
	//dis[s]=0,只需要s先入队列就行 其他都一样
	while(!q.empty()){
		int u = q.front();
		q.pop();
		inq[u] = false;
		for(auto e:g[u]){
			int v = e.to;
			ll w = e.w;
			if(dis[u]+w<dis[v]){
				dis[v] = dis[u]+w;
				cnt[v] = cnt[u]+1;
				if(cnt[v]>=n){
					return true;//有负环
				}
				if(!inq[v]){
					inq[v] = true;
					q.push(v);
				}
			}
		}
	}
	return false;//无负环
}
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	int t;cin>>t;
	while(t--){
		cin>>n>>m;
		for(int i = 1;i<=n;i++){
			g[i].clear();
		}
		for(int i = 1;i<=m;i++){
			int u,v,w;
			cin>>u>>v>>w;
			if(w>=0){
				g[u].push_back({v,w});
				g[v].push_back({u,w});
			}else{
				g[u].push_back({v,w});
			}
		}
		cout<<(spfa()?"YES\n":"NO\n");
	}
	return 0;
}
