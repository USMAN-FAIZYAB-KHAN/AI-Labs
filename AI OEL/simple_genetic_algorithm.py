import random
import numpy as np

# Genetic Algorithm constants
POPULATION_SIZE = 200
TOTAL_GENERATIONS = 1000
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.8
TARGET_STRING = "Hello, World!"  # Target string to match

# Generate a random string of the same length as the target string
def generate_random_string(length):
    return ''.join(np.random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ,.!?"), length))

# Calculate the fitness of an individual by comparing it to the target string
def fitness(individual):
    return np.sum([1 for i, j in zip(individual, TARGET_STRING) if i == j])

# Tournament selection
def select_parents(population, fitness_scores, tournament_size=3):
    parents = []
    for _ in range(2):  # We need two parents
        # Randomly select individuals for the tournament
        tournament_indices = np.random.choice(len(population), size=tournament_size, replace=False)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        # Select the winner (individual with the highest fitness)
        winner_index = tournament_indices[np.argmax(tournament_fitness)]
        parents.append(population[winner_index])
    
    return parents[0], parents[1]

# Crossover operation (single-point crossover)
def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1, parent2

# Mutation operation (randomly change a character in the string)
def mutate(individual):
    if random.random() < MUTATION_RATE:
        mutation_point = random.randint(0, len(individual) - 1)
        individual = list(individual)
        individual[mutation_point] = np.random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ,.!?"))
        return ''.join(individual)
    return individual

# Main genetic algorithm function
def genetic_algorithm():
    # Initialize population with random strings
    population = [generate_random_string(len(TARGET_STRING)) for _ in range(POPULATION_SIZE)]
    
    for generation in range(TOTAL_GENERATIONS):
        # Calculate fitness for each individual in the population
        fitness_scores = [fitness(individual) for individual in population]
        
        # Check if the target string has been matched
        best_individual = population[np.argmax(fitness_scores)]
        if fitness(best_individual) == len(TARGET_STRING):
            return best_individual
        
        print(f"Generation {generation}: {best_individual}, Fitness: {fitness(best_individual)}")
        
        # Create new generation
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = select_parents(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1), mutate(child2)])
        
        population = new_population
    
    # Return the best individual after all generations
    return max(population, key=fitness)

# Run the genetic algorithm and print the result
result = genetic_algorithm()
print(f"Best matched string: {result}")
