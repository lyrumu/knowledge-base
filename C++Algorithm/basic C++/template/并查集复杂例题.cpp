#include<bits/stdc++.h>
using namespace std;
#define ll long long
const int N = 100010,M = 100010;
int fa[N+1];
int size[N+1];
vector<map<int,int>> game_competitors;//每个连通块中的游戏和玩家数的组合
vector<int> game_distribute;//每个游戏的玩家分布在几个连通块
vector<vector<int>> game_players(M+1);//每个游戏的玩家列表
int ans[M+1];//存储每个游戏的答案
int find(int x){
	if(x==fa[x]){
		return x;
	}
	return fa[x] = find(fa[x]);
}
void unite(int x,int y,int edge_id){
	int fx=find(x);
	int fy=find(y);
	if(fx==fy)return;
	if(size[fx]<size[fy]){
		swap(fx,fy);
	}
	for(const auto& game_info:game_competitors[fy]){
		int game_id = game_info.first;
		int players_in_b = game_info.second;
		int players_in_a = 0;
		auto it = game_competitors[fx].find(game_id);
		if(it!=game_competitors[fx].end()){
			players_in_a = it->second;
		}
		game_competitors[fx][game_id] = players_in_a+players_in_b;
		if(players_in_a>0&&players_in_b>0){
			game_distribute[game_id]--;
			if(game_distribute[game_id]==1&&ans[game_id]==-1){
				ans[game_id] = edge_id;
			}
		}
	}
	fa[fy] = fx;
	size[fx]+=size[fy];
}
int main(){
	int n,m,q;
	cin>>n>>m>>q;
	for(int i = 1;i<=n;i++){
		fa[i] = i;
		size[i] = 1;
	}
	game_competitors.resize(n+1);
	game_distribute.resize(m+1,0);
	for(int i = 1;i<=n;i++){
		int game;cin>>game;
		game_players[game].push_back(i);
		game_competitors[i][game] = 1;
	}
	for(int i = 1;i<=m;i++){
		int cnt = game_players[i].size();
		if(cnt==1){
			ans[i] = 0;
		}else{
			ans[i] = -1;
		}
		game_distribute[i] = cnt;
	}
	for(int i = 1;i<=q;i++){
		int u,v;cin>>u>>v;
		unite(u,v,i);
	}
	for(int i = 1;i<=m;i++){
		cout<<ans[i]<<'\n';
	}
	return 0;
}
