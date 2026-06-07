from __future__ import annotations
import random
from random import randint
from statistics import mean

from src.ClubData import ClubData
from src.FitnessCalculator import FitnessCalculator

class Individual:
    def __init__(self, permutation: list[int] | None = None):
        self.club_ids = list(ClubData.club_coords.keys())   # club_ids is a list of integers from 1 to 80 that were used as keys in the club_coords dictionary in ClubData.py

        if permutation is None:
            self.permutation = self._create_individual()
        else:
            self.permutation = permutation
        
        self.permutation_size = 80

    def _create_individual(self) -> list[int]:
        """Creates a random individual (a random permutation of the clubs)."""
        individual = self.club_ids.copy()
        random.shuffle(individual)
        return individual

    def __str__(self):
        return f"permutation: {self.permutation}"

    @classmethod
    def from_permutation(cls, permutation: list[int]):
        """Creates an individual from a given permutation of club IDs. This is useful for creating new individuals during recombination."""
        return cls(permutation=permutation)

    @staticmethod
    def clubs_to_coords(id_list: list[int]) -> list[tuple[float, float]]:
        """Converts a list of club IDs to a list of their corresponding coordinates."""
        return [ClubData.club_coords[id] for id in id_list]
    
    @property
    def fitness(self) -> float:
        '''Calculate the fitness of an individual'''
        fitness = FitnessCalculator.individual_fitness(self)
        return fitness
    
    def mutation(self, mutation_swaps: int) -> None: # TODO: swap with a team from another group instead of random swap
        if mutation_swaps > 40 or mutation_swaps < 0:
            raise ValueError("mutation_swaps must be between 0 and 40!")
        self.permutation = self.permutation.copy()
        indexes = [i for i in range(self.permutation_size)] # indexes: all unused indexes of the population
        for _ in range (mutation_swaps):
            index1 = randint(0, self.permutation_size - 1)
            indexes.remove(index1)
            index2 = randint(0, self.permutation_size - 1)
            while index2 not in indexes:
                index2 = randint(0, self.permutation_size - 1)
            indexes.remove(index2)
            self.permutation[index1], self.permutation[index2] = self.permutation[index2], self.permutation[index1]
    
    def avg_group_latitudes(self) -> list[float]:
        """Calculates the average latitude for each of the 4 groups of clubs in the individual's permutation."""
        avg_group_latitudes = []
        for i in range(0, 4):
            avg_group_latitudes.append(mean([coord[0] for coord in self.clubs_to_coords(self.permutation[i * 20:(i + 1) * 20])]))
    
        return avg_group_latitudes
    
    def sort_by_latitude(self, debug: bool = True) -> None:
        """Sorts the individual's permutation by the average latitude of the groups of clubs."""
        if debug:
            print(f"Sorting individual by latitude.")
            print("original: ", self.avg_group_latitudes())
        groups = [self.permutation[i * 20:(i + 1) * 20] for i in range(4)]
        groups.sort(key=lambda group: mean(coord[0] for coord in self.clubs_to_coords(group)), reverse=True)
        self.permutation = [club for group in groups for club in group]
        if debug:
            print("sorted: ", self.avg_group_latitudes())