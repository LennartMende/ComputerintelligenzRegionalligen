from random import randint

from src.Individual import Individual

def tournament_selection(self, tournament_size: int) -> Individual:
        """"Select an individual"""
        individuals: list[Individual] = []
        indexes = []
        for i in range (tournament_size):
            while True:
                index = randint(0, self.popsize - 1)
                if index not in indexes:
                    indexes.append(index)
                    individuals.append(self.individuals[index])
                    break
                else:
                    continue
        
        fitnesses = [self.fitnesses[index] for index in indexes]
        best_individual = individuals[fitnesses.index(max(fitnesses))]
        return best_individual
    
def population_tournament_selection(self) -> list[Individual]:
    individuals =  [self.tournament_selection(self.tournament_size) for _ in range(self.popsize)]
    return individuals

def elitism(self, other: Population):
        overwritten_index = other.individuals.index(other.worst_individual)
        other.individuals[overwritten_index] = self.best_individual