import random
import math
import itertools
import time
import sys

# Jobs with their respective processing times
jobs = [1, 2, 3, 4]  # You can change the job list size here
# jobs = [2, 1, 3, 4]
# jobs = [3, 2, 1, 4]
# jobs = [4, 2, 3, 1]
# jobs = [1, 3, 2, 4]
# jobs = [1, 4, 3, 2]
# jobs = [1, 2, 4, 3]

# Function to calculate the total completion time of a schedule
def calculate_completion_time(schedule):
    return sum(schedule)

# Brute Force Approach with Memoization
def brute_force_schedule(jobs):
    # Space Complexity: O(n!)
    # Time Complexity: O(n * n!)
    best_schedule = None
    best_time = float('inf')
    
    memo = {}  # Cache to store completion times of previously encountered permutations
    
    for schedule in itertools.permutations(jobs):
        # If this schedule has been encountered before, use the cached completion time
        if schedule in memo:
            current_time = memo[schedule]
        else:
            current_time = calculate_completion_time(schedule)
            memo[schedule] = current_time
        
        if current_time < best_time:
            best_time = current_time
            best_schedule = schedule
            
    return best_schedule, best_time

# Simulated Annealing Approach with Caching
def simulated_annealing(jobs, initial_temp=1000, cooling_rate=0.995, max_iterations=1000):
    # Space Complexity: O(n)
    # Time Complexity: O(m * n)
    current_schedule = jobs[:]
    current_time = calculate_completion_time(current_schedule)
    best_schedule = current_schedule[:]
    best_time = current_time
    
    temperature = initial_temp
    cache = {}  # Cache to store previously calculated schedules' completion times
    
    for iteration in range(max_iterations):
        # Generate a new schedule by swapping two jobs
        new_schedule = current_schedule[:]
        i, j = random.sample(range(len(new_schedule)), 2)
        new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
        
        # Check if we have cached the completion time for this new schedule
        if tuple(new_schedule) in cache:
            new_time = cache[tuple(new_schedule)]
        else:
            new_time = calculate_completion_time(new_schedule)
            cache[tuple(new_schedule)] = new_time
        
        # Calculate the change in energy
        delta_energy = new_time - current_time
        
        # Decide whether to accept the new schedule
        if delta_energy < 0 or random.uniform(0, 1) < math.exp(-delta_energy / temperature):
            current_schedule = new_schedule
            current_time = new_time
            
            # Update best schedule found
            if current_time < best_time:
                best_schedule = current_schedule[:]
                best_time = current_time
        
        # Cool down the temperature
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
    
    # Brute Force Approach with Memoization
    start_time = time.perf_counter()
    bf_schedule, bf_time = brute_force_schedule(jobs)
    bf_duration = (time.perf_counter() - start_time) * 1e9  # converting results to nanoseconds
    
    # to prevent 0.0 nanoseconds results 
    bf_duration_ns = max(bf_duration, 1.0)
    print("\nBrute Force Schedule:", bf_schedule)
    print("Total Completion Time (Brute Force):", bf_time)
    print("Execution Time (Brute Force):", bf_duration_ns, "nanoseconds")
    print("Expected Time Complexity: O(n * n!) =", len(jobs) * math.factorial(len(jobs)), "operations")
    
    # Simulated Annealing Approach with Caching
    start_time = time.perf_counter()
    sa_schedule, sa_time = simulated_annealing(jobs)
    sa_duration = (time.perf_counter() - start_time) * 1e9  # Convert to nanoseconds
    
    sa_duration_ns = max(sa_duration, 1.0)
    print("\nSimulated Annealing Schedule:", sa_schedule)
    print("Total Completion Time (Simulated Annealing):", sa_time)
    print("Execution Time (Simulated Annealing):", sa_duration_ns, "nanoseconds")
    print("Expected Time Complexity: O(m * n) =", 1000 * len(jobs), "operations")
    
    # Space Complexity Estimates
    bf_space = estimate_space_brute_force(jobs)
    print("\nEstimated Space Complexity (Brute Force):", bf_space, "bytes")
    
    sa_space = estimate_space_simulated_annealing(jobs)
    print("Estimated Space Complexity (Simulated Annealing):", sa_space, "bytes")
    
if __name__ == "__main__":
    main()
