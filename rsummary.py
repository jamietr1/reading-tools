#!/usr/bin/env python

import re
import argparse
from os.path import expanduser
from termcolor import colored
from math import modf

def GetHoursMinsFormat(hours):
    min_part, hour_part = modf(hours)
    str_time = str(int(hour_part)) + ':' + str(int(min_part*60))
    return str_time


def FormatGraph(year_string, book_count, page_count):
    output = year_string
    padding = 100 - (book_count + 5)
    output = output + " " * padding
    padding = 5 - len(str(book_count))
    output = output + " " * padding
    output = output + str(book_count)
    padding = 7 - len(str(page_count))
    output = output + " " * padding
    output = output + str(page_count)
    return output

def FormatLegend():
    output = "LEGEND: # = Paper   " + colored('+ = Ebook', 'blue', attrs=['bold']) + "   " + colored('@ = Audiobook', 'yellow')
    if args.author:
        output = output + "   " + colored('Red = ', 'red', attrs=['bold']) + args.author
    return output

parser = argparse.ArgumentParser(description='Summarize reading list data.')
parser.add_argument('-a', '--author', help='Highlight books by author.')
parser.add_argument('-f', '--from_year', help='Summarize each year from yyyy inclusive.')
parser.add_argument('-g', '--graph', action="store_true", help='Produces a graph for each year.')
parser.add_argument('-H', '--highlight', action="store_true", help='Highlights books by type.')
parser.add_argument('-l', '--legend', action="store_true", help='Displays a legend with the graph.')
parser.add_argument('-s', '--stats', action="store_true", help='Adds summary stats at the end of the listing.')
parser.add_argument('-u', '--until_year', help='Summarize each year until yyyy inclusive.')
args = parser.parse_args()


reading_list = expanduser("~") + "/Documents/home/reading-list/reading.md"
f=open(reading_list, 'r')
content = f.readlines()
stats = stat_line = ""
prev_year = year_string = ""
total_audio_time = audio_time = total_paper = total_audio = total_ebook = total_books = total_pages = book_count = page_count = 0
year_count = 0
dict = {}
for line in content:
    matchObj = re.match(r'^1.\s(.*)\s(edited by|by)\s(.*);\s(.*)\s\((.*)\)</br>', line, re.M|re.I)
    if matchObj:
        title_string = matchObj.group(1)
        titleMatchObj = re.match(r'^\*\*', title_string, re.M|re.I)
        if titleMatchObj:
            recommended = 'Yes'
        else:
            recommended = 'No'

        book_type = "Paper"

        titleMatchObj = re.search(r'\@', title_string, re.M|re.I)
        if titleMatchObj:
            book_type = "Audiobook"

        titleMatchObj = re.search(r'\+', title_string, re.M|re.I)
        if titleMatchObj:
            book_type = "Ebook"

        title_string = title_string.replace("*", "")
        title_string = title_string.replace("_", "")
        title_string = title_string.replace("@", "")
        title_string = title_string.replace("+", "")

        author = matchObj.group(3)
        pages = matchObj.group(4)
        date = matchObj.group(5)

        current_year = date[-4:]

        if current_year != prev_year:
            if args.from_year:
                if current_year < args.from_year:
                    continue
            if args.until_year:
                if current_year > args.until_year:
                    break
            #print len(year_string)
            if year_count != 0 and args.graph:
                print FormatGraph(year_string, book_count, page_count)
                stat_line = '{:<4} {:>3} {:>3} {:>3} {:>3} {:>5} {:>3} {:>5}'
            elif year_count == 0 and args.graph:
                print('{:<100} {:>4} {:>5}'.format('Year', 'Books', 'Pages'))
                stat_line = '{:<4} {:>3} {:>3} {:>3} {:>3} {:>5} {:>3} {:>5}'.format('Year', 'PB', 'EB', 'AB', 'TOT', 'PP', 'P/B', 'A/B')
            year_string = current_year + " "
            book_count = page_count = 0
            prev_year = current_year
            year_count = year_count +1

        if book_type == "Paper":
            type_string = "#"
            total_paper = total_paper + 1
        elif book_type == "Audiobook":
            if args.highlight:
                type_string = colored('@', 'yellow')
            else:
                type_string = "@"
            total_audio = total_audio + 1
            #year_string = year_string + "@"
        elif book_type == "Ebook":
            if args.highlight:
                type_string = colored('+', 'blue', attrs=['bold'])
            else:
                type_string = "+"
            total_ebook = total_ebook + 1
            #year_string = year_string + "+"

        if args.author:
            if author == args.author:
                year_string = year_string + colored(type_string, 'red', attrs=['bold'])
            else:
                year_string = year_string + type_string
        else:
            year_string = year_string + type_string

        if "/" in pages:
            pp, audio = pages.split('/')
            pc = int(pp.replace('p', ''))
            page_count = page_count + int(pp.replace('p', ''))
            hrs, mins = audio.split(':')
            total_mins = int(hrs)*60 + int(mins)
            audio_time = total_mins

        else:
            pc = int(pages.replace('p', ''))
            page_count = page_count + int(pages.replace('p', ''))


        book_count = book_count +1
        total_books = total_books + 1
        total_pages = total_pages + pc
        total_audio_time = total_audio_time + audio_time
    else:
        print line
f.close()
# Final year goes here
if year_count != 0 and args.graph:
    print FormatGraph(year_string, book_count, page_count)
elif year_count == 0 and args.graph:
    print('{:<100} {:>4} {:>6}'.format('Year', 'Books', 'Pages'))
year_string = current_year + " "
prev_year = current_year
print('{:<100} {:>4} {:>6}'.format('Total', total_books, total_pages))

if args.legend:
    print ""
    print FormatLegend()

if args.stats:
    print ""
    print "Statistical Summary"
    print "==================="
    print "Years:", year_count
    print "Books:", total_books
    print "  - Paper:", total_paper
    print "  - Ebook:", total_ebook
    print "  - Audio:", total_audio
    print "Stats:"
    print "  - Avg books/year:", str(total_books/year_count)
    print "  - Avg pages/year:", str(total_pages/year_count)
    print "  - Avg pages/book:", str(total_pages/total_books)
    if total_audio > 0:
        print "  - Avg audio time/book:", GetHoursMinsFormat(total_audio_time/total_audio/60.0)
