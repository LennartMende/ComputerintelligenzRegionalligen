import random

class RecombinatorPmx:

    @staticmethod
    def pmx(parent1: list[int], parent2: list[int], cut1: int = -1, cut2: int = -1) -> tuple[list[int], list[int]]:
        '''Performs Partially Mapped Crossover (PMX) on two parents to produce two offspring.'''
        # check if parents are of the same length
        size = len(parent1)
        if size != len(parent2):
            raise ValueError("Parents must be of the same length!")
        
        # randomly select two crossover points
        if cut1 == -1 or cut2 == -1:
            cut1, cut2 = sorted(random.sample(range(size+1), 2))
        print(f"Crossover points: {cut1}, {cut2}")

        # create offspring1 with the same length as the parents

        offspring1 = [0] * size

        # Copy the middle section from `parent1`
        offspring1[cut1:cut2] = parent1[cut1:cut2]

        # Copy the rest from `parent2`, resolving conflicts
        for i in (*range(0,cut1), *range(cut2,size)):
            candidate = parent2[i]
            while candidate in parent1[cut1:cut2]:  # handle successive mappings
                candidate = parent2[parent1.index(candidate)]
            offspring1[i] = candidate

        
        # create offspring2 with the same length as the parents
        offspring2 = [0] * size

        # Copy the middle section from `parent2`
        offspring2[cut1:cut2] = parent2[cut1:cut2]

        # Copy the rest from `parent1`, resolving conflicts
        for i in (*range(0,cut1), *range(cut2,size)):
            candidate = parent1[i]
            while candidate in parent2[cut1:cut2]:  # handle successive mappings
                candidate = parent1[parent2.index(candidate)]
            offspring2[i] = candidate

        return offspring1, offspring2