from __future__ import annotations
from src.Population import Population
from src.Individual import Individual
from src.GenerationVisualizer import GenerationVisualizer
from src.Evaluator import Evaluator
from src.LocationProvider import get_location_provider
from dataclasses import dataclass

import random

from copy import deepcopy

from time import perf_counter


@dataclass
class StrategyCfg:
    pop_size: int
    generations: int
    real_clubs: bool = True
    tournament_size: int = 3
    number_of_points: int = 80
    leagues: int = 4
    stagnation_counter_limit: int = 1000
    eval_rounds: int = 40
    draw_map: bool = True


class Strategy:

    @staticmethod
    def parse_permutation_space_separated(input_str: str) -> list[int]:
        return [int(x) for x in input_str.strip().split()]
    
    @staticmethod
    def evaluate_manual_input(input_str: str, use_real_clubs: bool = True):
        # 1. String → Liste
        permutation = Strategy.parse_permutation_space_separated(input_str)

        # 2. Create LocationProvider
        location_provider = get_location_provider(use_real_clubs=use_real_clubs, n=len(permutation))

        # 3. Individual erzeugen
        individual = Individual.from_permutation(permutation, location_provider=location_provider)

        # 4. Fitness berechnen (falls noch nicht passiert)
        fitness = individual.fitness

        # 5. Ausgabe
        print("\n--- MANUAL FITNESS CHECK ---")
        print("Permutation:", individual.permutation)
        print("Fitness: \n\n", fitness)

    @staticmethod
    def run(strategyCfg: StrategyCfg):
        pop_size = strategyCfg.pop_size
        generations = strategyCfg.generations
        leagues = strategyCfg.leagues
        real_clubs = strategyCfg.real_clubs
        number_of_points = strategyCfg.number_of_points
        stagnation_counter_limit = strategyCfg.stagnation_counter_limit
        tournament_size=strategyCfg.tournament_size

        random_seed = 42

        if random_seed is not None:
            random.seed(random_seed)
            print(f"Random seed set to: {random_seed}\n")
        
        else:
            print(f"No random seed provided. Results may vary between runs.\n")

        # -------------------------------------------------
        # CREATE LOCATION PROVIDER
        # -------------------------------------------------
        print(f"\n[DEBUG Strategy] run() called with real_clubs={real_clubs}, number_of_points={number_of_points}")
        location_provider = get_location_provider(use_real_clubs=real_clubs, n=number_of_points)
        locations = location_provider.get_locations()
        print(f"[DEBUG Strategy] Location provider created. Got {len(locations)} locations.")
        print(f"[DEBUG Strategy] First 3 location IDs: {list(locations.keys())[:3]}")
        print(f"[DEBUG Strategy] First location value: {list(locations.values())[0]}")

        # -------------------------------------------------
        # INITIAL POPULATION
        # -------------------------------------------------
        population = Population(pop_size=pop_size, leagues=leagues, tournament_size=tournament_size, location_provider=location_provider)
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
        for _ in range(generations- 1):

            # -------------------------------------------------
            # 1. SELECTION (Eltern auswählen)
            # -------------------------------------------------
            selection_time = perf_counter()
            parents = population.select()
            selection_times.append(perf_counter() - selection_time)

            # TEMP Population nur für Recombination
            parent_population = Population(
                pop_size=pop_size,
                leagues=leagues,
                individuals=parents,
                generation=population.generation,
                location_provider=location_provider
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
                leagues=leagues,
                individuals=offspring,
                generation=population.generation + 1,
                location_provider=location_provider
            )

            
            offspring_population.sort_by_latitude()

            mutation_time = perf_counter()
            offspring_population.mutate()
            mutation_times.append(perf_counter() - mutation_time)

            # -------------------------------------------------
            # 4. ELITISMUS + NEUE GENERATION
            # -------------------------------------------------
            population = population.create_next_generation(offspring_population=offspring_population, leagues=leagues)
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

            if stagnation_counter >= stagnation_counter_limit:
                print("\nStagnated for {} generations. Stopping early.".format(stagnation_counter_limit))
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
    def run_evaluation(strategyCfg: StrategyCfg):
        pop_size = strategyCfg.pop_size
        generations = strategyCfg.generations
        leagues = strategyCfg.leagues
        real_clubs = strategyCfg.real_clubs
        number_of_points = strategyCfg.number_of_points
        stagnation_counter_limit = strategyCfg.stagnation_counter_limit
        tournament_size=strategyCfg.tournament_size
        eval_rounds=strategyCfg.eval_rounds
        draw_map=strategyCfg.draw_map

        eval_populations = []
        optimization_runs = []

        for random_seed in range(1,eval_rounds + 1):
        
            if random_seed is not None:
                random.seed(random_seed)
                print(f"Random seed set to: {random_seed}\n")
            
            else:
                print(f"No random seed provided. Results may vary between runs.\n")

            # -------------------------------------------------
            # CREATE LOCATION PROVIDER
            # -------------------------------------------------
            location_provider = get_location_provider(use_real_clubs=real_clubs, n=number_of_points)

            # -------------------------------------------------
            # INITIAL POPULATION
            # -------------------------------------------------
            population = Population(leagues=leagues, pop_size=pop_size, tournament_size=tournament_size, location_provider=location_provider)
            start_time = perf_counter()
            stagnation_counter = 0

            populations = [population]
            population_creation_times = [0]
            selection_times = [0]
            recombination_times = [0]
            mutation_times = [0]

            
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
                    leagues=leagues,
                    individuals=parents,
                    generation=population.generation,
                    location_provider=location_provider
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
                    leagues=leagues,
                    individuals=offspring,
                    generation=population.generation + 1,
                    location_provider=location_provider
                )

                offspring_population.sort_by_latitude()

                mutation_time = perf_counter()
                offspring_population.mutate()
                mutation_times.append(perf_counter() - mutation_time)

                # -------------------------------------------------
                # 4. ELITISMUS + NEUE GENERATION
                # -------------------------------------------------
                population = population.create_next_generation(leagues=leagues, offspring_population=offspring_population)
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

                
                if stagnation_counter >= stagnation_counter_limit:
                    print("\nStagnated for {} generations. Stopping early.".format(stagnation_counter_limit))
                    break
                # -------------------------------------------------
                # SAVE
                # -------------------------------------------------
                populations.append(deepcopy(population))

            # -------------------------------------------------
            # FINAL OUTPUT
            # -------------------------------------------------
            optimization_runs.append(populations)
            eval_populations.append(population)
        
        # compare all poopulation's final results
        Population.multiple_populations_evaluation(populations=eval_populations)
        individual_population_pairs = [
            (pop.best_individual, pop)
            for pop in populations
        ]

        # find best individual and draw the map
        best_individual, best_population = min(
            individual_population_pairs,
            key=lambda pair: pair[0].fitness
        )

        print("\n" * 3)
        print("-" * 80)
        print("Evaluator-Evaluation mit print:")
        Evaluator.eval_printed(populations=eval_populations)

        if draw_map:
            GenerationVisualizer.plot_map(best_population)

        # detailed evaluation of ALL population's generations
        Evaluator.eval_as_csvs(strategyCfg=strategyCfg, optimization_runs=optimization_runs)

    @staticmethod
    def run_eval_with_different_configs(strategy_cfg_list: list[StrategyCfg]):
        for i in range(0, len(strategy_cfg_list)):
            if strategy_cfg_list[len(strategy_cfg_list) - 1].draw_map == True:
                strategy_cfg_list[i].draw_map = (True if i == len(strategy_cfg_list) - 1 else False)
            else:
                strategy_cfg_list[i].draw_map = False
            Strategy.run_evaluation(strategy_cfg_list[i])
