#!/usr/local/bin/python

import re
import argparse
#import fuzzy
from os.path import expanduser
from datetime import datetime

reading_list = expanduser("~") + "/Documents/home/reading-list/reading.md"
f=open(reading_list, 'r')
content = f.readlines()
authors = author_file = []

for line in content:
    #print line
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

        # First we need to build an author index
        if " and " in author:
            author_list = author.split(' and ')
            for person in author_list:
                authors.append(person)
        elif "," in author:
            author_list = author.split(', ')
            for person in author_list:
                authors.append(person)
        else:
            authors.append(author)
f.close()

# remove duplicates
authors = list(set(authors))
author_file = []

for author in authors:
    # split into last, First
    names = author.split(' ')
    last_name = names[len(names)-1]
    del names[len(names)-1]
    first_name = " ".join(names)
    soundex = '' #fuzzy.Soundex(4)
    sfirst = '' #soundex(first_name)
    slast = '' #soundex(last_name)

    # list of books
    f=open(reading_list, 'r')
    content = f.readlines()
    book_line = 1
    book_list = ""
    for line in content:
        #print line
        matchObj = re.match(r'^1.\s(.*)\s(edited by|by)\s(.*);\s(.*)\s\((.*)\)</br>', line, re.M|re.I)
        if matchObj:
            book_author = matchObj.group(3)
            if author in book_author:
                book_list = book_list + str(book_line) + ','
        book_line = book_line +1
    f.close()

    author_file.append(last_name + "|" + first_name + '|' + author + '|' + slast + '|' + sfirst + '|' + book_list[:-1])

# Write author index
author_index = expanduser("~") + "/Documents/scripts/reading-tools/data/authors.dat"
auth = open(author_index, 'w')
for author in sorted(author_file):
    print>>auth, author
auth.close()

# Build reading list index
reading_list = expanduser("~") + "/Documents/home/reading-list/reading.md"
f=open(reading_list, 'r')
content = f.readlines()
reading_file = []
book_count = 1

for line in content:
    #print line
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

        pages = pages.replace('p', '')
        if '/' in pages:
            pages, time = pages.split('/')

        date = datetime.strptime(matchObj.group(5), "%m/%d/%Y")
        date = datetime.strftime(date, "%Y-%m-%d")

        reading_file.append(str(book_count) + '|' + date + '|' + title_string + '|' + author + '|' + book_type + '|' + pages)
    book_count = book_count +1
f.close()

# Write reading list index
list_index = expanduser("~") + "/Documents/scripts/reading-tools/data/reading.dat"
reading = open(list_index, 'w')
for item in reading_file:
    print>>reading, item
reading.close()

# Sort list by longest reading-tools
list_index = expanduser("~") + "/Documents/scripts/reading-tools/data/reading.dat"
f=open(list_index, 'r')
content = f.readlines()
length_list = {}

for line in content:
    line = line.rstrip()
    num, date, title, author, media, pages = line.split('|')
    pages = int(pages)
    if pages in length_list.keys():
        value = length_list[pages]
        value = value + ';' + date + '|' + title + '|' + author + '|' + media + '|' + str(pages)
        length_list[pages] = value
    else:
        length_list[pages] = date + '|' + title + '|' + author + '|' + media + '|' + str(pages)
f.close()

# Write reading length index
list_index = expanduser("~") + "/Documents/scripts/reading-tools/data/length.dat"
reading = open(list_index, 'w')
for key in sorted(length_list.iterkeys(), reverse=True):
    print>>reading, length_list[key]
reading.close()
