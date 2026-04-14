#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
const int N = 1000005;
const ull P = 131;
char s[N];
ull h[N];
ull p[N];//预处理并存储P的幂次
ull get_hash(int l,int r){
	return h[r]-h[l-1]*p[r-l+1];//前缀和作差哈希公式
}
int main(){
	scanf("%s",s+1);//让下标从1开始写入 哈希类的都比较适合1-based
	int n = strlen(s+1);
	p[0] = 1;//P的0次是1
	for(int i = 1;i<=n;i++){
		h[i] = h[i-1]*P+s[i];
		p[i] = p[i-1]*P;//比如第一次循环就存储了 P的1次是131 也就是P本身
	}
	int m;cin>>m;
	while(m--){
		int l1,l2,r1,r2;
		cin>>l1>>r1>>l2>>r2;
		if(r1-l1==r2-l2){
			if(get_hash(l1,r1)==get_hash(l2,r2)){//判断子串哈希值是否相等
				cout<<"Yes"<<endl;
			}else{
				cout<<"No"<<endl;
			}
		}
	}
	return 0;
}
