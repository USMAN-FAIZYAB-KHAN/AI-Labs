import numpy as np
from PIL import Image
import base64
from io import BytesIO

POPULATION_SIZE = 350
TOTAL_GENERATIONS = 2000
MUTATION_RATE = 0.0001
CROSSOVER_RATE = 0.9

# Load target image and convert it to a binary (black-and-white) numpy array
def load_image(image_data):
    image_data = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_data)).convert('1')
    image = image.resize((128, 128))
    return np.array(image).astype(np.uint8)

# Initialize the population with random binary images
def initialize_population(population_size, shape):
    return np.random.randint(2, size=(population_size, *shape), dtype=np.uint8)

# Calculate fitness as the number of matching pixels
def fitness(individual, target):
    return np.sum(individual == target)

# Tournament selection
def select_parents(population, fitness_scores, tournament_size=3):
    parents = []
    for _ in range(2):  # We need two parents
        # Randomly select individuals for the tournament
        tournament_indices = np.random.choice(len(population), size=tournament_size, replace=False)
        tournament_fitness = fitness_scores[tournament_indices]
        # Select the winner (individual with the highest fitness)
        winner_index = tournament_indices[np.argmax(tournament_fitness)]
        parents.append(population[winner_index])
    
    return parents[0], parents[1]


# Crossover operation (uniform crossover)
def crossover(parent1, parent2, crossover_rate=0.7):
    if np.random.rand() < crossover_rate:
        mask = np.random.randint(2, size=parent1.shape, dtype=bool)
        child1 = np.where(mask, parent1, parent2)
        child2 = np.where(mask, parent2, parent1)
        return child1, child2
    else:
        return parent1, parent2

# Mutation operation (flips a percentage of bits)
def mutate(individual, mutation_rate=0.01):
    mutation_mask = np.random.rand(*individual.shape) < mutation_rate
    individual[mutation_mask] = 1 - individual[mutation_mask]  # Flip bits
    return individual