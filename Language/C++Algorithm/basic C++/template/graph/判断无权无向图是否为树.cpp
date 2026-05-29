#include<bits/stdc++.h>
using namespace std;
//m=n-1加上无环，能够保证无向图连通
//有向图不可以
const int N = 10010;
int fa[N];
int find(int x){
	if(x==fa[x]){
		return x;
	}
	return fa[x]=find(fa[x]);
}
int main(){
	int n,m;cin>>n>>m;
	if(m!=n-1){
		cout<<"NO";
		return 0;
	}
	for(int i = 1;i<=n;i++){
		fa[i] = i;
	}
	for(int i = 0;i<m;i++){//判断是否有环
		int u,v;cin>>u>>v;
		int fu = find(u);
		int fv = find(v);
		if(fu==fv){//如果已经在同一个集合了，后面又要连一条边，那肯定就成环了
			cout<<"NO";
			return 0;
		}
		fa[fu] = fv;
	}
	cout<<"YES";
	return 0;
}
