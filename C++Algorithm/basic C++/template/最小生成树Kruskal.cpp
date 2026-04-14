#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
//最小生成树要求:(用最小的代价把所有的点连接起来)
//边数 = 点数 - 1
//连通
//无环
//kruskal就是按边权排序 再利用并查集贪心 适合稀疏无向图
//不连通时得到最小生成森林
const int N = 5010;
int fa[N];
int find(int x){
	if(x==fa[x])return x;
	return fa[x]=find(fa[x]);
}
bool unite(int x,int y){
	int fx = find(x);
	int fy = find(y);
	if(fx==fy)return false;//已经连通
	fa[fx] = fy;return true;//合并
}
struct edge{
	int u,v;
	ll w;
};
bool cmp(edge a,edge b){//sort按边权排序的比较函数
	return a.w<b.w;
}
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	int n,m;
	cin>>n>>m;
	vector<edge> e(m);
	for(int i = 0;i<m;i++){
		cin>>e[i].u>>e[i].v>>e[i].w;
	}
	for(int i = 1;i<=n;i++){
		fa[i] = i;
	}
	//按边权排序 贪心 边权小 就尝试先连通
	sort(e.begin(),e.end(),cmp);
	ll ans = 0;
	int cnt = 0;
	for(int i = 0;i<m;i++){
		if(unite(e[i].u,e[i].v)){//如果是本来没有连通的才进入
			ans+=e[i].w;
			cnt++;
			if(cnt==n-1)break;//生成树就是需要刚好n-1条边
		}
	}
	if(cnt!=n-1)cout<<"orz"<<endl;//如果无法联通输出"orz"
	else cout<<ans<<endl;//能连通 输出连通后的边权和
	return 0;
}
