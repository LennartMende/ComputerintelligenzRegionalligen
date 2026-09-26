from src.Strategy import Strategy
import argparse
from src.Strategy import StrategyCfg

parser = argparse.ArgumentParser()
parser.add_argument("--default", action="store_true", help="if default scenario should be optimized")
parser.add_argument("--eval", action="store_false", help="evaluate multiple populations")
parser.add_argument("--draw_map", action="store_false", help="draw map during evaluation")
parser.add_argument("--real-clubs", action="store_false", help="use real clubs for the optimization")

parser.add_argument("--eval_rounds", help="only needed if evaluation", type = int, default=20)
parser.add_argument("--pop_size", help="number of individuals per generation", type = int, default=10)
parser.add_argument("--generations", help="number of generations", type = int, default=500)
parser.add_argument("--leagues", help="number of leagues", type = int, default=40)
parser.add_argument("--stagnation_counter_limit", help="number of generations without improvement before stopping", type = int, default=1000)
parser.add_argument("--number_of_points", help="number of generated_points", type = int, default=80)
parser.add_argument("--tournament_size", help="number of individuals per tournament", type = int, default=3)
args = parser.parse_args()

print(args)

strategyCfg = StrategyCfg(
    pop_size=args.pop_size,
    generations=args.generations,
    real_clubs=args.real_clubs,
    number_of_points=args.number_of_points,
    leagues=args.leagues,
    stagnation_counter_limit=args.stagnation_counter_limit,
    eval_rounds=args.eval_rounds,
    draw_map=args.draw_map,
    tournament_size=args.tournament_size
)

Strategy.run(strategyCfg)
