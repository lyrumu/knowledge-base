#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
const int N = 50010;
int n;
vector<int> tree[N];
ll size[N];
ll weight[N];//每个节点的重量
ll population[N];//每个节点的权重
ll tot = 0;//总的权重
void dfs(int u,int f){//计算节点重量
	size[u] = population[u];
	weight[u] = 0;
	for(int v:tree[u]){
		if(v==f)continue;
		dfs(v,u);
		size[u]+=size[v];
		weight[u] = max(weight[u],size[v]);
	}
	weight[u] = max(weight[u],tot-size[u]);
}

int main(){
	cin>>n;
	for(int i = 1;i<=n;i++){
		int u,v;
		cin>>population[i]>>u>>v;
		tot+=population[i];
		if(u!=0){
			tree[i].push_back(u);
			tree[u].push_back(i);
		}
		if(v!=0){
			tree[i].push_back(v);
			tree[v].push_back(i);
		}
	}
	dfs(1,0);
	int centroid = 1;
	for(int i = 2;i<=n;i++){
		if(weight[i]<weight[centroid]){
			centroid = i;//找到加权重心
		}
	}
	ll dist = 0;
	vector<int> distance(n+1,-1);
	queue<int> q;
	distance[centroid] = 0;
	q.push(centroid);
	while(!q.empty()){//计算总距离
		int cur = q.front();q.pop();
		dist+=distance[cur]*population[cur];//记得乘上权重
		for(int v:tree[cur]){
			if(distance[v]==-1){
				distance[v] = distance[cur]+1;
				q.push(v);
			}
		}
	}
	cout<<dist<<endl;
	return 0;
}
