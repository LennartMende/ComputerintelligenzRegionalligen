from src.Population import Population
from src.Strategy import StrategyCfg
from statistics import mean, median, stdev
from collections import Counter
from math import floor
from pathlib import Path
from datetime import datetime
import csv

class Evaluator: 
    @staticmethod
    def multiple_populations_evaluation(populations: list[Population]):
        # fitness of best individuals
        individual_population_pairs = [
            (pop.best_individual, pop)
            for pop in populations
        ]
        best_individual, best_population = min(
            individual_population_pairs,
            key=lambda pair: pair[0].fitness
        )
        worst_individual, worst_population = max(
            individual_population_pairs,
            key=lambda pair: pair[0].fitness
        )
        best_individuals = [pop.best_individual for pop in populations]
        best_individuals_fitness = [pop.best_individual.fitness for pop in populations]
        
        mean_fit = mean(best_individuals_fitness)
        worst_fit = max(best_individuals_fitness)
        best_fit = min(best_individuals_fitness)


        fitness_counter = Counter(best_individuals_fitness)
        
        print("\n", "-" * 80)
        print("\nEvaluation of every population's best individual:")
        print("Fitness evaluation:")
        print("Best fitness = ", best_fit, ", worst fitness = ", worst_fit, ", mean fitness = ", mean_fit)
        print("Fitness distribution:")
        for fitness, count in sorted(fitness_counter.items()):
            print(f"{fitness}: {count}x")

        # diversity of the populations
        population_diversities = [pop.diversity for pop in populations]
        
        mean_div = mean(population_diversities)
        lowest_div = min(population_diversities)
        highest_div = max(population_diversities)
        
 
        print("\nDiversity evaluation:")
        print("Mean diversity: ", mean_div)
        print("Highest diversity: ", highest_div)
        print("Lowest diversity: ", lowest_div)
        
        print("\nBest and worst individual:")
        print("Best individual:", best_individual.permutation)
        print("Best individual's fitness: ", best_fit)
        print("Best individual's diversity:", best_population.diversity)
        print("Worst individual's fitness:", worst_individual.fitness)
        print("Worst individual's diversity:", worst_population.diversity)
        print("-" * 80, "\n")

    @staticmethod
    def eval(populations: list[Population]) -> tuple[dict[str, list[float]], dict[str, list[bool | int]]]:
        numeric_rows = {
            "Best fitness": [],
            "Worst fitness": [],
            "Mean population fitness": [],
            "Mean diversity": [],
            "Median fitness": [],
            "Fitness stddev": [],
            "Fitness range": [],
            "Mean deltas": [],
            "Best deltas": []
        }

        boolean_rows = {
            "Is diversity 0?": []
        }

        first_zero_generation = None

        for i, pop in enumerate(populations, start=1):
            if pop.is_diversity_zero:
                first_zero_generation = i
                break

        for pop in populations:
            best_fitness = pop.best_individual.fitness
            worst_fitness = pop.worst_individual.fitness
            fitnesses = pop.fitnesses

            numeric_rows["Best fitness"].append(best_fitness)
            numeric_rows["Worst fitness"].append(worst_fitness)
            numeric_rows["Mean population fitness"].append(pop.avg_fitness)
            numeric_rows["Mean diversity"].append(pop.diversity)
            numeric_rows["Median fitness"].append(median(fitnesses))
            numeric_rows["Fitness stddev"].append(stdev(fitnesses))
            numeric_rows["Fitness range"].append(max(fitnesses) - min(fitnesses))

        
        
        numeric_rows["Mean deltas"].append(0)
        numeric_rows["Best deltas"].append(0)
        for idx in range(1, len(populations)):
            numeric_rows["Mean deltas"].append(numeric_rows["Mean population fitness"][idx] - numeric_rows["Mean population fitness"][idx - 1])
            numeric_rows["Best deltas"].append(numeric_rows["Best fitness"][idx] - numeric_rows["Best fitness"][idx - 1])
        
        for pop in populations:
            boolean_rows["Is diversity 0?"].append(pop.is_diversity_zero) 
        boolean_rows["Is diversity 0?"].append(first_zero_generation)

        for row in numeric_rows.values():
            values = row.copy()

            minimum = min(values)
            maximum = max(values)
            min_generation = values.index(minimum) + 1   
            max_generation = values.index(maximum) + 1

            row.append(minimum)
            row.append(min_generation)
            row.append(maximum)
            row.append(max_generation)
            row.append(mean(values))
            median_value = median(values)
            median_generation = min(
                range(len(values)),
                key=lambda i: abs(values[i] - median_value)
            )

            row.append(median_value)
            row.append(median_generation + 1)
            row.append(stdev(values))

            change = values[-1] - values[0]
            row.append(change)
            row.append(change / (len(values) - 1))
            try:
                row.append(100 * (values[-1] - values[0]) / values[0])
            except Exception as e:
                row.append(0)
            try:
                row.append(values[-1] / values[0])
            except Exception as e:
                row.append(0)

        return numeric_rows, boolean_rows

    @staticmethod
    def eval_as_csvs(populations: list[Population], strategyCfg: StrategyCfg | None = None):
        numeric_rows, boolean_rows = Evaluator.eval(populations)

        # -------------------------------------------------
        # Header erzeugen
        # -------------------------------------------------
        generation_count = len(populations)

        numeric_header = (
            ["Criterion"]
            + [f"Gen {i}" for i in range(1, generation_count + 1)]
            + [
                "Minimum",
                "Generation of minimum",
                "Maximum",
                "Generation of maximum",
                "Mean",
                "Median",
                "Generation of median",
                "Std. Dev.",
                "Absolute trend",
                "Average trend / generation",
                "Relative trend (%)",
                "Final / Initial"
            ]
        )

        boolean_header = (
            ["Criterion"]
            + [f"Gen {i}" for i in range(1, generation_count + 1)]
            + ["First generation with diversity = 0"]
        )

        # -------------------------------------------------
        # Ausgabeordner erzeugen
        # -------------------------------------------------
        base_dir = Path(__file__).resolve().parent.parent
        evaluation_dir = base_dir / "evaluations"
        evaluation_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        numeric_path = evaluation_dir / f"evaluation_numeric_{timestamp}.csv"
        boolean_path = evaluation_dir / f"evaluation_boolean_{timestamp}.csv"

        # -------------------------------------------------
        # Numeric CSV
        # -------------------------------------------------
        with open(
            numeric_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)
            writer.writerow(numeric_header)

            for criterion, values in numeric_rows.items():
                writer.writerow([criterion] + values)
        print(f"Saved numeric evaluation to {numeric_path}")

        # -------------------------------------------------
        # Boolean CSV
        # -------------------------------------------------
        with open(
            boolean_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)
            writer.writerow(boolean_header)

            for criterion, values in boolean_rows.items():
                writer.writerow([criterion] + values)
        print(f"Saved boolean evaluation to {boolean_path}")

        if strategyCfg:
            

    @staticmethod
    def eval_printed(populations: list[Population]) -> None:
        numeric_rows, boolean_rows = Evaluator.eval(populations)

        generation_count = len(populations)
        population_size = populations[0].pop_size

        final_population = populations[-1]

        print()
        print("=" * 80)
        print("EVOLUTION EVALUATION")
        print("=" * 80)

        print(f"Generations        : {generation_count}")
        print(f"Population size    : {population_size}")

        print()

        # -------------------------------------------------
        # FINAL GENERATION
        # -------------------------------------------------

        print("-" * 80)
        print("FINAL GENERATION")
        print("-" * 80)

        print(f"Best fitness       : {final_population.best_individual.fitness:.2f}")
        print(f"Worst fitness      : {final_population.worst_individual.fitness:.2f}")
        print(f"Mean fitness       : {final_population.avg_fitness:.2f}")
        print(f"Median fitness     : {numeric_rows['Median fitness'][generation_count-1]:.2f}")
        print(f"Fitness stddev     : {numeric_rows['Fitness stddev'][generation_count-1]:.2f}")
        print(f"Fitness range      : {numeric_rows['Fitness range'][generation_count-1]:.2f}")
        print(f"Diversity          : {final_population.diversity:.2f}")

        print()

        # -------------------------------------------------
        # OVER ALL GENERATIONS
        # -------------------------------------------------

        print("-" * 80)
        print("OVER ALL GENERATIONS")
        print("-" * 80)

        best_values = numeric_rows["Best fitness"][:generation_count]
        diversity_values = numeric_rows["Mean diversity"][:generation_count]

        best_generation = best_values.index(min(best_values)) + 1
        worst_generation = best_values.index(max(best_values)) + 1

        highest_div_generation = diversity_values.index(max(diversity_values)) + 1
        lowest_div_generation = diversity_values.index(min(diversity_values)) + 1

        print(f"Overall best fitness      : {min(best_values):.2f}")
        print(f"Occurred in generation    : {best_generation}")

        print()

        print(f"Overall worst fitness     : {max(best_values):.2f}")
        print(f"Occurred in generation    : {worst_generation}")

        print()

        print(f"Highest diversity         : {max(diversity_values):.2f}")
        print(f"Occurred in generation    : {highest_div_generation}")

        print()

        print(f"Lowest diversity          : {min(diversity_values):.2f}")
        print(f"Occurred in generation    : {lowest_div_generation}")

        print()

        # -------------------------------------------------
        # TRENDS
        # -------------------------------------------------

        print("-" * 80)
        print("TRENDS")
        print("-" * 80)

        print(f"Mean fitness change       : {numeric_rows['Mean population fitness'][-4]:.2f}")
        print(f"Best fitness change       : {numeric_rows['Best fitness'][-4]:.2f}")

        print()

        print(f"Mean fitness change/gen   : {numeric_rows['Mean population fitness'][-3]:.2f}")
        print(f"Best fitness change/gen   : {numeric_rows['Best fitness'][-3]:.2f}")

        print()

        print(f"Relative mean improvement : {numeric_rows['Mean population fitness'][-2]:.2f} %")
        print(f"Relative best improvement : {numeric_rows['Best fitness'][-2]:.2f} %")

        print()

        first_zero = boolean_rows["Is diversity 0?"][-1]

        if first_zero is None:
            print("Population diversity never reached zero.")
        else:
            print(f"Population diversity first reached zero in generation {first_zero}.")

        print()

        # -------------------------------------------------
        # PER GENERATION
        # -------------------------------------------------

        print("-" * 80)
        print("PER GENERATION")
        print("-" * 80)

        header = (
            f"{'Gen':>4}"
            f"{'Best':>12}"
            f"{'Mean':>12}"
            f"{'Median':>12}"
            f"{'StdDev':>12}"
            f"{'Range':>12}"
            f"{'Div':>12}"
        )

        print(header)
        print("-" * len(header))

        for i in range(generation_count):
            print(
                f"{i+1:>4}"
                f"{numeric_rows['Best fitness'][i]:>12.2f}"
                f"{numeric_rows['Mean population fitness'][i]:>12.2f}"
                f"{numeric_rows['Median fitness'][i]:>12.2f}"
                f"{numeric_rows['Fitness stddev'][i]:>12.2f}"
                f"{numeric_rows['Fitness range'][i]:>12.2f}"
                f"{numeric_rows['Mean diversity'][i]:>12.2f}"
            )

        print("=" * 80)

    @staticmethod
    def time_eval(populations: list[Population]):
        pass