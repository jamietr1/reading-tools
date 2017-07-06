#!/usr/bin/env python

import readingapi
import argparse

# Arguement parser
parser = argparse.ArgumentParser(description='Summarize reading list data.')
parser.add_argument('-g', '--graph', action="store_true", help='Produces a graph for each year.')
parser.add_argument('-y', '--year', help='A year or comma-separated list of years')
args = parser.parse_args()

# list, summary

if args.command == "list":
    pass
elif args.command == "summary":
    pass
