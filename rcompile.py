#!/usr/bin/env python

import re
import argparse
import fuzzy
from os.path import expanduser

reading_list = expanduser("~") + "/Documents/reading-list/reading.md"
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
    soundex = fuzzy.Soundex(4)
    sfirst = soundex(first_name)
    slast = soundex(last_name)

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
author_index = expanduser("~") + "/Scripts/reading-tools/authors.dat"
auth = open(author_index, 'w')
for author in sorted(author_file):
    print>>auth, author
auth.close()

# Build reading list index
reading_list = expanduser("~") + "/Documents/reading-list/reading.md"
f=open(reading_list, 'r')
content = f.readlines()
reading_file = []

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

        reading_file.append(title_string + '|' + author + '|' + book_type + '|' + pages + '|' + date)
f.close()

# Write reading list index
list_index = expanduser("~") + "/Scripts/reading-tools/reading.dat"
reading = open(list_index, 'w')
for item in reading_file:
    print>>reading, item
reading.close()