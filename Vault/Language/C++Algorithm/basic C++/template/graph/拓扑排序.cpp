#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
//拓扑排序只存在于有向无环图(DAG)
//最终的拓扑序表示依赖关系的线性序
//每个顶点只出现一次且按图的顺序
const int N = 110;
const int M = 160;
vector<int> g[N];//邻接表
int in[N];//存储每个点的入度
int n,m;
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cin>>n>>m;
	while(m--){
		int p1,p2;
		cin>>p1>>p2;
		g[p1].push_back(p2);//p1->p2
		in[p2]++;
	}
	vector<int> ans;//存储结果拓扑序
	//使用优先队列小顶堆 确保了编号小的优先
	priority_queue<int,vector<int>,greater<int>> pq;
	//一般来说只用queue也可以 但是不能确保编号小的点优先
	for(int i = 1;i<=n;i++){
		if(in[i]==0)pq.push(i);//最开始入度就是0的点直接入队
	}
	while(!pq.empty()){
		int u = pq.top();
		pq.pop();
		ans.push_back(u);
		for(int v:g[u]){
			in[v]--;
			if(in[v]==0)pq.push(v);
		}
	}
	int num = ans.size();
	if(num!=n){
		cout<<"no"<<endl;
		return 0;
	}
	for(int i = 0;i<num;i++){
		cout<<ans[i];
		if(i!=num-1)cout<<" ";
	}
	cout<<endl;
	return 0;
}
