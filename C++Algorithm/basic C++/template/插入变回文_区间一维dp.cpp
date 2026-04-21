#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
//https://www.luogu.com.cn/problem/P1435
//dp[i][j]表示将字符串区间[i,j]的部分变成回文需要的最小操作数
//如果s[i]==s[j]-->dp[i][j] = dp[i+1][j-1];
//如果s[i]!=s[j]-->dp[i][j] = min(dp[i+1][j],dp[i][j-1])+1
//发现dp[i][j]只依赖于dp[i+1][j-1],dp[i+1][j],dp[i][j-1];
const int N = 5010;
int dp[N];
char s[N];
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	int n;cin>>n;
	string str;
	cin>>str;
	for(int i = 0;i<n;i++){
		s[i+1] = str[i];//1-based
	}
	for(int i = n;i>=1;i--){
		int last = 0;//表示dp[i+1][j-1];
		for(int j = i+1;j<=n;j++){
			int tmp = dp[j];//记录dp[i+1][j];
			if(s[i]==s[j]){
				dp[j] = last;
			}else{
				dp[j] = min(dp[j],dp[j-1])+1;
			}
			last = tmp;
		}
	}
	cout<<dp[n]<<endl;
	return 0;
}
