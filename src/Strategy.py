from src.ClubData import ClubData
from src.PopulationInitializer import PopulationInitializer
from src.FitnessCalculator import FitnessCalculator





class Strategy:

    def run():

        # create an instance of the PopulationInitializer class
        population_initializer = PopulationInitializer()

        # create an initial population of random individuals - default size is 100
        population_size = 100
        initial_population = population_initializer.create_population(population_size)

        # create an instance of the FitnessCalculator class
        fitness_calculator = FitnessCalculator()

        # Calculate the fitness of each individual in the initial population
        fitness_values = []
        for individual in initial_population:
            fitness = fitness_calculator.calculate_fitness(individual)
            fitness_values.append(fitness)

        # Print the fitness values for each individual
        for i, fitness in enumerate(fitness_values):
            print(f"Individual {i}: Fitness = {fitness}")
