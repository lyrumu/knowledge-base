#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long//利用溢出尽量避免哈希冲突
const int P = 131;
ull get_hash(string s){//计算一整个字符串对应的哈希值
	ull h = 0;
	int len = s.size();
	for(int i = 0;i<len;i++){
		h = h*P+s[i];//哈希函数  h[i-1]*P+s[i]
	}
	return h;
}
int main(){
	int n;cin>>n;
	vector<ull> a(n);
	for(int i = 0;i<n;i++){
		string s;cin>>s;
		a[i] = get_hash(s);
	}
	sort(a.begin(),a.end());
	int ans = 1;
	for(int i = 1;i<n;i++){
		if(a[i]!=a[i-1]){
			ans++;
		}
	}
	cout<<ans<<endl;//输出有多少个不同的字符串
	return 0;
}
