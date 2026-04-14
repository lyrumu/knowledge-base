#include<bits/stdc++.h>
//https://www.luogu.com.cn/problem/P8805
using namespace std;
#define ll long long
#define ull unsigned long long
#define endl '\n'
const int N = 1e6+10;
int n,m;
vector<int> g[N<<1];
const int LOG = 20;
int fa[N][LOG+1];
int dep[N];
int dist[N];
int a[N];
void dfs(int u,int f){
	dep[u] = dep[f]+1;
    fa[u][0] = f;
    for(int j = 1;(1<<j)<=dep[u];j++){//不需要每次都跑满LOG层
    	if(fa[u][j-1]==0){
			fa[u][j] = 0;
			continue;
		}
		fa[u][j] = fa[fa[u][j-1]][j-1];
		//每次只初始化自己的fa数组	
	}
    for(int v:g[u]){
        if(v==f)continue;
        dist[v] = dist[u]+a[v];//+g[u].size();
        dfs(v,u);
    }
}

int lca(int x,int y){
    if(dep[x]<dep[y]){
        swap(x,y);
    }
    
    int diff = dep[x]-dep[y];
    for(int i = LOG;i>=0;i--){
        if(diff>=(1<<i)){//更好的写法是"diff&(1<<i)" 然后去掉diff-=
            x = fa[x][i];
            diff-=(1<<i);
        }
    }
    if(x==y)return x;
    for(int i = LOG;i>=0;i--){
        if(fa[x][i]!=fa[y][i]){
            x = fa[x][i];
            y = fa[y][i];
        }
    }
    return fa[x][0];
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cin>>n>>m;
    for(int i = 0;i<n-1;i++){
        int x,y;
        cin>>x>>y;
        g[x].push_back(y);
        g[y].push_back(x);
    }
    dist[1] = g[1].size();
	for(int i = 1;i<=n;i++){
		a[i] = g[i].size();
	}
    dfs(1,0);
    while(m--){
        int u,v;cin>>u>>v;
        int k = lca(u,v);
        int ans = dist[u]+dist[v]-2*dist[k]+a[k];//由于本题累加的是点权
        //公共祖先点被减去两次 最后还应该加上一次
        //一般累加边权的时候 不需要加最后那一项
        cout<<ans<<endl;
    }
	return 0;
}
