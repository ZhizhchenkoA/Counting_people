#pragma once
#include <vector>
#include <utility>

using Item = std::pair<double, double>;

struct KnapsackData {
    int n;
    double max_w;
    std::vector<Item> items;
};

void knapsack_solve(KnapsackData& data, std::vector<int>& out_sol, double& out_val, int max_iters);