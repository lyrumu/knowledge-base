#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long

const int N =3e6+5;//所有模式串的最大可能总字符数
//trie[i][j]表示节点i通过字符j达到的节点
int trie[N][62];//26+26+10;
//cnt[u]表示经过节点u的模式串的个数
int cnt[N];
int node = 0;//表示当前分配的节点个数

int toid(char c){//将字符转换为数字id
    if(c>='a'&&c<='z'){
        return c-'a';
    }
    if(c>='A'&&c<='Z'){
        return 26+c-'A';
    }
    return 52+(c-'0');
}

void ist(const string &s){
    int u = 0;
    for(char c:s){
        int id = toid(c);
        if(!trie[u][id]){
            trie[u][id] = ++node;
        }
        u = trie[u][id];
        cnt[u]++;
    }
}

int que(const string &s){//查询
	int u = 0;
    for(char c:s){
        int id = toid(c);
        if(!trie[u][id]){
            return 0;
        }
        u = trie[u][id];
    }
    return cnt[u];//这里返回的就是以t为前缀的s的数量
}

void clr(){//清除字典树 进行下一轮
    for(int i = 0;i<=node;i++){
        memset(trie[i],0,sizeof(int)*62);
        cnt[i] = 0;
    }
    node = 0;
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	int T;cin>>T;
    while(T--){
        int n,q;
        clr();
        cin>>n>>q;
        for(int i = 0;i<n;i++){
            string s;cin>>s;
            ist(s);
        }
        for(int i = 0;i<q;i++){
            string t;
            cin>>t;
            cout<<que(t)<<endl;
        }
    }
	return 0;
}
