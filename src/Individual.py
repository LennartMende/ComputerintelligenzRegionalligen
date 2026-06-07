from __future__ import annotations
import random
from random import randint

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
    
    # old version of mutation method, new version is below
    # def mutation(self, mutation_swaps: int) -> None: # TODO: swap with a team from another group instead of random swap
    #     if mutation_swaps > 40 or mutation_swaps < 0:
    #         raise ValueError("mutation_swaps must be between 0 and 40!")
    #     if hasattr(self.permutation, "permutation"):
    #         self.permutation = self.permutation.permutation
    #     self.permutation = self.permutation[:] # create a copy of the permutation to avoid modifying the original one
    #     indexes = [i for i in range(self.permutation_size)] # indexes: all unused indexes of the population
    #     for _ in range (mutation_swaps):
    #         index1 = randint(0, self.permutation_size - 1)
    #         indexes.remove(index1)
    #         index2 = randint(0, self.permutation_size - 1)
    #         while index2 not in indexes:
    #             index2 = randint(0, self.permutation_size - 1)
    #         indexes.remove(index2)
    #         self.permutation[index1], self.permutation[index2] = self.permutation[index2], self.permutation[index1]

    # ChatGPT version of mutation method, which ensures that the same index is not swapped twice in one mutation step
    def mutation(self, mutation_swaps: int) -> None:
        
        if hasattr(self.permutation, "permutation"):
            self.permutation = self.permutation.permutation
    
        available = list(range(self.permutation_size))

        for _ in range(mutation_swaps):
            i = random.choice(available)
            available.remove(i)

            j = random.choice(available)
            available.remove(j)

            self.permutation[i], self.permutation[j] = self.permutation[j], self.permutation[i]