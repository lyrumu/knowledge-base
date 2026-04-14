#include<bits/stdc++.h>
using namespace std;
#define ll long long
int main(){
	ll n,m;
	cin>>n>>m;
	vector<int> a(n);
	for(ll i = 0;i<n;i++){
		cin>>a[i];
	}
	ll cursum = 0;ll ans = 0;
	ll l = 0;//Ë«Ö¸Õë»¬¶¯´°¿Ú
	for(ll r = 0;r<n;r++){
		cursum += a[r];
		while(cursum>m&&l<=r){
			cursum-=a[l];
			l++;
		}
		if(cursum==m){
			ans++;
		}
	}
	cout<<ans;
	return 0;
}
