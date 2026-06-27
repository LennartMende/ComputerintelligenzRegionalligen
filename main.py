from src.Strategy import Strategy
print("Beginn")
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--default", action="store_true", help="if default scenario should be optimized")
parser.add_argument("--eval", action="store_true", help="evaluate multiple populations")
parser.add_argument("--draw_map", action="store_true", help="draw map during evaluation")
parser.add_argument("--real-clubs", "--real_clubs", action="store_true", help="use real clubs for the optimization")

parser.add_argument("--eval_rounds", help="only needed if evaluation", type = int, default=30)
parser.add_argument("--pop_size", help="number of individuals per generation", type = int, default=30)
parser.add_argument("--generations", help="number of generations", type = int, default=20)
parser.add_argument("--leagues", help="number of leagues", type = int, default=4)
args = parser.parse_args()

print(args)

# Strategy.evaluate_manual_input("1 2 3 4 5 6 7 9 10 11 12 13 14 18 19 21 23 26 28 29 8 15 16 17 20 22 24 25 35 36 37 38 42 43 46 49 50 51 52 54 27 30 31 32 33 34 39 40 41 44 45 47 48 53 55 56 58 60 61 62 57 59 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80")
# Strategy.run() # for a normal optimzation of 1 population

print("Ich bin die richtige main")

if args.eval: # for an optimization and evaluation of multiple populations
    Strategy.run_evaluation(eval_rounds=args.eval_rounds, draw_map=args.draw_map, pop_size=args.pop_size, generations=args.generations) 
else: # for a normal optimzation of 1 population
    Strategy.run(pop_size=args.pop_size, generations=args.generations, leagues=args.leagues, real_clubs=args.real_clubs)