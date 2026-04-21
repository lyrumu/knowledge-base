#include<bits/stdc++.h>
using namespace std;
//要习惯写全局,代替局部的vector
const int N = 430;
int n,m;
char maze[N][N];//存储迷宫信息
int dist[N][N];//表示起点到其他的距离

struct node{
	int x;int y;
}start,target;

int dx[] = {0,0,1,-1};
int dy[] = {1,-1,0,0};//表示每次上下左右四种走法

int bfs(){
	queue<node> q;
	q.push(start);
	memset(dist,-1,sizeof(dist));//用于快速初始化或者清空
	dist[start.x][start.y] = 0;
	while(!q.empty()){
		node cur = q.front();
		q.pop();
		if(cur.x==target.x&&cur.y==target.y){//终止条件
			return dist[cur.x][cur.y];
		}
		for(int i = 0;i<4;i++){
			int nx = cur.x+dx[i];
			int ny = cur.y+dy[i];
			if(nx>=0&&nx<n&&ny>=0&&ny<m&&maze[nx][ny]!='#'&&dist[nx][ny]==-1){
				dist[nx][ny] = dist[cur.x][cur.y]+1;
				q.push({nx,ny});
			}
		}
	}
	return -1;//最后走不出迷宫就返回-1
}

int main(){
	cin>>n>>m;	
	for(int i = 0;i<n;i++){
		for(int j = 0;j<m;j++){
			cin>>maze[i][j];
			if(maze[i][j]=='S')start={i,j};
			if(maze[i][j]=='T')target={i,j};
		}
	}
	cout<<bfs()<<'\n';
	return 0;
}
