#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
//用来判断两个长度相同的序列是否为同一个集合
mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());//映射为随机数的函数
//哈希集合记得要保证相同的数得到相同的映射
unordered_map<int,ull> mp;
int main(){
	int n,q;
	cin>>n>>q;
	int a[n],b[n];
	for(int i = 0;i<n;i++){
		cin>>a[i];
	}
	ull aa[n];
	ull pre_a[n+1] = {0};
	for(int i = 0;i<n;i++){
		cin>>b[i];
	}
	ull bb[n];
	ull pre_b[n+1] = {0};
	for(int i = 0;i<n;i++){//给a数组映射
		if(mp.count(a[i])==0){//这里保证同一个数 映射相同
			mp[a[i]] = rng();
		}
		aa[i] = mp[a[i]];
	}
	for(int i = 0;i<n;i++){//给b数组映射 注意不用clear之前的mp 因为映射需相同
		if(mp.count(b[i])==0){
			mp[b[i]] = rng();
		}
		bb[i] = mp[b[i]];
	}
	for(int i = 1;i<=n;i++){//计算映射后的前缀和
		pre_a[i] = pre_a[i-1]+aa[i-1];
		pre_b[i] = pre_b[i-1]+bb[i-1];
	}
	while(q--){
		int l,r,x,y;
		cin>>l>>r>>x>>y;
		ull h1 = pre_a[r]-pre_a[l-1];//通过前缀和计算集合区间哈希值
		ull h2 = pre_b[y]-pre_b[x-1];
		if(h1==h2){
			cout<<"Yes"<<endl;
		}else{
			cout<<"No"<<endl;
		}
	}
	return 0;
}
