#include<bits/stdc++.h>
using namespace std;
const int N = 5010;

int pa[N];//存储父亲节点

int find(int x){//查找
	if(x==pa[x]){
		return x;
	}
	return pa[x]=find(pa[x]);
}
void unite(int x,int y){//合并
	int px = find(x);
	int py = find(y);
	if(px!=py){
		pa[px] = py;
	}
}

int main(){
	int n,m,q;
	cin>>n>>m>>q;
	for(int i = 1;i<=n;i++){
		pa[i] = i;//初始化父亲
	}
	for(int i = 0;i<m;i++){
		int a,b;cin>>a>>b;
		unite(a,b);//a,b有亲戚关系
	}
	for(int i = 0;i<q;i++){
		int a,b;cin>>a>>b;
		if(find(a)==find(b)){
			cout<<"Yes"<<'\n';
		}else{
			cout<<"No"<<'\n';
		}
	}
	return 0;
}
