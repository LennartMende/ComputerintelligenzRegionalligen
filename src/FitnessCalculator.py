from ClubData import ClubData

class FitnessCalculator:
    @staticmethod
    def clubs_to_coords(id_list: list[int]) -> list[tuple[float, float]]:
        """Converts a list of club IDs to a list of their corresponding coordinates."""
        return [ClubData.clubs[id] for id in id_list]

    @staticmethod
    def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
        """Calculates the Euclidean distance between two points a and b."""
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
    
    @staticmethod
    def _fitness_for_one_club(list_of_clubs: list[tuple[float, float]], index) -> float:
        """Calculates the fitness for one club by summing the distances to all other clubs in the same league."""
        league = index // 20
        fitness = 0
        for i in range(league * 20, league * 20 + 20):
            if i != index:
                fitness += FitnessCalculator._dist(list_of_clubs[index], list_of_clubs[i])
        return fitness

    @staticmethod
    def individual_fitness(list_of_clubs) -> float:
        """Calculates the total fitness for an individual by summing the fitness for each club."""
        if all(isinstance(club, int) for club in list_of_clubs): # club : list[int]
            list_of_clubs = FitnessCalculator.clubs_to_coords(list_of_clubs)
        elif all(isinstance(club, tuple) for club in list_of_clubs) \
            and all(isinstance(coord, float) for coord in list_of_clubs[0]): # club : list[tuple[float, float]]
            pass
        else:
            raise ValueError("List must be of type list[int] or list[tuple[float, float]]!")
        if len(list_of_clubs) != 80:
            raise TypeError("List must include 80 elements!")
        total_fitness = 0
        for i in range (80):
            total_fitness += FitnessCalculator._fitness_for_one_club(list_of_clubs, i)
        return total_fitness