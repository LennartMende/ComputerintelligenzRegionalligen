import random
from typing import List, Tuple, Dict


class OrderCrossover:
    """
    Order Crossover (OX) implementation for permutation-based problems.

    Key features:
    - Two RANDOM parents are selected for EACH crossover event
    - Produces TWO children per crossover
    - Stores crossover points for debugging / analysis
    """

    def __init__(self, crossover_rate: float = 1.0):
        """
        :param crossover_rate: probability of applying crossover
        """
        self.crossover_rate = crossover_rate

        # optional debug storage
        self.debug_info = []

    # ------------------------------------------------------------
    # PUBLIC METHOD: recombine full population
    # ------------------------------------------------------------
    def recombine_ox(self, population: List[List[int]]) -> List[List[int]]:
        """
        Creates a new population using OX.

        IMPORTANT:
        - For EACH crossover event, TWO RANDOM PARENTS are selected.
        - Parents are NOT paired beforehand.
        """

        new_population = []

        pop_size = len(population)

        # We assume we want same population size again
        # -> so we generate pop_size / 2 crossover events, because each event produces 2 children
        num_crossovers = pop_size // 2

        for _ in range(num_crossovers):

            # --------------------------------------------------------
            # STEP 1: RANDOMLY SELECT TWO PARENTS (with replacement)
            # --------------------------------------------------------
            parent1 = random.choice(population)
            parent2 = random.choice(population)

            # ensure they are not identical references (optional safety)
            while parent2 is parent1 and pop_size > 1:
                parent2 = random.choice(population)

            # --------------------------------------------------------
            # STEP 2: APPLY CROSSOVER OR COPY
            # --------------------------------------------------------
            if random.random() < self.crossover_rate:
                child1, child2, info = self.ox_crossover(parent1, parent2)
                self.debug_info.append(info)
            else:
                # no crossover → clone parents
                child1, child2 = parent1[:], parent2[:]

            new_population.extend([child1, child2])

        return new_population

    # ------------------------------------------------------------
    # CORE OX OPERATOR
    # ------------------------------------------------------------
    def ox_crossover(
        self,
        parent1: List[int],
        parent2: List[int]
    ) -> Tuple[List[int], List[int], Dict]:

        size = len(parent1)

        # --------------------------------------------------------
        # STEP 1: choose crossover points
        # --------------------------------------------------------
        i, j = sorted(random.sample(range(size), 2))

        # --------------------------------------------------------
        # STEP 2: initialize empty children
        # --------------------------------------------------------
        child1 = [None] * size
        child2 = [None] * size

        # --------------------------------------------------------
        # STEP 3: copy segment from each parent
        # --------------------------------------------------------
        child1[i:j + 1] = parent1[i:j + 1]
        child2[i:j + 1] = parent2[i:j + 1]

        # --------------------------------------------------------
        # STEP 4: fill remaining positions
        # --------------------------------------------------------
        self._fill_child(child1, parent2, j)
        self._fill_child(child2, parent1, j)

        # --------------------------------------------------------
        # DEBUG INFO (important for your report / analysis)
        # --------------------------------------------------------
        debug = {
            "parent1": parent1,
            "parent2": parent2,
            "crossover_points": (i, j),
            "child1": child1,
            "child2": child2
        }

        return child1, child2, debug

    # ------------------------------------------------------------
    # HELPER: fill child according to OX rule
    # ------------------------------------------------------------
    def _fill_child(self, child: List[int], parent: List[int], start_index: int):
        """
        Fills empty positions in child using OX rule:

        - iterate over parent in order
        - skip already used genes
        - fill empty slots cyclically (wrap-around)
        """

        size = len(child)

        # genes already in child
        used = set(child)

        # start position for insertion - at the beginning of the child
        pos = 0

        # go through parent in order
        for gene in parent:

            if gene in used:
                continue

            # find next empty slot
            while child[pos] is not None:
                pos = (pos + 1) % size

            child[pos] = gene
            used.add(gene)

    # ------------------------------------------------------------
    # OPTIONAL: print debug results
    # ------------------------------------------------------------
    def print_debug(self):
        for entry in self.debug_info:
            print("\n--- OX CROSSOVER ---")
            print("Parents:")
            print(entry["parent1"])
            print(entry["parent2"])
            print("Crossover points:", entry["crossover_points"])
            print("Child 1:", entry["child1"])
            print("Child 2:", entry["child2"])

if __name__ == "__main__":

    population = [
        [1,2,3,4,5,6,7,8],
        [4,1,2,8,7,6,5,3],
        [2,3,1,5,4,8,6,7],
        [8,7,6,5,4,3,2,1]
    ]

    ox = OrderCrossover(crossover_rate=1.0)

    new_population = ox.recombine_ox(population)

    print("NEW POPULATION:")
    for ind in new_population:
        print(ind)

    print("\nDEBUG INFO:")
    ox.print_debug()
