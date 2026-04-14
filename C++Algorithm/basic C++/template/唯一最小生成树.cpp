#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
const int N = 200010;
const int M = 200010;
int fa[N];
int find(int x){
	if(x==fa[x])return x;
	return fa[x] = find(fa[x]);
}
struct e{
	int u,v;
	ll w;
};
bool cmp(e a,e b){
	return a.w<b.w;
}
int n,m;
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cin>>n>>m;
	vector<e> edge(m);
	ll ans = 0;
	for(int i = 1;i<=n;i++)fa[i] = i;
	for(int i = 0;i<m;i++){
		cin>>edge[i].u>>edge[i].v>>edge[i].w;
	}
	sort(edge.begin(),edge.end(),cmp);
	int i = 0;
	while(i<m){
		int j = i;
		while(j<m&&edge[i].w==edge[j].w)j++;
		for(int k = i;k<j;k++){
			int u = find(edge[k].u);
			int v = find(edge[k].v);
			if(u!=v){
				ans+=edge[k].w;//第一次遍历 只要是需要连通的边 通通先算上
			}
		}
		for(int k = i;k<j;k++){
			int u = find(edge[k].u);
			int v = find(edge[k].v);
			if(u!=v){
				//第二次遍历 每次都真的合并上 
				//因此 后续若又有连接这两个块的边
				//就不会进入这个if,ans里就会保留这个需要删去的"重边"
				fa[u] = v;
				ans-=edge[k].w;
			}
		}
		i = j;
	}
	cout<<ans<<endl;
	return 0;
}
