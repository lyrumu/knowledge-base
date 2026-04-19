#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
//注意每轮需要找到距离当前集合最近的点
//因此可以使用 堆优化+邻接表 优化--->O(m log n)
const int N = 200010;
const ll INF = 4e18;
vector<pair<int,ll>> g[N];
bool vis[N];
ll dist[N];
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	int n,m;
	cin>>n>>m;
	for(int i = 1;i<=n;i++){//初始化所有点
		g[i].clear();//清空邻接表
		dist[i] = INF;
		vis[i] = false;
	}
	for(int i = 0;i<m;i++){
		int u,v;
		ll w;
		cin>>u>>v>>w;
		g[u].push_back({v,w});
		g[v].push_back({u,w});
	}
	//小根堆 每次获取距离最小的点
	priority_queue<pair<ll,int>,vector<pair<ll,int>>,greater<pair<ll,int>>> pq;
	dist[1] = 0;
	pq.push({0,1});
	ll ans = 0;
	int cnt = 0;
	while(!pq.empty()){
		auto [d,u] = pq.top();//当前取出的距离目前集合的点
		pq.pop();
		if(vis[u])continue;
		vis[u] = true;
		ans+=d;
		cnt++;
		for(auto[v,w]:g[u]){
			if(!vis[v]&&w<dist[v]){
				dist[v] = w;
				pq.push({dist[v],v});
			}
		}
	}
	if(cnt!=n){
		cout<<"orz"<<endl;
	}else{
		cout<<ans<<endl;
	}
	return 0;
}