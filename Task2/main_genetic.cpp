#include <iostream>
#include <vector>
#include <ctime>
#include "genetic.h"
#define MAX_ITERS 500

int main() {
    srand(time(0));
    
    int n;
    double capacity;
    std::cin >> n >> capacity;
    
    KnapsackData kd;
    kd.n = n;
    kd.max_w = capacity;
    kd.items.resize(n);
    
    for (int i = 0; i < n; i++)
        std::cin >> kd.items[i].second >> kd.items[i].first;
    
    std::vector<int> ans;
    double ans_val;
    knapsack_solve(kd, ans, ans_val, 500); 
    
    std::cout << "\n";
    std::cout << ans_val << std::endl;
    for (int i = 0; i < n; i++)
        std::cout << ans[i] << " ";
    std::cout << std::endl;
    
    return 0;
}