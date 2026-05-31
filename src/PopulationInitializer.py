import random

from src.ClubData import ClubData





class PopulationInitializer:

    def __init__(self):
        self.club_ids = list(ClubData.club_coords.keys())   # club_ids is a list of integers from 1 to 80 that were used as keys in the club_coords dictionary in ClubData.py
        self.initial_population = []

    def create_inidividual(self) -> list[int]:
        """Creates a random individual (a random permutation of the clubs)."""
        individual = self.club_ids.copy()
        random.shuffle(individual)
        return individual

    def create_population(self, population_size: int) -> list[list[int]]:
        """Creates a population of random individuals."""

        for i in range(population_size):
            individual = self.create_inidividual()
            self.initial_population.append(individual)
