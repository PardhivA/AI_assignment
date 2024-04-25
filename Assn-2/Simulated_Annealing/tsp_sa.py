import random
import time
import json
import os
import numpy as np
import math

# Get the total distance of the given tour
def tour_distance(tour, dist_matrix):
    tour_shifted = np.roll(tour, -1)
    return np.sum(dist_matrix[tour, tour_shifted])

# for final iter
def tour_distance_final_iter(tour, dist_matrix):
    tour_shifted = np.roll(tour, -1)
    return dist_matrix[tour, tour_shifted].tolist(), np.sum(dist_matrix[tour, tour_shifted])


# A neighbourhood function which mirror rotates a subset of the given tour and return it
def two_opt(tour, i, j):
    new_tour = np.concatenate((tour[:i], tour[i:j+1][::-1], tour[j+1:]))
    return new_tour

# A neighbourhood function which swaps two segments in a given tour. E
def three_opt(tour, i, j, k):
    new_tour = np.concatenate((tour[:i], tour[j:k], tour[i:j], tour[k:]))
    return new_tour

# A neighbourhood function which swaps two cities' position in a given tour. E
def four_opt(tour, k=150):
    new_tour = tour.copy()
    for _ in range(k):
        i, j = sorted(random.sample(range(1, len(tour)-1), 2))
        new_tour = two_opt(new_tour, i, j)
    return new_tour




# Followed the usual Simulated Annealing Pseudo Code 
def CustomSA(tour, dist_matrix):
    alpha = 0.99999 # temparature control hyper parameter
    initial_temp = 100000
    tmin = 1
    temp = initial_temp
    energy_init = tour_distance(tour,dist_matrix)
    while(temp > tmin):
        i, j = sorted(random.sample(range(1, len(tour)-1), 2))
        new_tour = two_opt(tour, i,j) 
        new_energy = tour_distance(new_tour, dist_matrix)
        deltaE = new_energy-energy_init
        if random.uniform(0, 1) <= math.exp(-float(deltaE) / float(temp)):
            tour = new_tour
            energy_init = new_energy
        temp = alpha*temp

    return tour




with open("Simulated_Annealing/benchmark_dataset/optimal_solutions.json", "r") as json_file:
    optimal_solutions = json.load(json_file)

benchmark_dir = "Simulated_Annealing/benchmark_dataset"

txt_files = [f for f in os.listdir(benchmark_dir) if f.endswith('.txt')]

results = []
counter = 1

for txt_file in txt_files:
    print(f"Test: {counter}/{len(txt_files)}")
    matrix_number = txt_file.split('.')[0]

    with open(os.path.join(benchmark_dir, txt_file), "r") as file:
        lines = file.readlines()
        dist_matrix = np.array([list(map(float, line.split())) for line in lines])

    initial_tour = random.sample(range(len(dist_matrix)), len(dist_matrix))
    best_tour = CustomSA(initial_tour, dist_matrix)
    
    results.append({
        "Test": matrix_number,
        "Number of cities": len(dist_matrix),
        "Total distance by VNS": tour_distance(best_tour, dist_matrix),
        "Optimal distance": optimal_solutions[matrix_number]["optimal_solution"],
        "Score": (optimal_solutions[matrix_number]["optimal_solution"] / tour_distance(best_tour, dist_matrix)) * 100,
           "Best Tour" : best_tour.tolist(),
        "Corresponding Distances": tour_distance_final_iter(best_tour, dist_matrix)

    })
    counter += 1

print("Done!")
    
logs = {
    "Average score": np.mean([result["Score"] for result in results]),
    "Results": results
}

with open("Simulated_Annealing/logs/results_sa.json", "w") as json_file:
    json.dump(logs, json_file, indent=4)