#!/usr/bin/env python2

import sys
import json
from datetime import datetime
from collections import Counter


def parse_csv(path):
    rows = []
    
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            
            raw_date, desc_with_amount = line.split(",", 1)
            raw_description, raw_amount = desc_with_amount.rsplit(",", 1)

            date = datetime.strptime(raw_date, "%Y-%m-%d").date()
            amount = float(raw_amount)

            rows.append((date, raw_description, amount))

    return rows


def get_category(description):
    description = description.lower()

    categories = json.load(open('categories.json'))
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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python print_expenses.py /path/to/csv"
        sys.exit(1)
    else:
        file_name = sys.argv[-1]
        
    rows = parse_csv(file_name)

    print "-- UNCATEGORISED --"
    for date, desc, amount in get_uncategorised_counts(rows):
        print "%s | %.2f\t| %s" % (date.strftime("%d %b"), amount, desc)

    category_counts = get_categorised_counts(rows)

    print "\n-- SUMMARY --"
    for category, total in category_counts.iteritems():
        print "%s: %.2f" % (category, total)

    total = get_total(rows)
    categorised_total = sum(category_counts.values())
    uncategorised_total = total - categorised_total
    print "\nCategorised total:\t%.2f" % categorised_total
    print "Uncategorised total:\t%.2f" % uncategorised_total

    print "\nTotal income:\t%.2f" % get_total_income(rows)
    print "Total expenses:\t%.2f" % get_total_expenses(rows)
    print "Net total:\t%.2f" % total
