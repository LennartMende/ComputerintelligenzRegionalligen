from __future__ import annotations
import random

from src.ClubData import ClubData
from src. FitnessCalculator import FitnessCalculator

class Individual:
    def __init__(self):
        self.permutation = self._create_individual()

    def _create_individual(self) -> list[int]:
        """Creates a random individual (a random permutation of the clubs)."""
        individual = self.club_ids.copy()
        random.shuffle(individual)
        return individual

    def __str__(self):
        return f"permutation: {self.permutation}"

    @staticmethod
    def clubs_to_coords(id_list: list[int]) -> list[tuple[float, float]]:
        """Converts a list of club IDs to a list of their corresponding coordinates."""
        return [ClubData.club_coords[id] for id in id_list]
    
    @property
    def fitness(self) -> float:
        '''Calculate the fitness of an individual'''
        fitness = FitnessCalculator.individual_fitness(self.permutation)
        return fitness