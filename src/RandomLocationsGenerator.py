import random

from src.GenerationVisualizer import GenerationVisualizer

class RandomLocationsGenerator:
    @staticmethod
    def generate_random_locations(number_of_points) -> dict[int, tuple[float, float]]:
        """
        Generates an src.Clubdata.Clubdata.club_data like dict of number_of_points entries in Germany's bounding box.
        """
        print("GenerationVisualizer.GERMANY_EXTREME_POINTS['north'][0] - GenerationVisualizer.GERMANY_EXTREME_POINTS['south'][0] = ", \
        GenerationVisualizer.GERMANY_EXTREME_POINTS['north'][0] - GenerationVisualizer.GERMANY_EXTREME_POINTS['south'][0])
        print("GenerationVisualizer.GERMANY_EXTREME_POINTS['east'][1] - GenerationVisualizer.GERMANY_EXTREME_POINTS['west'][1] = ", \
        GenerationVisualizer.GERMANY_EXTREME_POINTS['east'][1] - GenerationVisualizer.GERMANY_EXTREME_POINTS['west'][1])
        club_coords = {}
        for i in range(1, number_of_points + 1):
            north_south = random.random() * \
                (GenerationVisualizer.GERMANY_EXTREME_POINTS['north'][0] - GenerationVisualizer.GERMANY_EXTREME_POINTS['south'][0]) \
                + GenerationVisualizer.GERMANY_EXTREME_POINTS['south'][0]
            east_west = random.random() * \
                (GenerationVisualizer.GERMANY_EXTREME_POINTS['east'][1] - GenerationVisualizer.GERMANY_EXTREME_POINTS['west'][1]) \
                + GenerationVisualizer.GERMANY_EXTREME_POINTS['west'][1]
            club_coords[i] = (north_south, east_west)
        # print("club_coords = ", club_coords)
        return club_coords
    
def main():
    RandomLocationsGenerator.generate_random_locations(100)

if __name__ == "__main__":
    main()
