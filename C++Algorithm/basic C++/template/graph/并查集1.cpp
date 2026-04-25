#include<bits/stdc++.h>
using namespace std;
//与图不同，并查集只考虑归属关系，但不一定要知道具体连接方式
const int N = 10010;
struct DSU{//并查集
	int pa[N];//用来存放父亲节点
	int size[N];//存储每个集合的大小
	void init(int n){//初始化
		for(int i = 1;i<=n;i++){
			pa[i] = i;
			size[i] = 1;
		}
	}
	int find(int x){//查找根节点(路径压缩版)
		if(pa[x]==x){
			return x;
		}
		return pa[x]=find(pa[x]);//先赋值再返回
	}
	void unite(int x,int y){//合并集合(优化)
		int px = find(x);
		int py = find(y);
		if(px==py)return;
		if(size[px]>size[py]){
			swap(px,py);
		}
		pa[px] = py;
		size[py]+=size[px];
	}
	bool same(int x,int y){//判断是否在同一个集合
		return find(x)==find(y);
	}
};

int main(){
	int n,q;cin>>n>>q;
	DSU dsu;
	dsu.init(n);
	for(int i = 0;i<q;i++){
		int z,x,y;
		cin>>z>>x>>y;
		if(z==1){
			dsu.unite(x,y);
		}else if(z==2){
			cout<<(dsu.same(x,y)?"Y":"N")<<'\n';
		}
	}
	return 0;
}
