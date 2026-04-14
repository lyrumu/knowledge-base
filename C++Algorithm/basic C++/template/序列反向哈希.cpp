#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
const int N = 200010;
const ull P = 131;
int n;
int a[N];
ull h[N],rh[N],p[N];
ull get_hash(int l,int r){
	return h[r]-h[l-1]*p[r-l+1];
}
ull get_rhash(int l,int r){//×Ö·ûµÄ·´Ïò¹þÏ£
	int L = n-r+1;
	int R = n-l+1;
	return rh[R]-rh[L-1]*p[r-l+1];
}

int main(){
	cin>>n;
	for(int i = 1;i<=n;i++){
		cin>>a[i];
	}
	p[0] = 1;
	for(int i = 1;i<=n;i++){
		h[i] = h[i-1]*P+a[i];
		p[i] = p[i-1]*P;
	}
	for(int i = n;i>=1;i--){
		rh[n-i+1] =rh[n-i]*P+a[i];
	}
	int best = 0;
	vector<int> ans;
	for(int k = 1;k<=n;k++){
		int m = n/k;
		if(m==0)break;
		set<pair<ull,ull>> s;
		for(int i = 0;i<m;i++){
			int l = i*k+1;
			int r = (i+1)*k;
			ull x = get_hash(l,r);
			ull y = get_rhash(l,r);
			if(x>y)swap(x,y);
			s.insert({x,y});
		}
		int cur = s.size();
		if(cur>best){
			best = cur;
			ans.clear();
			ans.push_back(k);
		}else if(cur==best){
			ans.push_back(k);
		}
	}
	cout<<best<<" "<<int(ans.size())<<endl;
	for(int x:ans){
		cout<<x<<" ";
	}
	return 0;
}
