from __future__ import annotations

def elitism(self, other: Population): # TODO: other überdenken
        overwritten_index = other.individuals.index(other.worst_individual)
        other.individuals[overwritten_index] = self.best_individual