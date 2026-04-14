#include<bits/stdc++.h>
using namespace std;
#define ll long long
//并查集不支持删除但是支持添加操作
//因此对于删除节点的题目可以逆序逐个操作
const int N = 3010;
int n,m;
vector<vector<int>> graph(N);
int closed[N];//用来存储仓库的关闭顺序
bool open[N];//逆序添加仓库标记
int fa[N];
string ans[N];//存储答案
int find(int x){
	return fa[x]==x?x:fa[x] = find(fa[x]);
}
int main(){
	cin>>n>>m;
	for(int i = 0;i<m;i++){
		int u,v;
		cin>>u>>v;
		graph[u].push_back(v);
		graph[v].push_back(u);
	}
	for(int i = 0;i<n;i++){
		cin>>closed[i];
	}
	for(int i = 1;i<=n;i++){
		fa[i] = i;
		open[i] = false;
	}
	int components = 0;//连通块数量
	for(int i = n-1;i>=0;i--){
		int cur = closed[i];
		open[cur] = true;
		components++;
		for(int v:graph[cur]){
			if(open[v]){
				int fx = find(cur);
				int fy = find(v);
				if(fx!=fy){
					fa[fx] = fy;
					components--;
				}
			}
		}
		ans[i] = components==1?"YES":"NO";
	}
	for(int i = 0;i<n;i++){
		cout<<ans[i]<<'\n';
	}
	return 0;
}
//标准判断连通块的方法
//find(i)==i;cnt++;
