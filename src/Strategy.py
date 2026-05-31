from src.PopulationInitializer import PopulationInitializer
from src.FitnessCalculator import FitnessCalculator





class Strategy:

    def run():

        # create an instance of the PopulationInitializer class
        population_initializer = PopulationInitializer()

        # create an initial population of random individuals - default size is 100
        population_size = 10
        population_initializer.create_population(population_size)

        print("Initial Population: \n", population_initializer.initial_population, "\n")



        # create an instance of the FitnessCalculator class
        fitness_calculator = FitnessCalculator()

        # calculate the fitness of the initial population
        fitness_values = FitnessCalculator.population_fitness(population_initializer.initial_population)
        print("Fitness Values: \n", fitness_values, "\n")
        print("Average distance per away game: \n", [value/80/19 for value in fitness_values], "\n")
