import random

class RandomLocationsGenerator:
    # Germany's extreme points for random location generation
    GERMANY_EXTREME_POINTS = {
        "north": (55.0586, 8.4167),
        "south": (47.2717, 10.1742),
        "west":  (51.0511, 5.8663),
        "east":  (51.2728, 15.0436),
    }

    @staticmethod
    def generate_random_locations(number_of_points) -> dict[int, tuple[float, float]]:
        """
        Generates an src.Clubdata.Clubdata.club_data like dict of number_of_points entries in Germany's bounding box.
        """
        club_coords = {}
        for i in range(1, number_of_points + 1):
            north_south = random.random() * \
                (RandomLocationsGenerator.GERMANY_EXTREME_POINTS['north'][0] - RandomLocationsGenerator.GERMANY_EXTREME_POINTS['south'][0]) \
                + RandomLocationsGenerator.GERMANY_EXTREME_POINTS['south'][0]
            east_west = random.random() * \
                (RandomLocationsGenerator.GERMANY_EXTREME_POINTS['east'][1] - RandomLocationsGenerator.GERMANY_EXTREME_POINTS['west'][1]) \
                + RandomLocationsGenerator.GERMANY_EXTREME_POINTS['west'][1]
            club_coords[i] = (north_south, east_west)
        # print("club_coords = ", club_coords)
        return club_coords
    
def main():
    RandomLocationsGenerator.generate_random_locations(100)

if __name__ == "__main__":
    main()
