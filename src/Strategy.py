from __future__ import annotations
from src.Population import Population
from src.GenerationVisualizer import GenerationVisualizer

import random

from copy import deepcopy

from time import perf_counter

class Strategy:

    @staticmethod
    def run():

        random_seed = 42

        if random_seed is not None:
            random.seed(random_seed)
            print(f"Random seed set to: {random_seed}\n")
        
        else:
            print(f"No random seed provided. Results may vary between runs.\n")

        # -------------------------------------------------
        # INITIAL POPULATION
        # -------------------------------------------------
        pop_size = 30

        population = Population(pop_size=pop_size)
        start_time = perf_counter()
        stagnation_counter = 0

        populations = [population]
        population_creation_times = [0]

        print("\n--- INITIAL POPULATION ---")
        for ind in population.individuals:
            print(ind.permutation, ind.fitness)
        
        print("\n==============================")
        print(f"GENERATION {population.generation}")
        print(f"Best fitness: {population.best_individual.fitness}")
        print(f"Avg fitness: {population.avg_fitness}")
        print(f"average distance for one trip: {population.avg_distance}")
        print(f"Diversity: {population.diversity}")

        # -------------------------------------------------
        # GENERATIONS LOOP (erstmal nur 1-2 zum Testen)
        # -------------------------------------------------
        generations = 5

        for _ in range(generations):

            # -------------------------------------------------
            # 1. SELECTION (Eltern auswählen)
            # -------------------------------------------------
            parents = population.select()

            # TEMP Population nur für Recombination
            parent_population = Population(
                pop_size=pop_size,
                individuals=parents,
                generation=population.generation
            )

            # -------------------------------------------------
            # 2. RECOMBINATION
            # -------------------------------------------------
            parent_population.sort_by_latitude()
            offspring = parent_population.recombine(method="ox")

            # -------------------------------------------------
            # 3. MUTATION
            # -------------------------------------------------
            offspring_population = Population(
                pop_size=pop_size,
                individuals=offspring,
                generation=population.generation + 1
            )

            offspring_population.sort_by_latitude()

            offspring_population.mutate()

            # -------------------------------------------------
            # 4. ELITISMUS + NEUE GENERATION
            # -------------------------------------------------
            population = population.create_next_generation(offspring_population)
            population_creation_times.append(perf_counter() - start_time)
            start_time = perf_counter()

            print("\n==============================")
            print(f"GENERATION {population.generation}")
            print("It took {:.2f} seconds to create this generation.".format(population_creation_times[-1]))
            print(f"Best fitness: {population.best_individual.fitness}")
            print(f"Avg fitness: {population.avg_fitness}")
            print(f"average distance for one trip: {population.avg_distance}")
            print(f"Diversity: {population.diversity}")

            if population.best_individual.fitness >= populations[-1].best_individual.fitness:
                stagnation_counter += 1
            else:
                stagnation_counter = 0

            if stagnation_counter >= 10:
                print("\nStagnated for 10 generations. Stopping early.")
                break
            # -------------------------------------------------
            # SAVE
            # -------------------------------------------------
            populations.append(deepcopy(population))

        # -------------------------------------------------
        # FINAL OUTPUT
        # -------------------------------------------------
        print("\n--- FINAL POPULATION ---")
        for ind in population.individuals:
            print(ind.permutation, ind.fitness)
        
        # -------------------------------------------------
        # EVALUATION
        # -------------------------------------------------
        Population.evaluation(populations[0], population)
        GenerationVisualizer.show_avg_fit(populations=populations)
        GenerationVisualizer.show_best_fit(populations=populations)
        # -------------------------------------------------
        # VISUALIZATION
        # -------------------------------------------------
        GenerationVisualizer.plot_map(population)
