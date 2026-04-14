#include<bits/stdc++.h>
//https://www.luogu.com.cn/problem/P1629
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
const int N = 1010;
const int INF = 1e9;
int n,m;
vector<pair<int,int>> g[N];
int dist[N];//从1到其余各个点的最短路
//由于是单向图 从1->i的路径不等于从i->的路径
//因此还单独需要计算各个点回到1的最短路
//由于dijkstra只能计算一个点到其他所有点的最短路 
//比如i->a->b->c->1  如果取反图 将所有u->v改为v->u
//此时再算一次1到所有i点的最短路 就等效得到了所有i->1的最短路
vector<pair<int,int>> rg[N];//反图
int rdist[N];//所有i到1的最短路

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cin>>n>>m;
	for(int i = 0;i<m;i++){
		int u,v,w;
		cin>>u>>v>>w;
		g[u].push_back({v,w});
		rg[v].push_back({u,w});
	}
	for(int i = 2;i<=n;i++){
		dist[i] = INF;
		rdist[i] = INF;
	}
	dist[1] = 0;
	rdist[1] = 0;
	//正图
	priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> pq;
	pq.push({0,1});
	while(!pq.empty()){
		auto [d,u] = pq.top();
		pq.pop();
		if(d!=dist[u])continue;
		for(auto [v,w]:g[u]){
			if(dist[u]+w<dist[v]){
				dist[v] = dist[u]+w;
				pq.push({dist[v],v});
			}
		}
	}
	//反图
	priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> rpq;
	rpq.push({0,1});
	while(!rpq.empty()){
		auto [d,u] = rpq.top();
		rpq.pop();
		if(d!=rdist[u])continue;
		for(auto [v,w]:rg[u]){
			if(rdist[u]+w<rdist[v]){
				rdist[v] = rdist[u]+w;
				rpq.push({rdist[v],v});
			}
		}
	}
	int ans = 0;
	for(int i = 1;i<=n;i++){
		ans += dist[i]+rdist[i];
	}
	cout<<ans;
	return 0;
}
