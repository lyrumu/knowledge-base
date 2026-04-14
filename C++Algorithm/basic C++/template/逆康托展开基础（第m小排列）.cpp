#include<bits/stdc++.h>
using namespace std;
#define ll long long
vector<int> get_permutation(int n,int m){
	//预先做一个1-n排列的可用数字
	vector<int> nums;
	for(int i = 1;i<=n;i++){
		nums.push_back(i);
	}
	ll k = m-1;//转换成0-based
	vector<int> ans;//到时候用来存储结果
	//接下来从第一位开始确定每一位
	for(int i = n;i>=1;i--){
		//每确定一个数之前单独确定阶乘结果(如果直接计算所有阶乘会溢出的)
		ll fact = 1;
		bool overflow = false;
		for(int j = 1;j<=i-1;j++){//计算该位的阶乘
			if(fact>k/j){//判断是否"溢出"，等价于fact*j>k
				overflow = true;
				break;
			}
			fact = fact*j;
		}
		if(overflow){
			ans.push_back(nums[0]);//idx = k/fact = 0
			nums.erase(nums.begin());//去掉当前数组及其索引
			//确定第一个数字的时候索引和值相等，后续的话，表示的是当下第几小的数
		}else{
			ans.push_back(nums[k/fact]);
			nums.erase(nums.begin()+k/fact);
			k %= fact; //更新k
		}
	}
	return ans;
}
int main(){
	ll n,m;
	while(cin>>n>>m){
		vector<int> result = get_permutation(n,m);
		int len = result.size();
		for(int i = 0;i<len;i++){
			cout<<result[i];
			if(i!=len-1){
				cout<<" ";
			}
		}
		cout<<'\n';
	}
	return 0;
}
