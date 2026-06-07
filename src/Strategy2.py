from __future__ import annotations
from src.Population import Population
from src.GenerationVisualizer import GenerationVisualizer



class Strategy:

    @staticmethod
    def run():

        # -------------------------------------------------
        # INITIAL POPULATION
        # -------------------------------------------------
        pop_size = 10 # 20

        population = Population(pop_size=pop_size)

        populations = [population]

        print("\n--- INITIAL POPULATION ---")
        for ind in population.individuals:
            print(ind.permutation, ind.fitness)

        # -------------------------------------------------
        # GENERATIONS LOOP (erstmal nur 1-2 zum Testen)
        # -------------------------------------------------
        generations = 10 # 30

        for gen in range(generations):

            print(f"\n==============================")
            print(f"GENERATION {population.generation}")
            print(f"Best fitness: {population.best_individual.fitness}")
            print(f"Avg fitness: {population.avg_fitness}")
            print(f"Diversity: {population.diversity}")

            # -------------------------------------------------
            # RECOMBINATION
            # -------------------------------------------------
            population.sort_by_latitude() # sort the groups by their average latitude (north to south)
            offspring = population.recombine(method="ox")
            population.sort_by_latitude() # sort the groups by their average latitude (north to south)

            # WICHTIG: neue Population erzeugen!
            population = Population(
                pop_size=pop_size,
                individuals=[
                    type(population.individuals[0]).from_permutation(child)
                    for child in offspring
                ],
                generation=population.generation + 1
            )

            # -------------------------------------------------
            # MUTATION
            # -------------------------------------------------
            population.mutate()

            # -------------------------------------------------
            # ELITISM
            # -------------------------------------------------
            # population.elitism(population)

            # -------------------------------------------------
            # SELECTION
            # -------------------------------------------------
            selected = population.select()

            # -------------------------------------------------
            # SAVE POPULATION
            # -------------------------------------------------
            populations.append(population)

            # -------------------------------------------------
            # CREATE NEW POPULATION
            # -------------------------------------------------
            population = Population(
                pop_size=pop_size,
                individuals=selected,
                generation=population.generation
            )

            populations.append(population) # warum 2-mal? Einmal nach Selektion, einmal nach Erzeugung der neuen Population?

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
