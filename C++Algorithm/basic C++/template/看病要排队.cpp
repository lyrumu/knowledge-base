#include<bits/stdc++.h>
using namespace std;
int main(){
	int n;
	while(cin>>n){
		vector<priority_queue<pair<int,int>>> doctors(11);//¾«Ëè
		int patient_id = 1;
		for(int i = 0;i<n;i++){
			string event;
			cin>>event;
			if(event=="IN"){
				int doctor,priority;
				cin>>doctor>>priority;
				doctors[doctor].push({priority,-patient_id});
				patient_id++;
			}else if(event=="OUT"){
				int doctor;
				cin>>doctor;
				if(!doctors[doctor].empty()){
					pair<int,int> patient = doctors[doctor].top();
					doctors[doctor].pop();
					cout<<-patient.second<<'\n';
				}else{
					cout<<"EMPTY"<<'\n';
				}
			}
		}
	}
	return 0;
}
