# utils/cli.py

import argparse
import sys
import os
import json
from engine.game import GameEngine

# ======== CLI HANDLER ========
def run_battle(args):
    """
    Exécute un scénario avec deux AI.
    """
    print(f"Running battle: scenario={args.scenario}, AI1={args.AI1}, AI2={args.AI2}")
    print(f"Terminal mode: {args.t}, Data file: {args.d}")

    # Ici on pourrait créer un GameEngine, charger scenario, AI etc.
    game = GameEngine()
    if args.t:
        print("Terminal mode activated (no graphics).")
    else:
        game.game_loop()  # ouvre la fenêtre Pygame

    if args.d:
        # sauvegarde minimaliste des résultats
        data = {"scenario": args.scenario, "AI1": args.AI1, "AI2": args.AI2}
        with open(args.d, "w") as f:
            json.dump(data, f)
        print(f"Data saved to {args.d}")

def load_battle(args):
    """
    Charge une partie sauvegardée depuis fichier.
    """
    print(f"Loading battle from {args.savefile}")
    if not os.path.exists(args.savefile):
        print("File does not exist.")
        return
    with open(args.savefile) as f:
        data = json.load(f)
    print("Loaded data:", data)

def run_tourney(args):
    """
    Lancement d'un tournoi automatique.
    """
    print(f"Running tournament: AIs={args.G}, Scenarios={args.S}, N={args.N}, alternate={not args.na}")
    # Ici on pourrait créer plusieurs instances de run_battle en batch

def plot_results(args):
    """
    Génère des plots depuis les résultats d'un scénario.
    """
    print(f"Plotting: AI={args.AI}, Plotter={args.plotter}, Scenario={args.scenario}, Range={args.range}")
    # Ici on pourrait appeler eval sur args.scenario et générer des données pour plotter

# ======== ARGPARSE CONFIG ========
def main():
    parser = argparse.ArgumentParser(description="Battle CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---------- battle run ----------
    parser_run = subparsers.add_parser("run", help="Run a battle")
    parser_run.add_argument("scenario", type=str)
    parser_run.add_argument("AI1", type=str)
    parser_run.add_argument("AI2", type=str)
    parser_run.add_argument("-t", action="store_true", help="Terminal mode")
    parser_run.add_argument("-d", type=str, help="Data file to save results")
    parser_run.set_defaults(func=run_battle)

    # ---------- battle load ----------
    parser_load = subparsers.add_parser("load", help="Load a saved battle")
    parser_load.add_argument("savefile", type=str)
    parser_load.set_defaults(func=load_battle)

    # ---------- battle tourney ----------
    parser_tourney = subparsers.add_parser("tourney", help="Run automatic tournament")
    parser_tourney.add_argument("-G", nargs="+", required=True, help="List of AIs")
    parser_tourney.add_argument("-S", nargs="+", required=True, help="List of scenarios")
    parser_tourney.add_argument("-N", type=int, default=10, help="Number of rounds per matchup")
    parser_tourney.add_argument("-na", action="store_true", help="Do not alternate player positions")
    parser_tourney.set_defaults(func=run_tourney)

    # ---------- battle plot ----------
    parser_plot = subparsers.add_parser("plot", help="Plot scenario results")
    parser_plot.add_argument("AI", type=str)
    parser_plot.add_argument("plotter", type=str)
    parser_plot.add_argument("scenario", type=str)
    parser_plot.add_argument("range", type=str, help="Range of parameters (as Python code)")
    parser_plot.add_argument("-N", type=int, default=10)
    parser_plot.set_defaults(func=plot_results)

    # ---------- Parse args ----------
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
