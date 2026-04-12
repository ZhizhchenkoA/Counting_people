#include <iostream>
#include <vector>
#include "branch.h"

int main() {
    int n;
    double capacity;
    
    std::cin >> n >> capacity;
    
    KnapsackData data;
    data.n = n;
    data.max_w = capacity;
    data.items.resize(n);
    
    for (int i = 0; i < n; i++) {
        std::cin >> data.items[i].second >> data.items[i].first;
    }

    std::vector<int> solution;
    double best_value;
    knapsack_solve(data, solution, best_value, 100000);
    std::cout << "\n";
    std::cout << best_value << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << solution[i] << " ";
    }
    std::cout << std::endl;
    
    return 0;
}