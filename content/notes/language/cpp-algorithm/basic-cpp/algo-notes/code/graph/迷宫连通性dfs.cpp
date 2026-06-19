#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
const int N = 110;
int n;
int dx[] = {1,-1,0,0};
int dy[] =  {0,0,1,-1};
char maze[N][N];
bool vis[N][N];
bool dfs(int x1,int y1,int x2,int y2){
	if(x1==x2&&y1==y2){
		return true;
	}
	vis[x1][y1] = true;
	for(int i = 0;i<4;i++){
		int nx = x1+dx[i];
		int ny = y1+dy[i];
		if(nx>=0&&nx<n&&ny>=0&&ny<n){//要先判断是否越界!
			if(maze[nx][ny]=='#')continue;
			if(vis[nx][ny]==true)continue;
			if(dfs(nx,ny,x2,y2))return true;
		}
	}
	return false;
}
int main(){
	int t;cin>>t;
	while(t--){
		cin>>n;
		for(int i = 0;i<n;i++){
			for(int j = 0;j<n;j++){
				cin>>maze[i][j];
			}
		}
		int x1,y1,x2,y2;cin>>x1>>y1>>x2>>y2;
		if(maze[x1][y1]=='#'||maze[x2][y2]=='#'){
			cout<<"NO"<<endl;
			continue;
		}
		memset(vis,false,sizeof(vis));
		bool ans = dfs(x1,y1,x2,y2);
		cout<<(ans?"YES":"NO")<<endl;
	}
	return 0;
}
