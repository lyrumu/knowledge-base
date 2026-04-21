#include<bits/stdc++.h>
using namespace std;
//由于结点数值不一定是0-n之类的，可以用(映射)来存储树
int main(){
	int n;cin>>n;
	map<int,vector<int>> adj_list;
	int fu,fv;
	cin>>fu>>fv;
	int start = fu;//随便找第一个点当起点
	adj_list[fu].push_back(fv);
	adj_list[fv].push_back(fu);
	for(int i = 1;i<n-1;i++){//输入剩下的节点
		int u,v;cin>>u>>v;
		adj_list[u].push_back(v);
		adj_list[v].push_back(u);
	}
	int maxv = 0;//最远距离
	int x = start;//最远点1
	map<int,int> distance;//存储每个节点到起点的距离
	distance[start] = 0;
	//随便找一个开始结点，找到距离改结点最远的点x，再找到离x最远的点y，xy就是直径？
	//bfs1
	queue<int> q;
	q.push(start);
	while(!q.empty()){
		int cur = q.front();
		q.pop();
		for(int neighbor:adj_list[cur]){
			if(distance.find(neighbor)==distance.end()){//如果还没访问
				distance[neighbor] = distance[cur]+1;
				q.push(neighbor);
				if(distance[neighbor]>maxv){
					maxv = distance[neighbor];
					x = neighbor;
				}
			}
		}
	}
	//bfs2
	map<int,int> dist2;
	queue<int> q2;
	dist2[x] = 0;
	q2.push(x);
	int y = x;//相对于x的最远点
	int d = 0;//答案直径
	while(!q2.empty()){
		int cur = q2.front();
		q2.pop();
		for(int neighbor:adj_list[cur]){
			if(dist2.find(neighbor)==dist2.end()){
				dist2[neighbor] = dist2[cur]+1;
				q2.push(neighbor);
				if(dist2[neighbor]>d){
					d = dist2[neighbor];
					y = neighbor;
				}
			}
		}
	}
	cout<<d<<endl;
	return 0;
}
