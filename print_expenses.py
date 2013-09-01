#!/usr/bin/env python2

import sys
import json
from datetime import datetime
from collections import Counter


def parse_csv(path):
    rows = []
    
    with open(path, 'r') as f:
        for line in f.readlines():
            raw_date, raw_description, raw_amount = line.strip().split(',')

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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python print_expenses.py /path/to/csv"
        sys.exit(1)
    else:
        file_name = sys.argv[-1]
        
    rows = parse_csv(file_name)

    categories = Counter()

    print "Uncategorised:"
    for date, desc, amount in rows:
        category = get_category(desc)

        if category:
            categories[category] += amount
        else:
            print "%s %s %.2f" % (date, desc, amount)

    print "\nSummary:"
    for category, total in categories.iteritems():
        print "%s: %.2f" % (category, total)

    total = sum(amount for (date, desc, amount) in rows)
    categorised_total = sum(categories.values())
    uncategorised_total = total - categorised_total
    print "\nCategorised total: %.2f" % categorised_total
    print "Uncategorised total: %.2f" % uncategorised_total
    print "Overall total: %.2f" % total
