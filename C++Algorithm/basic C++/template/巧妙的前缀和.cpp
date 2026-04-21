#include<bits/stdc++.h>
using namespace std;
int main(){
	int t;cin>>t;
	while(t--){
		int n,q;cin>>n>>q;
		string a,b;
		cin>>a>>b;
		vector<pair<int,int>> qq(q);
		for(int i = 0;i<q;i++){
			cin>>qq[i].first>>qq[i].second;
		}
		vector<vector<int>> prea(n+1,vector<int>(26,0));//表示1-i中某个字符出现的次数
		vector<vector<int>> preb(n+1,vector<int>(26,0));
		for(int i = 0;i<n;i++){
			prea[i+1] = prea[i];
			preb[i+1] = preb[i];//先复制上一个位置的情况
			prea[i+1][a[i]-'a']++;
			preb[i+1][b[i]-'a']++;//再判断当前前缀和以及当前字符
		}
		
		for(int i = 0;i<q;i++){
			int l_idx = qq[i].first;
			int r_idx = qq[i].second;
			int ans = 0;
			for(int ch = 0;ch<26;ch++){
				int A = prea[r_idx][ch]-prea[l_idx-1][ch];
				int B = preb[r_idx][ch]-preb[l_idx-1][ch];
				ans+=max(0,B-A);
			}
			cout<<ans<<endl;	
		}
	}
	return 0;
}
