#include<bits/stdc++.h>
using namespace std;
const int N = 10010,M = 30010;
int fa[N+M];//奶牛和语言都作为节点
int find(int x){
	if(x==fa[x]){
		return x;
	}
	return fa[x] = find(fa[x]);
}
void unite(int x,int y){
	int fx = find(x);
	int fy = find(y);
	if(fx!=fy){
		if(fx<fy){//让编号小的作为合并后的根，就等于让奶牛作为根
			fa[fy] = fx;
		}else{
			fa[fx] = fy;
		}
	}
}

int main(){
	int n,m;cin>>n>>m;
	for(int i = 1;i<=n+m;i++){
		fa[i] = i;
	}
	bool alnolan = true;//判断是否所有奶牛都不会任何语言
	for(int i = 1;i<=n;i++){
		int k;cin>>k;
		if(k>0)alnolan = false;
		for(int j = 0;j<k;j++){
			int language;cin>>language;
			unite(i,n+language);
		}
	}
	if(alnolan){
		cout<<n<<'\n';//注意需要n而不是n-1
		return 0;
	}
	//接下来统计连通块数量
	set<int> roots;
	//存在三种连通块：1.有奶牛节点也有语言节点
	//2.只有奶牛节点(该奶牛不会任何语言)
	//3.只有语言节点(没有奶牛会该种语言)
	//我们需要的是包含奶牛的连通块数量!
	for(int i = 1;i<=n;i++){//因为只关心奶牛的连通性,i<=n就可以了
		roots.insert(find(i));
	}
	cout<<roots.size()-1<<'\n';
	return 0;
}
