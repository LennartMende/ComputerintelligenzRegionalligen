from __future__ import annotations
from src.Population import Population
from src.GenerationVisualizer import GenerationVisualizer



class Strategy:

    @staticmethod
    def run():

        # -------------------------------------------------
        # INITIAL POPULATION
        # -------------------------------------------------
        pop_size = 20

        population = Population(pop_size=pop_size)

        populations = [population]

        print("\n--- INITIAL POPULATION ---")
        for ind in population.individuals:
            print(ind.permutation, ind.fitness)

        # -------------------------------------------------
        # GENERATIONS LOOP (erstmal nur 1-2 zum Testen)
        # -------------------------------------------------
        generations = 30

        for gen in range(generations):

            print("\n==============================")
            print(f"GENERATION {population.generation}")
            print(f"Best fitness: {population.best_individual.fitness}")
            print(f"Avg fitness: {population.avg_fitness}")
            print(f"Diversity: {population.diversity}")

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

            offspring_population.mutate()

            # -------------------------------------------------
            # 4. ELITISMUS + NEUE GENERATION
            # -------------------------------------------------
            population = population.create_next_generation(offspring_population)

            # -------------------------------------------------
            # SAVE
            # -------------------------------------------------
            import copy
            populations.append(copy.deepcopy(population))

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
