from src.Population import Population





class Strategy:

    @staticmethod
    def run():

        # -------------------------------------------------
        # INITIAL POPULATION
        # -------------------------------------------------
        pop_size = 10

        population = Population(pop_size=pop_size)

        populations = [population]

        print("\n--- INITIAL POPULATION ---")
        for ind in population.individuals:
            print(ind.permutation, ind.fitness)

        # -------------------------------------------------
        # GENERATIONS LOOP (erstmal nur 1-2 zum Testen)
        # -------------------------------------------------
        generations = 10

        for gen in range(generations):

            print(f"\n==============================")
            print(f"GENERATION {population.generation}")
            print(f"Best fitness: {population.best_individual.fitness}")
            print(f"Avg fitness: {population.avg_fitness}")
            print(f"Diversity: {population.diversity}")

            # -------------------------------------------------
            # RECOMBINATION
            # -------------------------------------------------
            offspring = population.recombine(method="ox")

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

        # -------------------------------------------------
        # FINAL OUTPUT
        # -------------------------------------------------
        print("\n--- FINAL POPULATION ---")
        for ind in population.individuals:
            print(ind.permutation, ind.fitness)
