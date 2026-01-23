
import sys
import os

parent_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(parent_dir)
from utils.cli import parse_args


def cmd_run(args):
    pass


def cmd_load(args):
    pass


def cmd_tourney(args):
    pass


def cmd_plot(args):
    pass


def main():
    args = parse_args()
    
    if args.command == "run":
        cmd_run(args)
    elif args.command == "load":
        cmd_load(args)
    elif args.command == "tourney":
        cmd_tourney(args)
    elif args.command == "plot":
        cmd_plot(args)


if __name__ == "__main__":
    main()
