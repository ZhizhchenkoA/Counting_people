#include "genetic.h"
#include <cstdlib>
#include <algorithm>


double calc_fitness(const KnapsackData& data, const std::vector<int>& ind) {
    double w = 0, v = 0;
    for (int i = 0; i < data.n; i++)
        if (ind[i]) { 
            w += data.items[i].first; 
            v += data.items[i].second; 
    }
    return (w <= data.max_w) ? v : 0.0;
}
std::vector<int> crossover(const std::vector<int>& p1, const std::vector<int>& p2) {
    int n = p1.size();
    if (n <= 1) return p1;
    int cut = rand() % (n - 1) + 1;
    std::vector<int> child = p1;
    for (int i = cut; i < n; i++) 
        child[i] = p2[i];
    return child;
}

void mutate(std::vector<int>& ind, double rate) {
    for (int &g : ind) {
        if ((double)rand() / RAND_MAX < rate) 
            g = g ^ 1;
    }
}

std::vector<int> tournament(const std::vector<std::vector<int>>& pop, const std::vector<double>& fits) {
    int a = rand() % pop.size();
    int b = rand() % pop.size();
    return (fits[a] >= fits[b]) ? pop[a] : pop[b];
}

double knapsack_get_value(KnapsackData& data, std::vector<int>& sol) {
    return calc_fitness(data, sol);
}

bool knapsack_is_valid(KnapsackData& data, std::vector<int>& sol) {
    return calc_fitness(data, sol) > 0.0 || (calc_fitness(data, sol) == 0.0 && sol == std::vector<int>(data.n, 0));
}

void knapsack_solve(KnapsackData& data, std::vector<int>& out_sol, double& out_val, int max_iters) {
    int POP_SIZE = 50; 
    double MUT_RATE = 0.05; 

    std::vector<std::vector<int>> pop(POP_SIZE, std::vector<int>(data.n, 0));
    for (int i = 0; i < POP_SIZE; i++)
        for (int j = 0; j < data.n; j++)
            pop[i][j] = rand() % 2;

    std::vector<int> best_ind(data.n, 0);
    double best_fit = 0.0;

    for (int gen = 0; gen < max_iters; gen++) {
        std::vector<double> fits(POP_SIZE);
        for (int i = 0; i < POP_SIZE; i++) {
            fits[i] = calc_fitness(data, pop[i]);
            if (fits[i] > best_fit) {
                best_fit = fits[i];
                best_ind = pop[i];
            }
        }

        std::vector<std::vector<int>> new_pop;
        new_pop.reserve(POP_SIZE);
        while ((int) new_pop.size() < POP_SIZE) {
            auto p1 = tournament(pop, fits);
            auto p2 = tournament(pop, fits);
            auto child = crossover(p1, p2);
            mutate(child, MUT_RATE);
            new_pop.push_back(child);
        }
        pop = new_pop;
    }

    out_sol = best_ind;
    out_val = best_fit;
}