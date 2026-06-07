import matplotlib.pyplot as plt
import numpy as np

from src.Population import Population

class GenerationVisualizer:
    def __init__(self, population: Population):
        self.population = population
    
    @staticmethod
    def show_avg_fit(populations: list[Population]):
        avg_fits = np.array([pop.avg_fitness for pop in populations])
        gens = np.arange(len(populations))

        plt.plot(gens, avg_fits)
        plt.show()
        
    @staticmethod
    def show_best_fit(populations: list[Population]):
        best_fits = np.array([pop.best_individual.fitness for pop in populations])
        gens = np.arange(len(populations))

        plt.plot(gens, best_fits)
        plt.show()