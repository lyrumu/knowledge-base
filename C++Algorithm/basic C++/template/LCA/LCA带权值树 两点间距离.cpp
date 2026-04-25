#include<bits/stdc++.h>
using namespace std;
#define ll long long
#define endl '\n'
#define ull unsigned long long

const int N = 100010;
const int LOG = 17;

// 邻接表：存 (目标节点, 边权)
vector<pair<int, int>> g[N];

int dep[N];           // 深度
int fa[N][LOG];       // 倍增祖先
ll dis[N];            // 根到当前节点的距离（累加边权）
int n, q;

void dfs(int u, int f) {
    fa[u][0] = f;
    for (auto [v, w] : g[u]) {
        if (v == f) continue;
        dep[v] = dep[u] + 1;
        dis[v] = dis[u] + w;   // 关键：累加边权
        dfs(v, u);
    }
}

int lca(int x, int y) {
    if (dep[x] < dep[y]) swap(x, y);
    
    // 把 x 提到和 y 同一深度
    int diff = dep[x] - dep[y];
    for (int i = LOG - 1; i >= 0; i--) {
        if (diff >= (1 << i)) {
            x = fa[x][i];
            diff -= (1 << i);
        }
    }
    
    if (x == y) return x;
    
    // 一起往上跳
    for (int i = LOG - 1; i >= 0; i--) {
        if (fa[x][i] != fa[y][i]) {
            x = fa[x][i];
            y = fa[y][i];
        }
    }
    return fa[x][0];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    
    cin >> n;
    for (int i = 1; i <= n - 1; i++) {
        int x, y, w;
        cin >> x >> y >> w;
        g[x].push_back({y, w});
        g[y].push_back({x, w});
    }
    
    cin >> q;
    
    // 预处理顺序不能乱
    dep[1] = 0;
    dis[1] = 0;
    dfs(1, 1);
    
    // 倍增表预处理
    for (int j = 1; j < LOG; j++) {
        for (int i = 1; i <= n; i++) {
            fa[i][j] = fa[fa[i][j-1]][j-1];
        }
    }
    
    while (q--) {
        int x, y;
        cin >> x >> y;
        int anc = lca(x, y);
        
        // 带权距离公式
        ll dist = dis[x] + dis[y] - 2 * dis[anc];
        cout << dist << endl;
    }
    
    return 0;
}
