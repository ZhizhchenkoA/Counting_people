#pragma once
#include <vector>
#include <utility>

using Item = std::pair<double, double>;

struct KnapsackData {
    int n;
    double max_w;
    std::vector<Item> items;
};

std::vector<int> knapsack_get_initial(KnapsackData& data, double& val);
std::vector<int> knapsack_neighbour(KnapsackData& data, std::vector<int>& prev, double& val, bool& ok);
double knapsack_get_value(KnapsackData& data, std::vector<int>& sol);
bool knapsack_is_valid(KnapsackData& data, std::vector<int>& sol);

void knapsack_solve(KnapsackData& data, std::vector<int>& out_sol, double& out_val, int max_iters);