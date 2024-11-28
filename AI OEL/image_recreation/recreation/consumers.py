from channels.generic.websocket import AsyncWebsocketConsumer
import json
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import asyncio
from .genetic_algorithm import *

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        target = load_image(data['image_data'])

        # Initialize population and track the best individual
        population = initialize_population(POPULATION_SIZE, target.shape)
        best_fitness = 0
        best_individual = None

        for generation in range(1, TOTAL_GENERATIONS+1):
            # Calculate fitness for each individual
            fitness_scores = np.array([fitness(individual, target) for individual in population])

            # Track the best solution
            max_fitness = np.max(fitness_scores)
            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_individual = population[np.argmax(fitness_scores)].copy()

            print(f"Generation {generation} - Best Fitness: {best_fitness}")

            # Visualize and send updates every 100 generations
            best_individual_image = Image.fromarray(best_individual * 255)
            buffered = BytesIO()
            best_individual_image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            await self.send_progress_update(generation, img_base64)
            await asyncio.sleep(0.1)

            # Early stopping if a perfect match is found
            if best_fitness == target.size:
                print("Perfect match found!")
                break

            # Generate the new population
            new_population = []
            for _ in range(POPULATION_SIZE // 2):
                # Select parents using roulette wheel selection
                parent1, parent2 = select_parents(population, fitness_scores)

                # Perform crossover with specified rate
                child1, child2 = crossover(parent1, parent2, CROSSOVER_RATE)

                # Apply mutation to each child
                child1 = mutate(child1, MUTATION_RATE)
                child2 = mutate(child2, MUTATION_RATE)

                # Add the new children to the population
                new_population.extend([child1, child2])

            # Update the population for the next generation
            population = np.array(new_population)

        
        # send final image
        await self.send_progress_update(generation, img_base64, final=True)


    async def send_progress_update(self, generation, image_base64, final=False):
        print(f"Sending progress update for generation {generation}")
        if final:
            await self.send(text_data=json.dumps({
                'generation': generation,
                'image_data': image_base64,
                'final': True,
            }))
        else:
            await self.send(text_data=json.dumps({
                'generation': generation,
                'image_data': image_base64,
            }))
