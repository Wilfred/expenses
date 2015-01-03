#!/usr/bin/env python2

import os
import sys
import json
import datetime as dt
from collections import Counter


def parse_csv(path):
    rows = []
    
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            
            raw_date, desc_with_amount = line.split(",", 1)
            raw_description, raw_amount = desc_with_amount.rsplit(",", 1)

            date = dt.datetime.strptime(raw_date, "%Y-%m-%d").date()
            amount = float(raw_amount)

            rows.append((date, raw_description, amount))

    return sorted(rows, key=lambda (date, desc, amount): date)


def get_category(description):
    description = description.lower()

    try:
        categories = json.load(open('categories.json'))
    except ValueError as e:
        print "Could not parse categories.json: %s" % e
        sys.exit(1)

    for category, keywords in categories.iteritems():
        for start_keyword in keywords.get('start', []):
            if description.startswith(start_keyword):
                return category

        for generic_keyword in keywords.get('contains', []):
            if generic_keyword in description:
                return category

    return None


def get_categorised_counts(rows):
    categories = Counter()

    for date, desc, amount in rows:
        category = get_category(desc)

        if category:
            categories[category] += amount

    return categories


def get_uncategorised_counts(rows):
    for date, desc, amount in rows:
        category = get_category(desc)

        if not category:
            yield (date, desc, amount)


def get_total(rows):
    total = 0
    for date, desc, amount in rows:
        total += amount

    return total


def get_total_income(rows):
    total = 0
    for date, desc, amount in rows:
        if amount > 0:
            total += amount

    return total


def get_total_expenses(rows):
    total = 0
    for date, desc, amount in rows:
        if amount < 0:
            total += amount

    return total


def get_terminal_width():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns)


def print_heading(text):
    print "-- {} ".format(text.upper()).ljust(get_terminal_width(), '-')


def print_tuples(pairs):
    """Pretty-print an iterable of (text, amount) tuples ordered by
    amount.

    """
    pairs = list(pairs)

    longest_text = max([text for (text, _) in pairs],
                       key=len)
    
    def abs_amount(pair):
        text, amount = pair
        return abs(amount)

    for text, amount in sorted(pairs, key=abs_amount):
        print "{}: {:8.2f}".format(
            text.rjust(len(longest_text)), amount)


def print_summary(rows):
    category_counts = get_categorised_counts(rows)

    print_heading('by category')
    print_tuples(category_counts.iteritems())
    print

    print_heading('category totals')
    
    total = get_total(rows)
    categorised_total = sum(category_counts.values())
    uncategorised_total = total - categorised_total
    print_tuples([
        ('Categorised', categorised_total),
        ('Uncategorised', uncategorised_total)
    ])
    print

    print_heading('overall totals')
    print_tuples([
        ('Income', get_total_income(rows)),
        ('Expenses', get_total_expenses(rows)),
        ('Net', total)
    ])


def print_uncategorised(rows):
    def abs_amount(count_tuple):
        date, desc, amount = count_tuple
        return abs(amount)
    
    print "-- UNCATEGORISED --"
    for date, desc, amount in sorted(
            get_uncategorised_counts(rows), key=abs_amount):
        space = "  " if amount > 0 else " "
        print "%s |%s%.2f\t| %s" % (date.strftime("%d %b %Y"),
                                    space, amount, desc)


def print_slush(rows):
    today = dt.date.today()

    remaining_bills_total = 0

    bills = json.load(open('bills.json'))['bills']
    for bill in bills:
        if bill['day'] >= today.day:
            remaining_bills_total += bill['amount']

    total = get_total(rows)

    print "Remaining bills (approx): %.2f" % remaining_bills_total
    print "Remaining money: %.2f" % total
    print "Slush remaining (approx): %.2f" % (total - remaining_bills_total)


def print_usage():
    print "Usage: "
    print "./print_expenses.py <csv_path> --summary"
    print "./print_expenses.py <csv_path> --misc"
    print "./print_expenses.py <csv_path> --slush"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    else:
        file_name = sys.argv[1]
        
    rows = parse_csv(file_name)

    if "--summary" in sys.argv:
        print_summary(rows)
    elif "--misc" in sys.argv:
        print_uncategorised(rows)
    elif "--slush" in sys.argv:
        print_slush(rows)
    else:
        print_usage()
        sys.exit(1)
