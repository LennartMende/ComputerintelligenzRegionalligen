import matplotlib.pyplot as plt
import numpy as np

from src.ClubData import ClubData
from src.Population import Population

from pyproj import Transformer
from src.ClubData import ClubData



class GenerationVisualizer:
    TRANSFORMER = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:3035",
        always_xy=True
    )

    GERMANY_EXTREME_POINTS = {
        "north": (55.0586, 8.4167),
        "south": (47.2717, 10.1742),
        "west":  (51.0511, 5.8663),
        "east":  (51.2728, 15.0436),
    }

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
    
    @staticmethod
    def project_club_coords():
        projected = {}

        for club_id, (lat, lon) in ClubData.club_coords.items():

            x_m, y_m = GenerationVisualizer.TRANSFORMER.transform(
                lon,
                lat
            )

            projected[club_id] = (
                x_m / 1000,
                y_m / 1000
            )

        return projected




    def project_extreme_points() -> dict[str, float]:
        """
        Returns:
        {
            "north": y_km,
            "south": y_km,
            "east": x_km,
            "west": x_km
        }
        """

        result = {}

        lat, lon = GenerationVisualizer.GERMANY_EXTREME_POINTS["north"]
        x, y = GenerationVisualizer.TRANSFORMER.transform(lon, lat)
        result["north"] = y / 1000.0

        lat, lon = GenerationVisualizer.GERMANY_EXTREME_POINTS["south"]
        x, y = GenerationVisualizer.TRANSFORMER.transform(lon, lat)
        result["south"] = y / 1000.0

        lat, lon = GenerationVisualizer.GERMANY_EXTREME_POINTS["east"]
        x, y = GenerationVisualizer.TRANSFORMER.transform(lon, lat)
        result["east"] = x / 1000.0

        lat, lon = GenerationVisualizer.GERMANY_EXTREME_POINTS["west"]
        x, y = GenerationVisualizer.TRANSFORMER.transform(lon, lat)
        result["west"] = x / 1000.0

        return result



    def plot_map(population: Population):
    
        COLORS = ["blue", "green", "orange", "red"]

        individual = population.best_individual
        perm = individual.permutation

        leagues = [perm[i:i+20] for i in range(0, len(perm), 20)]

        plt.figure()

        limits = GenerationVisualizer.project_extreme_points()

        # Bild laden und anzeigen im richtigen Koordinatensystem
        img = plt.imread("images/germany2.png")
        plt.imshow(img, extent=[limits["west"], limits["east"], limits["south"], limits["north"]])



        for league_idx, (league, color) in enumerate(zip(leagues, COLORS)):

            projected = GenerationVisualizer.project_club_coords()

            coords = [projected[i] for i in league]

            lats = [c[0] for c in coords]
            lons = [c[1] for c in coords]

            plt.scatter(lats, lons, c=color, label=f"Liga {league_idx+1}")

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
        # plt.xlabel("Longitude")
        # plt.ylabel("Latitude")
        plt.legend()
        # plt.grid(True)

        # Achsenbegrenzungen auf Deutschland setzen
        plt.xlim(limits["west"], limits["east"])
        plt.ylim(limits["south"], limits["north"])

        # Seitenverhältnis beibehalten
        plt.axis("equal")

        plt.show()