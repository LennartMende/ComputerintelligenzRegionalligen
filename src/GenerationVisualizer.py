import matplotlib.pyplot as plt
import numpy as np
import os

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


    def compute_colors_and_markers(population: Population):
        COLORS = ["blue", "green", "orange", "red", "grey", "black", "purple", "pink", "brown", "cyan"]
        MARKERS = ["o", "s", "^", "X"]

        # compute used markers and colors based on len(population.individuals[0].permutation) und population.league_size
        team_count = len(population.individuals[0].permutation)
        league_size = population.league_size
        league_count = team_count // league_size

        MARKERS_count = (league_count // len(COLORS) if league_count % len(COLORS) == 0 else league_count // len(COLORS) + 1)
        COLORS_count = league_count // MARKERS_count

        COLORS = COLORS[:COLORS_count]
        MARKERS = MARKERS[:MARKERS_count]

        return COLORS, MARKERS



    def plot_map(population: Population):
        COLORS, MARKERS = GenerationVisualizer.compute_colors_and_markers(population)

        individual = population.best_individual
        perm = individual.permutation

        print("population.league_size = ", population.league_size)

        leagues = [
            perm[i:i + population.league_size]
            for i in range(0, len(perm), population.league_size)
        ]

        # -------------------------------------------------
        # FIGURE + SUBPLOTS
        # -------------------------------------------------
        fig = plt.figure(figsize=(14, 15))
        gs = fig.add_gridspec(1, 2, width_ratios=[1, 4])

        ax_leg = fig.add_subplot(gs[0])
        ax_map = fig.add_subplot(gs[1])

        # -------------------------------------------------
        # MAP SETUP
        # -------------------------------------------------
        limits = GenerationVisualizer.project_extreme_points()
        projected = GenerationVisualizer.project_club_coords()

        base_path = os.path.dirname(__file__)
        project_root = os.path.dirname(base_path)
        img_path = os.path.join(project_root, "images", "germany2.png")

        img = plt.imread(img_path)
        ax_map.imshow(
            img,
            extent=[limits["west"], limits["east"], limits["south"], limits["north"]]
        )

        # -------------------------------------------------
        # PLOTTING
        # -------------------------------------------------
        from itertools import product

        styles = list(product(COLORS, MARKERS))

        for league_idx, (league, (color, marker)) in enumerate(
            zip(leagues, styles)
        ):
            coords = [projected[i] for i in league]

            lats = [c[0] for c in coords]
            lons = [c[1] for c in coords]

            ax_map.scatter(
                lats,
                lons,
                c=color,
                marker=marker,
                label=f"Liga {league_idx+1}"
            )

            for club_id, (lat, lon) in zip(league, coords):
                ax_map.annotate(str(club_id), (lat, lon))

        # -------------------------------------------------
        # LEGEND
        # -------------------------------------------------
        handles, labels = ax_map.get_legend_handles_labels()

        ax_leg.legend(handles, labels, loc="upper left")
        ax_leg.axis("off")

        # -------------------------------------------------
        # FINAL FORMATTING
        # -------------------------------------------------
        ax_map.set_title("Bestes Individuum (Ligenverteilung)")
        ax_map.set_xlim(limits["west"], limits["east"])
        ax_map.set_ylim(limits["south"], limits["north"])
        ax_map.axis("off")

        plt.show()



if __name__ == "__main__":
    GenerationVisualizer.compute_colors_and_markers()