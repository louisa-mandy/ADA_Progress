import random
import math
import itertools
import time

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
    # Time Complexity: O(n!)
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
    # Time Complexity: O(max_iterations * n)
    current_schedule = jobs[:]
    current_time = calculate_completion_time(current_schedule)
    best_schedule = current_schedule[:]
    best_time = current_time
    
    temperature = initial_temp
    
    for iteration in range(max_iterations):
        # Generate a new schedule by swapping two jobs
        new_schedule = current_schedule[:]
        i, j = random.sample(range(len(new_schedule)), 2)
        new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
        
        new_time = calculate_completion_time(new_schedule)
        
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


    # Initialize population
    population = [create_schedule() for _ in range(population_size)]
    
    best_schedule = None
    best_time = float('inf')
    
    for generation in range(generations):
        # Evaluate fitness
        population = sorted(population, key=calculate_completion_time)
        
        # Update best schedule found
        current_best_time = calculate_completion_time(population[0])
        if current_best_time < best_time:
            best_time = current_best_time
            best_schedule = population[0]
        
        # Create new generation
        new_population = population[:10]  # Elitism: keep the best 10
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:50], k=2)  # Select from the top 50
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)
        
        population = new_population
    
    return best_schedule, best_time

# Main function to run the scheduling algorithms
def main():
    print("Jobs:", jobs)
    
    # Brute Force Approach
    start_time = time.time()
    bf_schedule, bf_time = brute_force_schedule(jobs)
    bf_duration = time.time() - start_time
    bf_duration_ns = bf_duration * 1e9  # Convert to nanoseconds
    print("\nBrute Force Schedule:", bf_schedule)
    print("Total Completion Time (Brute Force):", bf_time)
    print("Execution Time (Brute Force):", bf_duration_ns, "nanoseconds")
    print("Expected Time Complexity: O(n!) =", math.factorial(len(jobs)), "operations")

    # Simulated Annealing Approach
    start_time = time.time()
    sa_schedule, sa_time = simulated_annealing(jobs)
    sa_duration = time.time() - start_time
    sa_duration_ns = sa_duration * 1e9  # Convert to nanoseconds
    print("\nSimulated Annealing Schedule:", sa_schedule)
    print("Total Completion Time (Simulated Annealing):", sa_time)
    print("Execution Time (Simulated Annealing):", sa_duration_ns, "nanoseconds")
    print("Expected Time Complexity: O(max_iterations * n) =", 1000 * len(jobs), "operations")



if __name__ == "__main__":
    main()
