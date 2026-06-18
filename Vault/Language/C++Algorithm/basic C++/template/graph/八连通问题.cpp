#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
int dx[] = {1,-1,0,0,1,1,-1,-1};//八连通
int dy[] = {0,0,-1,1,1,-1,1,-1};
const int N = 120;
int n,m;
char land[N][N];
bool vis[N][N];
void dfs(int x,int y){//目的就是把属于同一个水洼的W全部标记掉
	vis[x][y] = true;
	for(int i = 0;i<8;i++){
		int nx = x+dx[i];
		int ny = y+dy[i];
		if(nx>=0&&nx<n&&ny>=0&&ny<m){
			if(vis[nx][ny])continue;
			if(land[nx][ny]=='W'){
				dfs(nx,ny);
			}
		}
	}
}
int main(){
	cin>>n>>m;
	for(int i = 0;i<n;i++){
		for(int j = 0;j<m;j++){
			cin>>land[i][j];
		}
	}
	int ans = 0;
	memset(vis,false,sizeof(vis));
	for(int i = 0;i<n;i++){
		for(int j = 0;j<m;j++){
			if(land[i][j]=='W'&&!vis[i][j]){
				ans++;
				dfs(i,j);
			}
		}
	}
	cout<<ans<<endl;
	return 0;
}
