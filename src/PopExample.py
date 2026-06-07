from __future__ import annotations
from random import uniform, randint, random
from EAs.Individual import Individual
from copy import deepcopy
from dataclasses import dataclass
from statistics import stdev

@dataclass
class PopulationConfig:
    popsize: int
    dimensions: int
    min_value: float
    max_value: float
    mutation_count: int = 20
    mutation_rate: float = 1
    tournament_size: int = 5
    elitism_on: bool = False
    termination_crit_key: str = "gen_count"
    termination_crit_value: float = 100.0 #gen_count, min_fitness, max_diversity or max_time in seconds
    generation: int = 0


class Population(list):
    def __init__(self, populationConfig: PopulationConfig):
        self.individuals = [Individual(populationConfig.dimensions, populationConfig.min_value, populationConfig.max_value) for _ in range(populationConfig.popsize)]
        self.populationConfig = populationConfig
        self.popsize = populationConfig.popsize
        self.tournament_size = populationConfig.tournament_size
        self.mutation_count = populationConfig.mutation_count
        self.mutation_rate = populationConfig.mutation_rate
        self.elitism_on = populationConfig.elitism_on
        self.generation = 0
        self.termination_crit_key = populationConfig.termination_crit_key
        self.termination_conds = {
            "gen_count": True if populationConfig.termination_crit_key == "gen_count" else False,
            "min_fitness": True if populationConfig.termination_crit_key == "min_fitness" else False,
            "min_diversity": True if populationConfig.termination_crit_key == "min_diversity" else False,
            #"time_limit": True if populationConfig.termination_crit_key == "time_limit" else False
        }
        self.termination_crit_value = populationConfig.termination_crit_value

    #property methods
    @property
    def fitnesses(self) -> list[float]:
        return [ind.fitness for ind in self.individuals]
    
    @property
    def best_individual(self) -> Individual:
        return self.individuals[self.fitnesses.index(max(self.fitnesses))]
    
    @property
    def worst_individual(self) -> Individual:
        return self.individuals[self.fitnesses.index(min(self.fitnesses))]
    
    @property
    def total_fitness(self) -> float:
        return sum(self.fitnesses)
    
    @property
    def avg_fitness(self) -> float:
        return self.total_fitness / self.popsize
    
    @property
    def diversity(self) -> float:
        """implementation for the diversity can be changed"""
        return stdev(self.fitnesses)


    def __str__(self):
        result = ""
        for individual in self.individuals:
            result += f"individual: {individual}, fitness: {individual.fitness}\n"
        result += f"population fitness: {self.total_fitness}\n"
        result += f"population average fitness: {self.avg_fitness}\n"
        return result
    
    # factory method to create a population with random individuals
    @classmethod
    def population_from_list(cls, individuals: list[Individual], populationConfig: PopulationConfig) -> Population:
        population = cls.__new__(cls)
        population.individuals = individuals
        population.popsize = len(individuals)
        population.populationConfig = populationConfig
        population.mutation_count = populationConfig.mutation_count
        population.tournament_size = populationConfig.tournament_size
        population.mutation_rate = populationConfig.mutation_rate
        population.elitism_on = populationConfig.elitism_on
        population.generation = populationConfig.generation
        population.termination_crit_key = populationConfig.termination_crit_key
        population.termination_conds = {
            "gen_count": True if populationConfig.termination_crit_key == "gen_count" else False,
            "min_fitness": True if populationConfig.termination_crit_key == "min_fitness" else False,
            "min_diversity": True if populationConfig.termination_crit_key == "min_diversity" else False,
            #"time_limit": True if populationConfig.termination_crit_key == "time_limit" else False
        }
        population.termination_crit_value = populationConfig.termination_crit_value
        return population


    def tournament_selection(self, tournament_size: int) -> Individual:
        '''Select an individual'''
        individuals: list[Individual] = []
        indexes = []
        for i in range (tournament_size):
            while True:
                index = randint(0, self.popsize - 1)
                if index not in indexes:
                    indexes.append(index)
                    individuals.append(self.individuals[index])
                    break
                else:
                    continue
        
        fitnesses = [self.fitnesses[index] for index in indexes]
        best_individual = individuals[fitnesses.index(max(fitnesses))]
        return best_individual
    
    def population_tournament_selection(self):
        individuals =  [self.tournament_selection(self.tournament_size) for _ in range(self.popsize)]
        return Population.population_from_list(individuals, self.populationConfig)
    
    def recombination(self) -> Population:
        '''Recombine individuals in the population to create a new population'''
        new_individuals = []
        for _ in range (2):
            population_copy = deepcopy(self)
            while len(population_copy.individuals) >= 2:
                i1 = randint(0, len(population_copy.individuals) - 1)
                i2 = randint(0, len(population_copy.individuals) - 1)
                while i1 == i2:
                    i2 = randint(0, len(population_copy.individuals) - 1)
                i1, i2 = sorted([i1, i2], reverse=True)

                parent1 = population_copy.individuals.pop(i1)
                parent2 = population_copy.individuals.pop(i2)

                child = Individual.recombine(parent1, parent2)
                new_individuals.append(child)
        
        return Population.population_from_list(new_individuals, PopulationConfig(
            popsize=self.popsize, dimensions=self.populationConfig.dimensions, 
            min_value=self.populationConfig.min_value, max_value=self.populationConfig.max_value, 
            mutation_count=self.mutation_count, mutation_rate=self.mutation_rate, tournament_size=self.tournament_size,
            termination_crit_key=self.termination_crit_key, termination_crit_value=self.termination_crit_value,
            elitism_on=self.elitism_on, generation=self.generation + 1))

    def mutation(self) -> Population:
        population_copy = deepcopy(self)
        indexes = []
        for i in range (self.mutation_count):
            index = randint(0, self.popsize - 1)
            while index in indexes:
                index = randint(0, self.popsize - 1)
            indexes.append(index)
            population_copy.individuals[index] = population_copy.individuals[index].mutate(self.mutation_rate)
        
        return population_copy
    
    def elitism(self, other: Population):
        overwritten_index = other.individuals.index(other.worst_individual)
        other.individuals[overwritten_index] = self.best_individual
    
    def calculate_next_generation(self) -> Population:
        '''Create the next generation of the population'''
        next_population = self.population_tournament_selection()
        next_population = next_population.recombination()
        next_population = next_population.mutation()
        if self.elitism_on:
            self.elitism(other=next_population)
        next_population.generation += 1
        return next_population
    

    @staticmethod
    def evaluation(pop1: Population, pop2: Population):
        print("\n", "-" * 80)
        print("                     pop1    pop2")
        print()
        print("fitness sum:     ", f"{sum(pop1.fitnesses):7.1f} ", f" {sum(pop2.fitnesses):7.1f}")
        print("avg fitness:     ", f"{sum(pop1.fitnesses)/pop1.popsize:7.1f} ", f" {sum(pop2.fitnesses)/pop2.popsize:7.1f}")
        print("fitness\n(best_individual): ", f"{pop1.best_individual.fitness:7.1f} ", f" {pop2.best_individual.fitness:7.1f}")
        print("-"*50, "\navg_fit(p2)/avg_fit(p1) = ", f"{(sum(pop2.fitnesses)/pop1.popsize) / (sum(pop1.fitnesses)/pop2.popsize):3.1f}")
        print("best_indiv_fit(p2)/best_indiv_fit(p1) = ", f"{(pop2.best_individual.fitness) / (pop1.best_individual.fitness):3.1f}")
        print("-" * 80, "\n")


    def termination(self):
        # Fehler abfangen (mehrfach oder kein True)
        if list(self.termination_conds.values()).count(True) != 1:
            raise Exception("There has to be exactly 1 termination condition!")
        if self.termination_conds["gen_count"]:
            return self.generation > self.termination_crit_value
        elif self.termination_conds["min_fitness"]:
            return self.best_individual.fitness > self.termination_crit_value
        elif self.termination_conds["min_diversity"]:
            return self.diversity < self.termination_crit_value
        #elif self.termination_conds["time_limit"]:
        #    return self.time_limit < self.termination_crit_value