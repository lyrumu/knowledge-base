#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
//计算无向图某两点间距离(s和t)
const ll inf = 4e18;
int n,m,s,t;
struct edge{
	int to;
	ll w;
};
vector<vector<edge>> g;
vector<ll> dist;
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cin>>n>>m>>s>>t;
	g.resize(n+1);
	dist.resize(n+1,inf);
	dist[s] = 0;
	for(int i = 0;i<m;i++){
		int u,v;ll w;
		cin>>u>>v>>w;
		g[u].push_back({v,w});//无向图两边都要存图的信息
		g[v].push_back({u,w});
	}
	priority_queue<pair<ll,int>,vector<pair<ll,int>>,greater<pair<ll,int>>> pq;
	pq.push({0,s});
	while(!pq.empty()){
		auto [d,u] = pq.top();
		pq.pop();
		if(d!=dist[u])continue;
		if(u==t){
			cout<<d<<endl;
			return 0;
		}
		for(edge e:g[u]){
			int v = e.to;
			ll w = e.w;
			if(dist[u]+w<dist[v]){
				dist[v] = dist[u]+w;
				pq.push({dist[v],v});
			}
		}
	}

	return 0;
}
