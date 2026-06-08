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

    # ChatGPT version of mutation method, which ensures that the same index is not swapped twice in one mutation step and that only teams from different groups are swapped
    def mutation(self, mutation_swaps: int) -> None:

        if hasattr(self.permutation, "permutation"):
            self.permutation = self.permutation.permutation

        size = len(self.permutation)

        swaps_done = 0
        attempts = 0
        max_attempts = mutation_swaps * 20

        #print("\n--- Mutation Start ---")

        while swaps_done < mutation_swaps and attempts < max_attempts:

            i = random.randrange(size)
            j = random.randrange(size)

            # Liga-Constraint
            if (i // 20) == (j // 20):
                attempts += 1
                continue

            # Swap durchführen
            self.permutation[i], self.permutation[j] = (
                self.permutation[j],
                self.permutation[i],
            )

            swaps_done += 1
            attempts += 1

            #print(f"Swap {swaps_done}: i={i} (Liga {i//20}) <-> j={j} (Liga {j//20})")

        #print("--- Mutation Ende ---\n")

    

    def mutation_from_location(self, max_swaps: int = 1) -> None:
        import random
        from src.ClubData import ClubData

        def distance(a, b):
            return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5

        size = len(self.permutation)
        leagues = [self.permutation[i:i+20] for i in range(0, size, 20)]

        centroids = []
        for league in leagues:
            coords = [ClubData.club_coords[i] for i in league]
            lat = sum(c[0] for c in coords) / len(coords)
            lon = sum(c[1] for c in coords) / len(coords)
            centroids.append((lat, lon))

        swaps_done = 0
        attempts = 0
        max_attempts = max_swaps * 5   # 🔥 wichtig

        while swaps_done < max_swaps and attempts < max_attempts:

            attempts += 1

            # --- schlechtestes Team ---
            worst_team = None
            worst_league = None
            worst_dist = -1

            for l_idx, league in enumerate(leagues):
                for team in league:
                    d = distance(ClubData.club_coords[team], centroids[l_idx])
                    if d > worst_dist:
                        worst_dist = d
                        worst_team = team
                        worst_league = l_idx

            # --- bestes Ziel ---
            best_target = None
            best_gain = 0

            for target_l in range(4):
                if target_l == worst_league:
                    continue

                d_new = distance(
                    ClubData.club_coords[worst_team],
                    centroids[target_l]
                )

                gain = worst_dist - d_new

                # 🔥 nur akzeptieren wenn wirklich sinnvoll
                if gain > best_gain:
                    best_gain = gain
                    best_target = target_l

            # ❌ kein sinnvoller Move → ABBRUCH
            if best_target is None or best_gain < 1e-6:
                return

            # --- Swap ---
            idx1 = self.permutation.index(worst_team)
            target_range = range(best_target * 20, (best_target + 1) * 20)
            idx2 = random.choice(list(target_range))

            self.permutation[idx1], self.permutation[idx2] = (
                self.permutation[idx2],
                self.permutation[idx1],
            )

            leagues = [self.permutation[i:i+20] for i in range(0, size, 20)]

            swaps_done += 1



    def sort_by_latitude(self) -> None:
        """Sorts the 4 groups by their average latitude (north to south)."""

        groups = [
            self.permutation[i * 20:(i + 1) * 20]
            for i in range(4)
        ]

        groups.sort(
            key=lambda group: mean(
                coord[0]
                for coord in self.clubs_to_coords(group)
            ),
            reverse=True
        )

        self.permutation = [
            club
            for group in groups
            for club in group
        ]