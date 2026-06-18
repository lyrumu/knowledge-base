#include<bits/stdc++.h>
//https://www.luogu.com.cn/problem/P3258
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
const int N = 300010;
const int LOG = 20;
vector<int> g[N];
int diff[N];
int fa[N][LOG+1];
int dep[N];
int n;



//void dfs1(int u,int f){
// 	dep[u] = dep[f]+1;
// 	fa[u][0] = f;
// 	for(int i = 1;i<=LOG;i++){
//	 	fa[u][i] = fa[fa[u][i-1]][i-1];
//	 }
// 	for(int v:g[u]){
//	 	if(v==f)continue;
//	 	dfs1(v,u);
//	 }
//}

//第一个dfs换成bfs更好 避免爆栈
//和dfs1是完全等价的
void bfs(int root){
	queue<int> q;
	q.push(root);
	dep[root] = 1;
	fa[root][0] = 0;
	while(!q.empty()){
		int u = q.front();
		q.pop();
		for(int v:g[u]){
			if(v==fa[u][0])continue;
			dep[v] = dep[u]+1;
			fa[v][0] = u;
			for(int i = 1;i<=LOG;i++){
				fa[v][i] = fa[fa[v][i-1]][i-1];
			}
			q.push(v);
		}
	}
}

int lca(int x,int y){
	if(dep[x]<dep[y]){
		swap(x,y);
	}
	int d = dep[x]-dep[y];
	for(int j = LOG;j>=0;j--){
		if(d>=(1<<j)){
			x = fa[x][j];
			d-=(1<<j);
		}
	}
	if(x==y)return x;
	for(int j = LOG;j>=0;j--){
		if(fa[x][j]!=fa[y][j]){
			x = fa[x][j];
			y = fa[y][j];
		}
	}
	return fa[x][0];
}



//void dfs2(int u,int f){//这个dfs作用是对差分数组做前缀和
//	for(int v:g[u]){
//		if(v==f)continue;
//		dfs2(v,u);
//		diff[u]+=diff[v];//子树汇总给根节点
//	}
//}

//dfs2换成栈遍历 防止爆栈
void solve_diff(int root){
    vector<int> parent(n+1, 0);
    vector<int> seq;//用seq代替order
    seq.reserve(n);
    stack<int> st;
    st.push(root);
    parent[root] = 0;
    //先得到一个遍历序
    while(!st.empty()){
        int u = st.top(); st.pop();
        seq.push_back(u);
        for(int v:g[u]){
            if(v == parent[u]) continue;
            parent[v] = u;
            st.push(v);
        }
    }
    //逆序处理=后序
    for(int i = (int)seq.size() - 1; i >= 0; i--){
        int u = seq[i];
        for(int v:g[u]){
            if(v == parent[u]) continue;
            diff[u] += diff[v];
        }
    }
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cin>>n;
	vector<int> order(n+1);//参观顺序
	vector<int> ans(n+1);//存储结果
	for(int i = 1;i<=n;i++){
		cin>>order[i];
	}
	for(int i = 0;i<n-1;i++){
		int x,y;cin>>x>>y;
		g[x].push_back(y);
		g[y].push_back(x);
	}
	bfs(1);
	for(int i = 1;i<n;i++){//注意别=n
		int cur = order[i];
		int nxt = order[i+1];
		int ancestor = lca(cur,nxt);
		diff[cur]++;
		diff[nxt]++;
		diff[ancestor]--;
		if(fa[ancestor][0])diff[fa[ancestor][0]]--;//经典树上差分
	}
	solve_diff(1);
	for(int i = 2;i<=n;i++){
		diff[order[i]]--;//对中间点以及终点的减法放到最后单独处理
		//否则会向上破坏数值结构
	}
	for(int i = 1;i<=n;i++){
		cout<<diff[i]<<endl;
	}
	return 0;
}
