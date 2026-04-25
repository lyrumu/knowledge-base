#include<bits/stdc++.h>
using namespace std;
#define ll long long
const ll N = 100010;
const ll LOG = 20;
ll n,m;
ll a[N];//查询的数组
ll st[N][LOG+1];//表示从下标i开始,长度为2^k次的区间的最值
ll lg[N];//表示log2(i),向下取整;也就是找到查询区间长度内能塞下的最大的2^k
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cin>>n>>m;
	for(ll i = 1;i<=n;i++){
		cin>>a[i];
	}
	//预处理lg数组
	lg[1] = 0;
	for(ll i = 2;i<=n;i++){
		lg[i] = lg[i>>1]+1;
	}
	//初始化st表
	for(ll i = 1;i<=n;i++){
		st[i][0] = a[i];//从i开始长度为1的区间的最值就是a[i]本身
	}
	//预处理st表
	for(ll j = 1;j<=LOG;j++){
		for(ll i = 1;i+(1<<j)-1<=n;i++){
			st[i][j] = max(st[i][j-1],st[i+(1<<(j-1))][j-1]);
		}//将查询的区间切成两半,(2^j)/2=2^(j-1);取大
	}
	//m次查询
	while(m--){
		ll l,r;cin>>l>>r;
		ll len = r-l+1;
		ll k = lg[len];
		ll ans = max(st[l][k],st[r-(1<<k)+1][k]);
		//由于大部分区间都不能直接由2^k表示,用从左开始+2^k的区间
		//加上从右开始-2^k的区间进行覆盖,就一定能包括整个[l,r];
		cout<<ans<<'\n';
	}
	return 0;
}
