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

        leagues = [perm[i:i+20] for i in range(0, len(perm), 20)]

        plt.figure(figsize=(10, 8))

        for league_idx, (league, color) in enumerate(zip(leagues, COLORS)):

            coords = [ClubData.club_coords[i] for i in league]

            lats = [c[0] for c in coords]
            lons = [c[1] for c in coords]

            plt.scatter(lons, lats, c=color, label=f"Liga {league_idx+1}")

            # 🔥 IDs hinzufügen
            for club_id, (lat, lon) in zip(league, coords):

                plt.annotate(
                    str(club_id),
                    (lon, lat),
                    xytext=(3, 3),                 # kleiner Offset
                    textcoords="offset points",
                    fontsize=7,
                    alpha=0.8
                )

        plt.title("Bestes Individuum (Ligenverteilung)")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend()
        plt.grid(True)

        plt.show()