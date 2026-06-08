import matplotlib.pyplot as plt
import numpy as np

from src.ClubData import ClubData
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

    def plot_map(population: Population):
        
        COLORS = ["blue", "green", "orange", "red"]

        individual = population.best_individual

        perm = individual.permutation

        # 4 Ligen schneiden
        leagues = [perm[i:i+20] for i in range(0, len(perm), 20)]

        for league, color in zip(leagues, COLORS):
            coords = [ClubData.club_coords[i] for i in league]

            lats = [c[0] for c in coords]
            lons = [c[1] for c in coords]

            plt.scatter(lons, lats, c=color)

        plt.title("Bestes Individuum (Ligenverteilung)")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend(["Liga 1", "Liga 2", "Liga 3", "Liga 4"])
        plt.show()