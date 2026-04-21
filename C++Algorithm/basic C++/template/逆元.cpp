#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
//逆元用于模运算替换:(用于替换模运算下的除法操作)
// a/b <==> a*(b的逆元)  (mod MOD) 
const ll MOD = 998244353;
const int N = 2000050;
ll fac[N],invfac[N];

ll fpow(ll base,ll exponent){//快速幂
	ll ans = 1;
	base = base%MOD;//base在不断"变大" 需要%MOD
	while(exponent>0){
		if(exponent%2==1){
			ans = ans*base%MOD;
		}
		base = base*base%MOD;
		exponent/=2;
	}
	return ans;
}

void init(){//预处理阶乘和逆元
	//fac[i] = i!;
	fac[0] = 1;
	for(int i = 1;i<N;i++){
		fac[i] = fac[i-1]*i%MOD;
	}
	//invfac[i]=(i!的逆元)
	//利用费马小定理:a^{-1}=a^(mod-2) (前提是 MOD为质数)
	invfac[N-1] = fpow(fac[N-1],MOD-2);//?
	for(int i = N-2;i>=0;i--){
		//因为(i+1)! = (i+1)*i!;
		//两边同时取逆元： ((i+1)!)^{-1} = (i+1)^{-1} * (i!)^{-1}
		//两边同时乘上(i+1)---> (i!)^{-1} = ((i+1)!)^{-1} * (i+1)
		//也就是如下代码
		invfac[i] = invfac[i+1]*(i+1)%MOD;//?
	}
}

ll C(ll n,ll m){//计算组合数
	if(m<0||m>n)return 0;
	return fac[n]*invfac[m]%MOD*invfac[n-m]%MOD;
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	int t,op;cin>>t>>op;
	if(op==2)init();
	while(t--){
		if(op==1){//n个不同的物品放进m个不同的箱子
			//即计算pow(m,n);-->快速幂
//			ll a,b;cin>>a>>b;
//			ll result = fpow(b,a)%MOD;
//			cout<<result<<endl;
			string n;
			ll m;
			cin>>n>>m;
			ll exp = 0;
			int len = n.size();
			for(int i=0;i<len;i++){//?
				exp = (exp*10 + (n[i]-'0')) % (MOD-1);
			}
			cout<<fpow(m,exp)<<endl;
		}else if(op==2){//n个相同的物品放进m个不同的箱子
			//隔板法;
			//如果要求每个箱子至少有一个物品 那就是求C(n-1,m-1)组合数
			//如果可以有空箱 就需要球和板一起排列 可以是例如oo||oo这种排列
			//就是求C(n+m-1,m-1)组合数
			ll n,m;cin>>n>>m;
			cout<<C(n+m-1,m-1)<<endl;
		}
	}
	return 0;
}
//以下为pdf中的教学伪代码
//const int MOD=1e9+7;
//int poww(int x,int y){
//int t=1;
//while(y){
//if(y&1)t=1LL*t*x%MOD;
//x=1LL*x*x%MOD;
//y>>=1;
//}
//return t;
//}
//int inv(int x){
//return poww(x,MOD-2);


//int fac[N],inv[N];
//void init(){
//int n=2e6;
//fac[0]=1;
//for(int i=1;i<=n;i++){
//fac[i]=1LL*i*fac[i-1]%MOD;
//}
//inv[n]=poww(fac[n],MOD-2);
//for(int i=n-1;i>=0;i--){
//inv[i]=1LL*(i+1)*inv[i+1]%MOD;
//}
//}
//int C(int n,int m){
//if(n<m||n<0||m<0)return 0;
//return 1LL*fac[n]*inv[m]%MOD*inv[n-m]%MOD;
