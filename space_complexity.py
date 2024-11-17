import random
import math
import itertools
import time
import sys

# Jobs with their respective processing times
jobs = [4, 8, 10, 12, 15, 18, 20, 22]

# Function to calculate the total completion time of a schedule
def calculate_completion_time(schedule):
    completion_time = 0
    for job in schedule:
        completion_time += job
    return completion_time

# Brute Force Approach
def brute_force_schedule(jobs):
    # Space Complexity: O(n!)
    best_schedule = None
    best_time = float('inf')
    
    for schedule in itertools.permutations(jobs):
        current_time = calculate_completion_time(schedule)
        if current_time < best_time:
            best_time = current_time
            best_schedule = schedule
            
    return best_schedule, best_time

# Simulated Annealing Approach
def simulated_annealing(jobs, initial_temp=1000, cooling_rate=0.995, max_iterations=1000):
    # Space Complexity: O(n)
    current_schedule = jobs[:]
    current_time = calculate_completion_time(current_schedule)
    best_schedule = current_schedule[:]
    best_time = current_time
    
    temperature = initial_temp
    
    for iteration in range(max_iterations):
        new_schedule = current_schedule[:]
        i, j = random.sample(range(len(new_schedule)), 2)
        new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
        
        new_time = calculate_completion_time(new_schedule)
        
        delta_energy = new_time - current_time
        
        if delta_energy < 0 or random.uniform(0, 1) < math.exp(-delta_energy / temperature):
            current_schedule = new_schedule
            current_time = new_time
            
            if current_time < best_time:
                best_schedule = current_schedule[:]
                best_time = current_time
        
        temperature *= cooling_rate
    
    return best_schedule, best_time


# Functions to estimate space complexity
def estimate_space_brute_force(jobs):
    # Space complexity: O(n!)
    return math.factorial(len(jobs)) * sys.getsizeof(jobs[0])

def estimate_space_simulated_annealing(jobs):
    # Space complexity: O(n)
    return len(jobs) * sys.getsizeof(jobs[0])

# Main function to run the scheduling algorithms
def main():
    print("Jobs:", jobs)
    
    # Brute Force Space Complexity Estimate
    bf_space = estimate_space_brute_force(jobs)
    print("\nEstimated Space Complexity (Brute Force):", bf_space, "bytes")

    # Simulated Annealing Space Complexity Estimate
    sa_space = estimate_space_simulated_annealing(jobs)
    print("Estimated Space Complexity (Simulated Annealing):", sa_space, "bytes")
    
   
    # Execution of algorithms (optional for verification)


if __name__ == "__main__":
    main()
