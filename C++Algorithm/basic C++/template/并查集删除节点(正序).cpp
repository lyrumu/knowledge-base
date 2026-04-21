#include<bits/stdc++.h>
using namespace std;
#define ll long long
const int N = 3010;
int n,m;
bool closed[N];
vector<pair<int,int>> edges;
int find(int x,int fa[]){
	return fa[x]==x?x:fa[x] = find(fa[x],fa);
}
bool is(){
	int cnt = 0;
	int tmp_fa[N];//每次重建并查集
	for(int i = 1;i<=n;i++){
		tmp_fa[i] = i;
	}
	int num = edges.size();
	for(int i = 0;i<num;i++){
		int u = edges[i].first;int v = edges[i].second;
		if(!closed[u]&&!closed[v]){
			int fu = find(u,tmp_fa);
			int fv = find(v,tmp_fa);
			if(fu!=fv){
				tmp_fa[fu] = fv;
			}
		}
	}
	for(int i = 1;i<=n;i++){
		if(!closed[i]&&find(i,tmp_fa)==i){
			cnt++;
		}
	}
	if(cnt==0)return true;//?
	return cnt==1;
}
int main(){
	cin>>n>>m;
	for(int i = 1;i<=n;i++){
		closed[i] = false;
	}
	for(int i = 0;i<m;i++){
		int u,v;cin>>u>>v;
		edges.push_back({u,v});
	}
	for(int i = 0;i<n;i++){
		//先判断再操作
		bool ans = is();
		if(ans){
			cout<<"YES"<<'\n';
		}else{
			cout<<"NO"<<'\n';
		}
		int cur;cin>>cur;
		closed[cur] = true;
	}
	return 0;
}
