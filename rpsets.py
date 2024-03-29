#!/usr/bin/env python3
"""Calculate warmup and backoff sets for Reverse Pyramid."""
import argparse
from argparse import Namespace
from typing import List, Tuple

DEFAULT_PERCENTAGE = 5
DEFAULT_WARMUP_SETS = 2
DEFAULT_SETS = 3
DEFAULT_ROUND_BASE = 2.5
WARMUP_BACKOFF = 0.9
WARMUP_MIN = 0.60
WARMUP_MAX = 0.75
WARMUP_RANGE = WARMUP_MAX - WARMUP_MIN


def warmup_sets(args: Namespace) -> Tuple[float, ...]:
    """Create the backoff sets."""
    result: List[float] = []

    # This works, but the math could be more elegant
    percent = WARMUP_MIN
    if args.warmup_sets == 1:
        percent += WARMUP_RANGE / 2
        step = 0
    else:
        step = WARMUP_RANGE / (args.warmup_sets - 1)

    i = 0
    while i < args.warmup_sets:
        result += [percent]
        i += 1
        percent += step

    return tuple(result)


def backoff_sets(args: Namespace) -> Tuple[float, ...]:
    """Create the backoff sets."""
    result: List[float] = [1]
    print(args.percentage)
    multiplier = (100 - float(args.percentage)) / 100
    for _ in range(1, args.sets):
        last_set = result[-1]
        result += [multiplier * last_set]
    return tuple(result)


def roundbase(num, base):
    """Round to a particular base."""
    return base * round(num / base)


def run(args: Namespace) -> List:
    """Calculate and print results."""
    sets = warmup_sets(args)
    sets += backoff_sets(args)
    result: List = []
    max_weight = args.max_weight
    if args.bodyweight:
        max_weight += args.bodyweight
    for set_ in sets:
        float_weight = set_ * float(max_weight)
        weight = roundbase(float_weight, args.round)
        if args.bodyweight:
            weight = weight - args.bodyweight
        percent = int(set_ * 100)
        result += [(percent, weight)]
    return result


def output(result: List) -> None:
    """Print the result dictionary."""
    for (percent, weight) in result:
        print(f"{percent: >3d}% : {weight}")


def parse_args():
    """Parse arguments and options."""
    parser = argparse.ArgumentParser(description="Calculate reverse pyramid sets")
    parser.add_argument("max_weight", type=float, help="Maximum intensity for the day")
    parser.add_argument(
        "-p",
        "--percentage",
        action="store",
        dest="percentage",
        type=float,
        default=DEFAULT_PERCENTAGE,
        help=f"Backoff percentage. Default: {DEFAULT_PERCENTAGE}",
    )
    parser.add_argument(
        "-b",
        "--bodyweight",
        action="store",
        type=int,
        dest="bodyweight",
        default=None,
        help="Bodyweight for bodyweight exercises.",
    )
    parser.add_argument(
        "-s",
        "--sets",
        action="store",
        dest="sets",
        type=int,
        default=DEFAULT_SETS,
        help=f"Number of work sets. Default: {DEFAULT_SETS}",
    )
    parser.add_argument(
        "-w",
        "--warmup-sets",
        action="store",
        dest="warmup_sets",
        type=int,
        default=DEFAULT_WARMUP_SETS,
        help=f"Number of warmup sets. Default: {DEFAULT_WARMUP_SETS}",
    )
    parser.add_argument(
        "-r",
        "--round",
        action="store",
        dest="round",
        type=float,
        default=DEFAULT_ROUND_BASE,
        help=f"Base to round intensity to. Default: {DEFAULT_ROUND_BASE}",
    )

    return parser.parse_args()


def main() -> None:
    """Take cli input."""
    args = parse_args()
    result = run(args)
    output(result)


if __name__ == "__main__":
    main()
