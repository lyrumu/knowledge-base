#include <bits/stdc++.h>
using namespace std;
#define ll long long
#define ull unsigned long long
const int N = 2010;
const ull P = 131;
ull p[N];
ull h[N];
ull pre_hash(vector<ull>& h,int l,int r){//每个字符串有自己对应的子串哈希数组
	return h[r]-h[l-1]*p[r-l+1];
}
int main(){
	int n;cin>>n;
	vector<string> s(n);
	for(int i = 0;i<n;i++){
		cin>>s[i];
	}
	p[0] = 1;
	for(int i = 1;i<N;i++){
		p[i] = p[i-1]*P;
	}
	vector<vector<ull>> h(n);//对于每一个字符串 都有一个存储其所有子串哈希值的数组
	for(int i = 0;i<n;i++){//预处理所有字符串的哈希值
		int m = s[i].size();
		h[i].resize(m+1);
		h[i][0] = 0;
		for(int j = 1;j<=m;j++){
			h[i][j] = h[i][j-1]*P+s[i][j-1];//注意 这里h是1-based 而s是0-based 注意下标
		}
	}
	int l = 0;int r = 2000;int ans = 0;
	while(l<=r){
		int mid = (l+r)/2;
		set<ull> st;
		int m = s[0].size();
		for(int i = 1;i+mid-1<=m;i++){
			st.insert(pre_hash(h[0],i,i+mid-1));//将第一个字符串所有长度为mid的子串的哈希值存入集合
		}
		for(int k = 1;k<n;k++){//在剩下字符串中
			set<ull> cur;
			int len = s[k].size();
			for(int i = 1;i+mid-1<=len;i++){
				ull t = pre_hash(h[k],i,i+mid-1);
				if(st.count(t)){//如果st中已经有这个哈希值 (取交集)
					cur.insert(t);
				}
			}
			st = cur;//将st变为交集的交集...
			if(st.empty())break;//空的话就不用做下去了 空集和其他集合相交还是空集
		}
		if(!st.empty()){
			ans = mid;
			l = mid+1;
		}else{
			r = mid-1;
		}
	}
	cout<<ans<<endl;
	return 0;
}
