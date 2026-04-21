#include<bits/stdc++.h>
using namespace std;

int bfs(int node,vector<vector<int>>& a,int n){
	vector<int> distance(n+1,-1);
	distance[node] = 0;
	int total = 0;//存储该节点到其他点的总距离和
	queue<int> q;
	q.push(node);
	while(!q.empty()){
		int cur = q.front();
		q.pop();
		total+=distance[cur];
		for(int neighbor:a[cur]){
			if(distance[neighbor]==-1){
				distance[neighbor] = distance[cur]+1;
				q.push(neighbor);
			}
		}
	}
	return total;
}
int main(){
	int n;cin>>n;
	int final_dot = 1;
	int min_dist = INT_MAX;
	vector<vector<int>> tree(n+1);//邻接表创树
	for(int i = 1;i<=n-1;i++){
		int a,b;
		cin>>a>>b;
		tree[a].push_back(b);
		tree[b].push_back(a);
	}
	//接下来计算每个节点到其余所有点的最短距离并求和
	for(int i = 1;i<=n;i++){
		int cur_dist = bfs(i,tree,n);
		if(cur_dist<min_dist){
			min_dist = cur_dist;
			final_dot = i;
		}else if(cur_dist==min_dist&&i<final_dot){
			final_dot = i;
		}
	}
	cout<<min_dist<<" "<<final_dot<<endl;
	return 0;
}
