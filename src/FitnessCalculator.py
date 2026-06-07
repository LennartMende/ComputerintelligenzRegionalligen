from src.ClubData import ClubData
from haversine import haversine

class FitnessCalculator:
    @staticmethod
    def clubs_to_coords(id_list):
        if hasattr(id_list, "permutation"):
            id_list = id_list.permutation

        return [ClubData.club_coords[id] for id in id_list]

    @staticmethod
    def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
        """Calculates the Euclidean distance between two points a and b."""
        return haversine(a, b)

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
    def individual_fitness(individual) -> float:
        list_of_clubs = individual.permutation

        coords = FitnessCalculator.clubs_to_coords(list_of_clubs)

        total_fitness = 0
        for i in range(len(coords)):
            total_fitness += FitnessCalculator._fitness_for_one_club(coords, i)

        return total_fitness
    
    @staticmethod
    def population_fitness(population: list[list[int]]) -> list[float]:
        """Calculates the fitness for each individual in the population."""
        fitness_values = []
        for individual in population:
            fitness_values.append(FitnessCalculator.individual_fitness(individual))
        return fitness_values