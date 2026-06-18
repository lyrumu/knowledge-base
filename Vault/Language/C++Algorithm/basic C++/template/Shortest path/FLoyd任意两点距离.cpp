#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
//Floyd就是不断尝试新的中转点 看看会不会出现更近的路线
//强制经过中转点k 看路径会不会更短
const int INF = 1e9;
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	int n,m;cin>>n>>m;
	vector<vector<int>> dis(n,vector<int>(n));
	for(int i = 0;i<n;i++){
		for(int j = 0;j<n;j++){
			cin>>dis[i][j];
		}
	}
	//Floyd三重循环
	//外层k：当前允许作为中转点的编号
	for(int k = 0;k<n;k++){
		//i:路径起点
		for(int i = 0;i<n;i++){
			//j:路径终点
			for(int j = 0;j<n;j++){
				if(dis[i][j]>dis[i][k]+dis[k][j]){
					dis[i][j] = dis[i][k]+dis[k][j];//更优的话就更新
				}
			}
		}
	}
	while(m--){
		int s,t;cin>>s>>t;
		cout<<dis[s][t]<<endl;
	}
	return 0;
}
