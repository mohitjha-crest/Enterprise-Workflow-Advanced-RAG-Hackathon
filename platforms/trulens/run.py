import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import argparse

from trulens_eval import Tru
from experiment import run_experiment

def trulense_experiment():
    print("Executing Trulense experiment...")
    run_experiment()


def trulense_dashboard():
    print("Opening Trulense dashboard...")

    tru = Tru()
    tru.run_dashboard()


def main():
    parser = argparse.ArgumentParser(description="Script to perform Trulense actions")
    parser.add_argument("action", nargs='?', choices=["trulense_dashboard", "trulense_experiment"], default="trulense_dashboard", help="Action to perform")

    args = parser.parse_args()

    if args.action == "trulense_experiment":
        trulense_experiment()

    trulense_dashboard()


if __name__ == "__main__":
    main()
