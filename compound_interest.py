#!/usr/bin/env python3
"""Calculate compound interest from command-line arguments."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate compound interest using principal, annual rate, compounds per year, "
            "and total years."
        )
    )
    parser.add_argument("principal", type=float, help="Initial principal amount (e.g. 15847)")
    parser.add_argument(
        "annual_rate",
        type=float,
        help="Annual interest rate as a percentage (e.g. 7.34) or decimal (e.g. 0.0734)",
    )
    parser.add_argument(
        "compounds_per_year",
        type=int,
        help="Number of times interest compounds per year (e.g. 12 for monthly)",
    )
    parser.add_argument(
        "total_years",
        type=float,
        help="Total investment duration in years (e.g. 8.583333 for 8 years 7 months)",
    )

    args = parser.parse_args()

    principal = args.principal
    annual_rate = args.annual_rate
    compounds_per_year = args.compounds_per_year
    total_years = args.total_years

    if annual_rate > 1:
        annual_rate /= 100.0

    final_amount = principal * (1 + annual_rate / compounds_per_year) ** (
        compounds_per_year * total_years
    )
    interest_earned = final_amount - principal

    print(f"Final amount: ${final_amount:.2f}")
    print(f"Interest earned: ${interest_earned:.2f}")


if __name__ == "__main__":
    main()
