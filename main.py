from src.Strategy import Strategy
import argparse
from src.Strategy import StrategyCfg
from src.evaluation_of_best_csvs import evaluation_of_best_csvs

parser = argparse.ArgumentParser()
parser.add_argument("--default", action="store_true", help="if default scenario should be optimized")
parser.add_argument("--eval", action="store_false", help="evaluate multiple populations")
parser.add_argument("--draw_map", action="store_false", help="draw map during evaluation")
parser.add_argument("--real-clubs", action="store_false", help="use real clubs for the optimization")

parser.add_argument("--eval_rounds", help="only needed if evaluation", type = int, default=20)
parser.add_argument("--pop_size", help="number of individuals per generation", type = int, default=30)
parser.add_argument("--generations", help="number of generations", type = int, default=1000)
parser.add_argument("--leagues", help="number of leagues", type = int, default=4)
parser.add_argument("--stagnation_counter_limit", help="number of generations without improvement before stopping", type = int, default=1000)
parser.add_argument("--number_of_points", help="number of generated_points", type = int, default=80)
parser.add_argument("--tournament_size", help="number of individuals per tournament", type = int, default=3)
args = parser.parse_args()

print(args)


# pop_sizes = [15, 30, 50, 70]
# tournament_sizes = [3, 5, 7, 10]

pop_sizes = [15, 30, 50]
tournament_sizes = [3, 5, 7]

strategyCfgs: list[StrategyCfg] = []

for pop_size in pop_sizes:
    for tournament_size in tournament_sizes:
        strategyCfgs.append(StrategyCfg(
            pop_size=pop_size,
            generations=args.generations,
            real_clubs=args.real_clubs,
            number_of_points=args.number_of_points,
            leagues=args.leagues,
            stagnation_counter_limit=args.stagnation_counter_limit,
            eval_rounds=args.eval_rounds,
            draw_map=args.draw_map,
            tournament_size=tournament_size
        ))

# strategyCfg = StrategyCfg(
#     pop_size=args.pop_size,
#     generations=args.generations,
#     real_clubs=args.real_clubs,
#     number_of_points=args.number_of_points,
#     leagues=args.leagues,
#     stagnation_counter_limit=args.stagnation_counter_limit,
#     eval_rounds=args.eval_rounds,
#     draw_map=args.draw_map,
#     tournament_size=args.tournament_size
# )

# strategyCfg2 = StrategyCfg(
#     pop_size=20,
#     generations=60,
#     real_clubs=args.real_clubs,
#     number_of_points=args.number_of_points,
#     leagues=args.leagues,
#     stagnation_counter_limit=args.stagnation_counter_limit,
#     eval_rounds=10,
#     draw_map=args.draw_map,
#     tournament_size=args.tournament_size
# )

# Strategy.evaluate_manual_input("1 2 3 4 5 6 7 9 10 11 12 13 14 18 19 21 23 26 28 29 8 15 16 17 20 22 24 25 35 36 37 38 42 43 46 49 50 51 52 54 27 30 31 32 33 34 39 40 41 44 45 47 48 53 55 56 58 60 61 62 57 59 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80")

# if args.eval: # for an optimization and evaluation of multiple populations
#     Strategy.run_evaluation(strategyCfg)
# else: # for a normal optimzation of 1 population
#     Strategy.run(strategyCfg)

Strategy.run_eval_with_different_configs(strategyCfgs)
evaluation_of_best_csvs()