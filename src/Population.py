from __future__ import annotations
import random
from typing import List, Tuple
from statistics import stdev, mean

from src.Individual import Individual




class Population:
    """
    Represents a population in an evolutionary algorithm.

    Attributes:
        generation (int): Current generation number
        individuals (List[Individual]): List of individuals in the population
        crossover_rate (float): Probability of crossover
        mutation_swaps (int): Number of swaps applied during mutation
    """

    def __init__(self,
        pop_size:int,
        individuals: List[Individual] | None = None,
        generation: int = 1,
        recombination_rate: float = 1.0,
        tournament_size: int = 5,
        mutation_swaps: int = 3,
    ):
        """
        Initializes the population.

        Args:
            pop_size: Size of the population
            individuals: Optional list of individuals (used for next generation)
            generation: Generation index
            recombination_rate: Probability of recombination
            tournament_size: Size of the tournament for selection
            mutation_swaps: Number of swaps in mutation
        """

        self.pop_size = pop_size
        self.generation = generation
        self.recombination_rate = recombination_rate
        self.tournament_size = tournament_size
        self.mutation_swaps = mutation_swaps

        # Create initial population or reuse given individuals
        if individuals is None:
            self.individuals = [Individual() for _ in range(pop_size)]
        else:
            self.individuals = individuals

        # for debugging purposes
        self.individuals_after_recombination = []
        self.individuals_after_mutation = []
        self.individuals_after_selection = []

    # -------------------------------------------------
    # Properties
    # -------------------------------------------------
    @property
    def fitnesses(self) -> List[float]:
        """Returns the fitness values of all individuals."""
        return [ind.fitness for ind in self.individuals]

    @property
    def best_individual(self) -> Individual:
        """Returns the best individual in the population."""
        return min(self.individuals, key=lambda ind: ind.fitness)

    @property
    def worst_individual(self) -> Individual:
        """Returns the worst individual in the population."""
        return max(self.individuals, key=lambda ind: ind.fitness)

    @property
    def total_fitness(self) -> float:
        """Returns the total fitness of the population."""
        return sum(self.fitnesses)

    @property
    def avg_fitness(self) -> float:
        """Returns the average fitness."""
        return self.total_fitness / self.pop_size
    
    @property
    def avg_distance(self) -> float:
        """Returns the average distance for one trip."""
        return self.best_individual.fitness / (80 * 19)

    @property
    def diversity(self) -> float:
        """Returns a simple diversity metric based on fitness standard deviation."""
        if len(self.individuals) < 2:
            return 0.0
        return stdev(self.fitnesses)

    

    
    # def recombine(self, method: str = "pmx") -> List[Individual]:
    #     """
    #     Applies recombination to the current population.

    #     Args:
    #         method: "pmx" or "ox"

    #     Returns:
    #         List of offspring individuals
    #     """

    #     if method == "pmx":
    #         self.individuals_after_recombination = self._recombine_pmx()
    #     elif method == "ox":
    #         self.individuals_after_recombination = self._recombine_ox()
    #     else:
    #         raise ValueError(f"Unknown recombination method: {method}")

    #     return self.individuals_after_recombination



    # ------------------------------------------------------------
    # PUBLIC METHOD: recombine full population
    # ------------------------------------------------------------
    def recombine(
        self,
        method: str = "ox"
    ) -> List[List[int]]:
        """
        Creates a new population using a recombination method.

        IMPORTANT:
        - For EACH crossover event, TWO RANDOM PARENTS are selected.
        - Parents are NOT paired beforehand.
        """

        new_population = []
        population = self.individuals
        pop_size = len(population)

        # We assume we want same population size again
        # -> so we generate pop_size / 2 crossover events, because each event produces 2 children
        num_crossovers = pop_size // 2

        for _ in range(num_crossovers):

            # --------------------------------------------------------
            # STEP 1: RANDOMLY SELECT TWO PARENTS (with replacement)
            # --------------------------------------------------------
            parent1 = random.choice(population)
            parent2 = random.choice(population)

            # ensure they are not identical references (optional safety)
            while parent2 is parent1 and pop_size > 1:
                parent2 = random.choice(population)

            # --------------------------------------------------------
            # STEP 2: APPLY CROSSOVER OR COPY
            # --------------------------------------------------------
            if random.random() < self.recombination_rate:

                if method == "ox":
                    child1, child2 = self.ox(parent1.permutation, parent2.permutation)

                elif method == "pmx":
                    child1, child2 = self.pmx(parent1.permutation, parent2.permutation)

                else:
                    raise ValueError(f"Unknown recombination method: {method}")

            else:
                # no crossover → clone parents
                child1, child2 = parent1.permutation[:], parent2.permutation[:]

            new_population.extend([Individual.from_permutation(child1), Individual.from_permutation(child2)])

        # optional: store result
        self.individuals_after_recombination = new_population

        return new_population


    # ------------------------------------------------------------
    # CORE OX OPERATOR
    # ------------------------------------------------------------
    def ox(
        self,
        parent1: List[int],
        parent2: List[int]
    ) -> Tuple[List[int], List[int]]:
        """
        Order Crossover (OX) implementation for permutation-based problems.
        Produces TWO children per crossover.
        """

        if hasattr(parent1, "permutation"):
            parent1 = parent1.permutation
        if hasattr(parent2, "permutation"):
            parent2 = parent2.permutation

        size = len(parent1)

        # --------------------------------------------------------
        # STEP 1: choose crossover points
        # --------------------------------------------------------
        i, j = sorted(random.sample(range(size), 2))

        # --------------------------------------------------------
        # STEP 2: initialize empty children
        # --------------------------------------------------------
        child1 = [None] * size
        child2 = [None] * size

        # --------------------------------------------------------
        # STEP 3: copy segment from each parent
        # --------------------------------------------------------
        child1[i:j + 1] = parent1[i:j + 1]
        child2[i:j + 1] = parent2[i:j + 1]

        # --------------------------------------------------------
        # STEP 4: fill remaining positions
        # --------------------------------------------------------
        def fill_child(child, parent):
            used = set(child)
            pos = 0

            for gene in parent:
                if gene in used:
                    continue

                while child[pos] is not None:
                    pos = (pos + 1) % size

                child[pos] = gene
                used.add(gene)

        fill_child(child1, parent2)
        fill_child(child2, parent1)

        return child1, child2


    # ------------------------------------------------------------
    # CORE PMX OPERATOR
    # ------------------------------------------------------------
    def pmx(
        self,
        parent1: List[int],
        parent2: List[int]
    ) -> Tuple[List[int], List[int]]:
        """Performs Partially Mapped Crossover (PMX) on two parents to produce two offspring."""

        if hasattr(parent1, "permutation"):
            parent1 = parent1.permutation
        if hasattr(parent2, "permutation"):
            parent2 = parent2.permutation

        # check if parents are of the same length
        size = len(parent1)
        if size != len(parent2):
            raise ValueError("Parents must be of the same length!")

        # randomly select two crossover points
        cut1, cut2 = sorted(random.sample(range(size + 1), 2))

        # create offspring1 with the same length as the parents
        offspring1 = [0] * size

        # Copy the middle section from `parent1`
        offspring1[cut1:cut2] = parent1[cut1:cut2]

        # Copy the rest from `parent2`, resolving conflicts
        for i in (*range(0, cut1), *range(cut2, size)):
            candidate = parent2[i]
            while candidate in parent1[cut1:cut2]:  # handle successive mappings
                candidate = parent2[parent1.index(candidate)]
            offspring1[i] = candidate

        # create offspring2 with the same length as the parents
        offspring2 = [0] * size

        # Copy the middle section from `parent2`
        offspring2[cut1:cut2] = parent2[cut1:cut2]

        # Copy the rest from `parent1`, resolving conflicts
        for i in (*range(0, cut1), *range(cut2, size)):
            candidate = parent1[i]
            while candidate in parent2[cut1:cut2]:  # handle successive mappings
                candidate = parent1[parent2.index(candidate)]
            offspring2[i] = candidate

        return offspring1, offspring2

    

    def mutate(self):
        for ind in self.individuals:

            if self.generation < 50:
                ind.mutation(self.mutation_swaps)

            else:
                ind.mutation_from_location_hardcore(max_swaps=self.mutation_swaps)

    

    # ------------------------------------------------------------
    # SELECT ONE INDIVIDUAL (TOURNAMENT)
    # ------------------------------------------------------------
    def tournament_selection(self, tournament_size: int):
        """Select an individual using tournament selection"""

        individuals = []
        indexes = []

        for _ in range(tournament_size):
            while True:
                index = random.randint(0, self.pop_size - 1)

                if index not in indexes:
                    indexes.append(index)
                    individuals.append(self.individuals[index])
                    break
                else:
                    continue

        fitnesses = [self.fitnesses[index] for index in indexes]

        # assuming MAXIMIZATION
        best_individual = individuals[fitnesses.index(min(fitnesses))]

        return best_individual


    # ------------------------------------------------------------
    # SELECT FULL POPULATION
    # ------------------------------------------------------------
    def select(self) -> List[List[int]]:
        """
        Creates a new population using tournament selection.

        - Repeats tournament selection pop_size times
        - Returns a full new population
        """

        new_population = [
            self.tournament_selection(self.tournament_size)
            for _ in range(self.pop_size)
        ]

        # optional: store result
        self.individuals_after_selection = new_population

        return new_population
    
    def sort_by_latitude(self) -> None:
        """Sorts the 4 groups by their average latitude (north to south)."""

        for ind in self.individuals:
            ind.sort_by_latitude()


    def create_next_generation(self, offspring_population, elite_size: int = 2):
        """
        Combines elitism + offspring to create next generation
        """

        # -------------------------------------------------
        # ELITE AUS ALTER POPULATION
        # -------------------------------------------------
        elites = sorted(self.individuals, key=lambda ind: ind.fitness)[:elite_size]

        # -------------------------------------------------
        # REST AUS OFFSPRING
        # -------------------------------------------------
        remaining = self.pop_size - elite_size
        offspring_sorted = sorted(offspring_population.individuals, key=lambda ind: ind.fitness)

        new_individuals = elites + offspring_sorted[:remaining]

        return Population(
            pop_size=self.pop_size,
            individuals=new_individuals,
            generation=self.generation + 1
        )

    # ------------------------------------------------------------
    # EVALUATION
    # ------------------------------------------------------------
    @staticmethod
    def evaluation(pop1: Population, pop2: Population):
        print("\n", "-" * 80)
        print("                     pop1    pop2")
        print()
        print("fitness sum:     ", f"{sum(pop1.fitnesses):7.1f} ", f" {sum(pop2.fitnesses):7.1f}")
        print("avg fitness:     ", f"{sum(pop1.fitnesses)/pop1.pop_size:7.1f} ", f" {sum(pop2.fitnesses)/pop2.pop_size:7.1f}")
        print("fitness\n(best_individual): ", f"{pop1.best_individual.fitness:7.1f} ", f" {pop2.best_individual.fitness:7.1f}")
        print("-"*50, "\navg_fit(p2)/avg_fit(p1) = ", f"{(sum(pop2.fitnesses)/pop1.pop_size) / (sum(pop1.fitnesses)/pop2.pop_size):3.1f}")
        print("best_indiv_fit(p2)/best_indiv_fit(p1) = ", f"{(pop2.best_individual.fitness) / (pop1.best_individual.fitness):3.1f}")
        print("-" * 80, "\n")
    
    @staticmethod
    def time_evaluation(times: list[float], pop_size: int, step_name: str = "generation") -> None:
        print("\n------------------------------")
        print(f"Average time per {step_name}", ": {:.2f} seconds".format(mean(times[1:])))
        print("Standard deviation of time: {:.5f} seconds".format(stdev(times[1:])))
        print("Average time per individual: {:.4f} seconds".format(mean(times[1:]) / pop_size))