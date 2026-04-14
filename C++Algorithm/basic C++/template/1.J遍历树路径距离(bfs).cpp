#include<bits/stdc++.h>
using namespace std;
int main(){
	int n,d;cin>>n>>d;
	vector<vector<int>> adj_list(n+1);//邻接表创图（树）
	for(int i = 0;i<n-1;i++){
		int u,v;
		cin>>u>>v;
		adj_list[u].push_back(v);
		adj_list[v].push_back(u);
	}
	//初始化为-1表示未访问
	vector<int> distance(n+1,-1);//表示由1到其他n个点包括自己的距离
	distance[1] = 0;
	queue<int> q;
	q.push(1);
	while(!q.empty()){
		int cur = q.front();
		q.pop();
		for(int neighbor:adj_list[cur]){
			if(distance[neighbor]==-1){
				distance[neighbor] = distance[cur]+1;
				q.push(neighbor);
			}
		}
	}
	int ans = 0;
	for(int i = 2;i<=n;i++){
		if(distance[i]<d&&distance[i]!=-1){
			ans++;
		}
	}
	cout<<ans<<endl;
	return 0;
}
