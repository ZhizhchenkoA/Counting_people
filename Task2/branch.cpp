#include "branch.h"
#include <algorithm>

static std::vector<int> g_best_sol;
static double g_best_val = -1;
static int g_max_nodes = 0;
static int g_nodes_count = 0;

double get_bound(KnapsackData& data, int idx, double cur_val, double cur_w, std::vector<int>& taken) {
    if (cur_w > data.max_w) return -1;
    double bound = cur_val;
    double free = data.max_w - cur_w;
    for (int i = idx; i < data.n && free > 0; i++) {
        double w = data.items[i].first;
        double v = data.items[i].second;
        if (w <= free) {
            bound += v;
            free -= w;
        } else {
            bound += v * (free / w); 
            free = 0;
        }
    }
    return bound;
}

void bb_recursive(KnapsackData& data, int idx, double cur_val, double cur_w, std::vector<int>& cur_sol) {
    g_nodes_count++;
    if (g_nodes_count > g_max_nodes) return;

    if (cur_val > g_best_val && cur_w <= data.max_w) {
        g_best_val = cur_val;
        g_best_sol = cur_sol;
    }
    
    if (idx == data.n) return;
    
    double bound = get_bound(data, idx, cur_val, cur_w, cur_sol);
    if (bound <= g_best_val + 1e-9) 
        return;
    if (cur_w + data.items[idx].first <= data.max_w) {
        cur_sol[idx] = 1;
        bb_recursive(data, idx + 1, cur_val + data.items[idx].second, cur_w + data.items[idx].first, cur_sol);
    }
    
    cur_sol[idx] = 0;
    bb_recursive(data, idx + 1, cur_val, cur_w, cur_sol);
}

std::vector<int> knapsack_get_initial(KnapsackData& data, double& val) {
    std::vector<int> sol(data.n, 0);
    double w = 0;
    val = 0;
    for (int i = 0; i < data.n; i++) {
        if (w + data.items[i].first <= data.max_w) {
            w += data.items[i].first;
            val += data.items[i].second;
            sol[i] = 1;
        }
    }
    return sol;
}

double knapsack_get_value(KnapsackData& data, std::vector<int>& sol) {
    double ans = 0;
    for (int i = 0; i < data.n; i++)
        if (sol[i] == 1) 
            ans += data.items[i].second;
    return ans;
}

bool knapsack_is_valid(KnapsackData& data, std::vector<int>& sol) {
    double w = 0;
    for (int i = 0; i < data.n; i++)
        if (sol[i] == 1) 
            w += data.items[i].first;
    return w <= data.max_w;
}

void knapsack_solve(KnapsackData& data, std::vector<int>& out_sol, double& out_val, int max_iters) {
    g_best_val = -1;
    g_best_sol = std::vector<int>(data.n, 0);
    g_max_nodes = max_iters;
    g_nodes_count = 0;
    double init_val;
    g_best_sol = knapsack_get_initial(data, init_val);
    g_best_val = init_val;
    std::vector<int> cur_sol(data.n, 0);
    bb_recursive(data, 0, 0, 0, cur_sol);
    out_sol = g_best_sol;
    out_val = g_best_val;
}