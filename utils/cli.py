# utils/cli.py

import argparse

def build_parser():
    parser = argparse.ArgumentParser(description="Battle Run Game CLI")

    parser.add_argument(
        "command",
        choices=["run", "test"],
        help="Commande à exécuter : run pour lancer le jeu."
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=60,
        help="Limite d'images par seconde."
    )

    return parser
