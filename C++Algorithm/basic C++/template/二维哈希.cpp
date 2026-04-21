#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long
//二维哈希用来快速判断两个子矩阵是否相同
//字符哈希+二位前缀和
//1-based
const int N = 1010;
ull h[N][N];//存储二维矩阵的哈希
ull base1 = 131;//行base 横向扩展 即列方向
ull base2 = 233;//列base 纵向扩展 即行方向
ull p1[N],p2[N];
int a[N][N];//原矩阵
int n,m,x,y,q;
void init(){
	//base幂初始化
	p1[0]=p2[0]=1;
	int idx = max(n,m);//取较大的 一次性处理完行列
	for(int i = 1;i<=idx;i++){
		p1[i] = p1[i-1]*base1;
		p2[i] = p2[i-1]*base2;
	}
	//行哈希
	for(int i = 1;i<=n;i++){
		for(int j = 1;j<=m;j++){
			h[i][j] = h[i][j-1]*base1+a[i][j];//处理完后 h[i][j]表示第i行前j个的哈希值
		}
	}
	//再处理列哈希
	for(int i = 1;i<=n;i++){
		for(int j = 1;j<=m;j++){
			h[i][j] = h[i-1][j]*base2+h[i][j];//注意这里是h[i][j]
		}
	}
}
ull query(int x1,int y1,int x2,int y2){//返回子矩阵哈希值
	return h[x2][y2]-h[x1-1][y2]*p2[x2-x1+1]-h[x2][y1-1]*p1[y2-y1+1]+h[x1-1][y1-1]*p1[y2-y1+1]*p2[x2-x1+1];
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	cin>>n>>m>>x>>y;
	for(int i = 1;i<=n;i++){
		string s;
		cin>>s;
		for(int j = 1;j<=m;j++){
			a[i][j] = s[j-1]-'0';
		}
	}
	init();
	vector<ull> st;
	st.reserve(1000000);//只预留容量 但不实际存入元素
	for(int i = x;i<=n;i++){//这里的x理解为x2
		for(int j = y;j<=m;j++){//j理解为y2
			int x1 = i-x+1;
			int y1 = j-y+1;
			ull value = query(x1,y1,i,j);
			st.push_back(value);
		}
	}
	sort(st.begin(),st.end());//排序
	st.erase(unique(st.begin(),st.end()),st.end());//去重
	cin>>q;
	while(q--){
		ull cur = 0;//存储后面输入的矩阵的哈希值
		for(int i = 1;i<=x;i++){
			string s;
			cin>>s;
			ull row = 0;
			for(int j = 1;j<=y;j++){
				row = row*base1+(s[j-1]-'0');
			}
			cur = cur*base2+row;
		}
		if(binary_search(st.begin(),st.end(),cur)){//binary_search是STL的二分查找函数
			cout<<1<<endl;
		}else{
			cout<<0<<endl;
		}
	}
	return 0;
}
