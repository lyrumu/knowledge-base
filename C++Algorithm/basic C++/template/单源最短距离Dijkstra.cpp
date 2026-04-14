#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
//dijkstra算法 适用于边权非负的题目
//计算单源到其他所有点的距离，每次弹出一个点,表示到该点的距离计算完毕
const ll inf = 4e18;
struct edge{
	int to;//连接的节点
	ll w;//权值
};
int n,m,s;
vector<ll> dist;
vector<vector<edge>> g;
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cin>>n>>m>>s;
	g.resize(n+1);
	dist.resize(n+1,inf);//初始化全都是INF
	for(int i = 1;i<=m;i++){
		int u,v;ll w;
		cin>>u>>v>>w;
		g[u].push_back({v,w});//有向图单向建边就好了,u->v
	}
	//优先队列：{当前距离,对应点编号}
	priority_queue<pair<ll,int>,vector<pair<ll,int>>,greater<pair<ll,int>>> pq;
	dist[s] = 0;//起点到起点距离当然就是0
	pq.push({0,s});
	while(!pq.empty()){
		auto [d,u] = pq.top();//取出当前已知距离源点最近的点
		pq.pop();//弹出一个点
		//d和dist[u]是不同的，d是入堆时的状态，dist[u]是当前已知最短距离
		if(d!=dist[u])continue;//只允已经达到最优解的点参与扩展
		//满足以上条件后 此时能确定到达u的最短距离已经确定 如果还有更短的 
		//例如还有源点->...->x->u
		//那么就有dist[x]<dist[u]
		//但此时u是优先队列的top 已经是距离源点最近的了 自相矛盾
		for(auto e:g[u]){
			int v = e.to;
			ll w = e.w;
			if(dist[u]+w<dist[v]){//如果这次距离更短
				dist[v] = dist[u]+w;//就更新更短的距离
				pq.push({dist[v],v});//把当前点推入队列，后续继续计算其余点
			}
		}
	}
	for(int i = 1;i<=n;i++){
		cout<<dist[i]<<(i==n?'\n':' ');
	}
	return 0;
}
