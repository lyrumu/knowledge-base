#include<bits/stdc++.h>
using namespace std;
int main(){
	int n,m;
	cin>>n>>m;
	vector<int> w(n);
	int maxw = 0;
	int max_value =0 ;
	for(int i = 0;i<n;i++){
		cin>>w[i];
		maxw = max(maxw,w[i]);
	}
	if(m>=n){
		cout<<maxw;
		return 0;
	}
	priority_queue<int,vector<int>,greater<int>> q;//Ð¡¶¥¶Ñ
	for(int i = 0;i<m;i++){
		q.push(w[i]);
		if(w[i]>max_value){
			max_value = w[i];
		}
	}
	for(int i = m;i<n;i++){
		int earliest = q.top();
		q.pop();
		int new_time = earliest+w[i];
		if(new_time>max_value){
			max_value = new_time;
		}
		q.push(new_time);
	}
	cout<<max_value;
	return 0;
}
