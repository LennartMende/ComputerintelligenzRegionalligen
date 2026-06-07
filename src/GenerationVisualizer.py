import matplotlib.pyplot as plt
import numpy as np

from src.Population import Population

class GenerationVisualizer:
    def __init__(self, population: Population):
        self.population = population
    
    @staticmethod
    def show_avg_fit(populations: list[Population]):
        '''Visualize the avg fitness of all generations of the population'''
        avg_fits = np.array([pop.avg_fitness for pop in populations])
        print("type(avg_fits): ", type(avg_fits), ", len(avg_fits): ", len(avg_fits))
        gens = np.linspace(0, populations[-1].generation, populations[-1].generation)
        print("type(gens): ", type(gens), ", len(gens): ", len(gens))
        plt.plot(gens, avg_fits)
        plt.show()
        
    @staticmethod
    def show_best_fit(populations: list[Population]):
        '''Visualize the best point's fitness of all generations of the population'''
        best_fits = np.array([pop.best_individual.fitness for pop in populations])
        print("type(best_fits): ", type(best_fits), ", len(best_fits): ", len(best_fits))
        gens = np.linspace(0, populations[-1].generation, populations[-1].generation)
        print("type(gens): ", type(gens), ", len(gens): ", len(gens))
        plt.plot(gens, best_fits)
        plt.show()