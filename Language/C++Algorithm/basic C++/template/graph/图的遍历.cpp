#include<bits/stdc++.h>
using namespace std;

vector<vector<int>> adj_list;//创建邻接表存储图

vector<bool> vis_dfs;
vector<int> ans_dfs;//存储结果
void dfs(int node){
	vis_dfs[node] = true;
	ans_dfs.push_back(node);
	for(int neighbor:adj_list[node]){
		if(!vis_dfs[neighbor]){
			dfs(neighbor);
		}
	}
}

vector<bool> vis_bfs;
vector<int> ans_bfs;
void bfs(int start){
	queue<int> q;
	vis_bfs[start] = true;
	q.push(start);
	while(!q.empty()){
		int cur = q.front();
		q.pop();
		ans_bfs.push_back(cur);
		for(int neighbor:adj_list[cur]){
			if(!vis_bfs[neighbor]){
				vis_bfs[neighbor] = true;
				q.push(neighbor);
			}
		}
	}
}

int main(){
	int n,m;
	cin>>n>>m;//点的数量，边的数量
	
	adj_list.resize(n);
	vis_dfs.resize(n,false);
	vis_bfs.resize(n,false);
	
	for(int i = 0;i<m;i++){
		int a,b;
		cin>>a>>b;
		adj_list[a].push_back(b);
		adj_list[b].push_back(a);
	}
	//要求按点从小到达排序,那就对每个点的邻居排序
	for(int i = 0;i<n;i++){
		sort(adj_list[i].begin(),adj_list[i].end());
	}
	//dfs
	for(int i = 0;i<n;i++){
		if(!vis_dfs[i]){
			dfs(i);
		}
	}
	//bfs
	for(int i = 0;i<n;i++){
		if(!vis_bfs[i]){
			bfs(i);
		}
	}
	//输出
	int len_dfs = ans_dfs.size();
	for(int i = 0;i<len_dfs;i++){
		cout<<ans_dfs[i]<<" ";
	}
	cout<<endl;
	int len_bfs = ans_bfs.size();
	for(int i = 0;i<len_bfs;i++){
		cout<<ans_bfs[i]<<" ";
	}
	return 0;
}
