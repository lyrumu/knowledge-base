#include<bits/stdc++.h>
using namespace std;

const int N = 50005;
int n;
vector<vector<int>> tree(N);//邻接表存储树
int size[N];//存储每个节点子树大小(自身+子节点)
int weight[N];//存储每个节点的重量
//重点是求weight,size只是为了辅助，方便求出weight
void dfs(int u,int fa){
	size[u] = 1;//子树大小至少为1
	weight[u] = 0;//重量初始化为0
	for(int v:tree[u]){
		if(v==fa)continue;
		dfs(v,u);
		size[u]+=size[v];
		weight[u] = max(weight[u],size[v]);
	}
	weight[u] = max(weight[u],n-size[u]);
}

int main(){
	cin>>n;
	for(int i = 1;i<n;i++){
		int a,b;cin>>a>>b;
		tree[a].push_back(b);
		tree[b].push_back(a);
	}
	dfs(1,0);
	//0是根节点的虚拟父亲节点
	int centroid = 1;//假设重心是1(初始化)
	for(int i = 2;i<=n;i++){
		if(weight[i]<weight[centroid]||(weight[i]==weight[centroid]&&i<centroid)){
			centroid = i;//树最多有两个重心;如果有两个,那一定是相邻的
		}
	}
	//现在找到重心了,计算其他所有节点到重心的距离之和就好了
	long long dist = 0;
	vector<int> distance(n+1,-1);
	queue<int> q;
	distance[centroid] = 0;
	q.push(centroid);
	while(!q.empty()){
		int cur = q.front();
		q.pop();
		dist+=distance[cur];
		for(int i:tree[cur]){
			if(distance[i]==-1){
				distance[i] = distance[cur]+1;
				q.push(i);
			}
		}
	}
	cout<<centroid<<" "<<dist<<endl;
	return 0;
}
