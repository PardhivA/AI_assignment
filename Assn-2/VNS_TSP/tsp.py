import random
import time
import json
import os
import numpy as np

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

# Generating a new tour based on given neighbourhood function
def local_search(tour, dist_matrix, operator, k):
    better_solution_found = True
    original_distance = tour_distance(tour, dist_matrix)
    
    while better_solution_found:
        better_solution_found = False
        if k == 0:
            for i in range(1, len(tour) - 1):
                for j in range(i+1, len(tour)):
                    if j-i == 1: continue
                    new_tour = operator(tour, i, j)
                    new_distance = tour_distance(new_tour, dist_matrix)
                    if new_distance < original_distance:
                        tour = new_tour
                        original_distance = new_distance
                        better_solution_found = True
        if k ==1:
            for i in range(1, len(tour) - 2):
                for j in range(i+1, len(tour)-1):
                    if j-i == 1: continue
                    for l in  range(j+1,len(tour)):
                        if l-j == 1: continue
                        new_tour = operator(tour, i, j,l)
                        new_distance = tour_distance(new_tour, dist_matrix)
                        if new_distance < original_distance:
                            tour = new_tour
                            original_distance = new_distance
                            better_solution_found = True
        if k == 2:
            new_tour = operator(tour)
            new_distance = tour_distance(new_tour, dist_matrix)
            if new_distance < original_distance:
                tour = new_tour
                # original_distance = new_distance
            
                    
    return tour



# Our Custom VNS which runs till the newly calculated tour is no different than the original one with very neighbourhood function. If a new one is found, it starts again with the new one.
def customVns(tour, dist_matrix,operators, k_max=2):
    k = 0
    # total_exploration_time = 0
    # total_exploitation_time = 0
    while k <= k_max:
        new_tour = local_search(tour, dist_matrix, operators[k],k)
        if tour_distance(new_tour, dist_matrix) < tour_distance(tour, dist_matrix):
            tour = new_tour
            k = 1
        else:
            k += 1
    return tour



with open("VNS_TSP/benchmark_dataset/optimal_solutions.json", "r") as json_file:
    optimal_solutions = json.load(json_file)

benchmark_dir = "VNS_TSP/benchmark_dataset"

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
    neighbourhood_structres  = [two_opt, three_opt, four_opt]
    best_tour = customVns(initial_tour, dist_matrix, neighbourhood_structres,2)
    
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

with open("VNS_TSP/logs/results_vns.json", "w") as json_file:
    json.dump(logs, json_file, indent=4)