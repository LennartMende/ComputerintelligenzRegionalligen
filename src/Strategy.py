from __future__ import annotations
from src.Population import Population
from src.Individual import Individual
from src.GenerationVisualizer import GenerationVisualizer

import random

from copy import deepcopy

from time import perf_counter

import argparse
parser = argparse.ArgumentParser()
parser.parse_args()

class Strategy:

    @staticmethod
    def parse_permutation_space_separated(input_str: str) -> list[int]:
        return [int(x) for x in input_str.strip().split()]
    
    @staticmethod
    def evaluate_manual_input(input_str: str):
        # 1. String → Liste
        permutation = Strategy.parse_permutation_space_separated(input_str)

        # 2. Individual erzeugen
        individual = Individual.from_permutation(permutation)

        # 3. Fitness berechnen (falls noch nicht passiert)
        fitness = individual.fitness

        # 4. Ausgabe
        print("\n--- MANUAL FITNESS CHECK ---")
        print("Permutation:", individual.permutation)
        print("Fitness: \n\n", fitness)

    @staticmethod
    def run(pop_size: int, generations: int, leagues: int, real_clubs: bool, number_of_points: int = 80):

        random_seed = 42

        if random_seed is not None:
            random.seed(random_seed)
            print(f"Random seed set to: {random_seed}\n")
        
        else:
            print(f"No random seed provided. Results may vary between runs.\n")

        # -------------------------------------------------
        # INITIAL POPULATION
        # -------------------------------------------------
        population = Population(pop_size=pop_size, leagues=leagues)
        start_time = perf_counter()
        stagnation_counter = 0

        populations = [population]
        population_creation_times = [0]
        selection_times = [0]
        recombination_times = [0]
        mutation_times = [0]

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
        for _ in range(generations):

            # -------------------------------------------------
            # 1. SELECTION (Eltern auswählen)
            # -------------------------------------------------
            selection_time = perf_counter()
            parents = population.select()
            selection_times.append(perf_counter() - selection_time)

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
            recombination_time = perf_counter()
            offspring = parent_population.recombine(method="ox")
            recombination_times.append(perf_counter() - recombination_time)

            # -------------------------------------------------
            # 3. MUTATION
            # -------------------------------------------------
            offspring_population = Population(
                pop_size=pop_size,
                individuals=offspring,
                generation=population.generation + 1
            )

            offspring_population.sort_by_latitude()

            mutation_time = perf_counter()
            offspring_population.mutate()
            mutation_times.append(perf_counter() - mutation_time)

            # -------------------------------------------------
            # 4. ELITISMUS + NEUE GENERATION
            # -------------------------------------------------
            population = population.create_next_generation(offspring_population)
            population_creation_times.append(perf_counter() - start_time)
            time_per_individual = population_creation_times[-1] / pop_size
            start_time = perf_counter()

            print("\n==============================")
            print(f"GENERATION {population.generation}")
            print("It took {:.2f} seconds to create this generation.".format(population_creation_times[-1]))
            print("Time per individual: {:.6f} seconds".format(time_per_individual))
            print(f"Best fitness: {population.best_individual.fitness}")
            print(f"Avg fitness: {population.avg_fitness}")
            print(f"average distance for one trip: {population.avg_distance}")
            print(f"Diversity: {population.diversity}")

            if population.best_individual.fitness >= populations[-1].best_individual.fitness:
                stagnation_counter += 1
            else:
                stagnation_counter = 0

            if stagnation_counter >=900:
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
        print("all times evaluated:")
        Population.time_evaluation(times=population_creation_times, pop_size=pop_size)
        Population.time_evaluation(times=selection_times, pop_size=pop_size, step_name="selection")
        Population.time_evaluation(times=recombination_times, pop_size=pop_size, step_name="recombination")
        Population.time_evaluation(times=mutation_times, pop_size=pop_size, step_name="mutation")
        # graphical analysis
        GenerationVisualizer.show_avg_fit(populations=populations)
        GenerationVisualizer.show_best_fit(populations=populations)
        # -------------------------------------------------
        # VISUALIZATION OF THE BEST SOLUTION
        # -------------------------------------------------
        GenerationVisualizer.plot_map(population)
        
    

    # evaluation for multiple populations:
    @staticmethod
    def run_evaluation(eval_rounds: int, draw_map: bool, pop_size: int, generations: int):
        eval_populations = []
        for random_seed in range(1,eval_rounds + 1):
        
            if random_seed is not None:
                random.seed(random_seed)
                print(f"Random seed set to: {random_seed}\n")
            
            else:
                print(f"No random seed provided. Results may vary between runs.\n")

            # -------------------------------------------------
            # INITIAL POPULATION
            # -------------------------------------------------
            population = Population(pop_size=pop_size)
            start_time = perf_counter()
            stagnation_counter = 0

            populations = [population]
            population_creation_times = [0]
            selection_times = [0]
            recombination_times = [0]
            mutation_times = [0]

            # print("\n--- INITIAL POPULATION ---")
            # for ind in population.individuals:
            #     print(ind.permutation, ind.fitness)
            
            print("\n==============================")
            print(f"GENERATION {population.generation}")
            print(f"Best fitness: {population.best_individual.fitness}")
            print(f"Avg fitness: {population.avg_fitness}")
            print(f"average distance for one trip: {population.avg_distance}")
            print(f"Diversity: {population.diversity}")

            # -------------------------------------------------
            # GENERATIONS LOOP (erstmal nur 1-2 zum Testen)
            # -------------------------------------------------
            for _ in range(generations):

                # -------------------------------------------------
                # 1. SELECTION (Eltern auswählen)
                # -------------------------------------------------
                selection_time = perf_counter()
                parents = population.select()
                selection_times.append(perf_counter() - selection_time)

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
                recombination_time = perf_counter()
                offspring = parent_population.recombine(method="ox")
                recombination_times.append(perf_counter() - recombination_time)

                # -------------------------------------------------
                # 3. MUTATION
                # -------------------------------------------------
                offspring_population = Population(
                    pop_size=pop_size,
                    individuals=offspring,
                    generation=population.generation + 1
                )

                offspring_population.sort_by_latitude()

                mutation_time = perf_counter()
                offspring_population.mutate()
                mutation_times.append(perf_counter() - mutation_time)

                # -------------------------------------------------
                # 4. ELITISMUS + NEUE GENERATION
                # -------------------------------------------------
                population = population.create_next_generation(offspring_population)
                population_creation_times.append(perf_counter() - start_time)
                time_per_individual = population_creation_times[-1] / pop_size
                start_time = perf_counter()

                print("\n==============================")
                print(f"GENERATION {population.generation}")
                print("It took {:.2f} seconds to create this generation.".format(population_creation_times[-1]))
                print("Time per individual: {:.6f} seconds".format(time_per_individual))
                print(f"Best fitness: {population.best_individual.fitness}")
                print(f"Avg fitness: {population.avg_fitness}")
                print(f"average distance for one trip: {population.avg_distance}")
                print(f"Diversity: {population.diversity}")

                if population.best_individual.fitness >= populations[-1].best_individual.fitness:
                    stagnation_counter += 1
                else:
                    stagnation_counter = 0

                
                if stagnation_counter >=900:
                    print("\nStagnated for 900 generations. Stopping early.")
                    break
                # -------------------------------------------------
                # SAVE
                # -------------------------------------------------
                populations.append(deepcopy(population))

            # -------------------------------------------------
            # FINAL OUTPUT
            # -------------------------------------------------
            # print("\n--- FINAL POPULATION ---")
            # for ind in population.individuals:
            #     print(ind.permutation, ind.fitness)

            eval_populations.append(population)
        

        Population.multiple_populations_evaluation(populations=eval_populations)
        individual_population_pairs = [
            (pop.best_individual, pop)
            for pop in populations
        ]
        best_individual, best_population = min(
            individual_population_pairs,
            key=lambda pair: pair[0].fitness
        )

        if draw_map:
            GenerationVisualizer.plot_map(best_population)