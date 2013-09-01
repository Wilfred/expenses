# Expenses Tracking

This is a Python script for categorising personal finance expenses. It
consumes CSV files in the format exported by HSBC.

GPL license.

To run it, you will need a categories.json in this directory. This is
very specific to the user (and contains personal data), so we don't
include it in the repo. To get started, create a categories.json with
the following contents:

    {
        "Utilities": {
            "start": [
                "thames water",
                "virgin mobile",
            ]
        }, "Food": {
            "contains": [
                "tesco"
            ], "start": [
                "sainsburys",
                "w m morrisons",
            ]
    }

You can then run the script with:

    $ python print_expenses.py /path/to/your.csv

A CSV file should take the following format:

    2012-12-31,SAINSBURYS,-10.00
