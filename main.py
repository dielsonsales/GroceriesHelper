#!/usr/bin/env python3
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from collections import defaultdict
import sys

def ask(prompt):
    try:
        return input(prompt)
    except EOFError:
        return ''

def parse_money(s):
    s = s.strip()
    if s == '':
        raise ValueError("empty")
    try:
        d = Decimal(s).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except InvalidOperation:
        raise ValueError("not a valid money amount")
    return d

def main():
    raw = ask("Enter TOTAL spent (e.g. 46.20): ").strip()
    if not raw:
        print("No total provided. Exiting.")
        return
    try:
        total = parse_money(raw)
    except ValueError as e:
        print("Bad total:", e); return

    cats = defaultdict(Decimal)
    print("\nEnter category allocations. Leave category blank to finish.")
    while True:
        cat = ask("Category: ").strip()
        if cat == '':
            break
        amt_raw = ask(f"Amount for '{cat}': ").strip()
        if amt_raw == '':
            print("Empty amount, skipping entry.")
            continue
        try:
            amt = parse_money(amt_raw)
        except ValueError:
            print("Bad amount; try again.")
            continue
        cats[cat] += amt

    allocated = sum(cats.values())
    groceries = total - allocated

    print("\nCategory breakdown:")
    for c, v in sorted(cats.items(), key=lambda x: (-x[1], x[0])):
        print(f"{c:15} {v:8.2f}")
    print("-"*30)
    print(f"{'Allocated total:':15} {allocated:8.2f}")
    print(f"{'Total spent:':15} {total:8.2f}")
    print(f"{'Groceries:':15} {groceries:8.2f}")
    if groceries < 0:
        print("Warning: allocated more than total!")

if __name__ == '__main__':
    main()

