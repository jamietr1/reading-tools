#!/usr/bin/env python

import re
from os.path import expanduser

reading_list = expanduser("~") + "/Documents/reading-list/reading.md"
f=open(reading_list, 'r')
content = f.readlines()
prev_year = year_string = ""
total_books = total_pages = book_count = page_count = 0
year_count = 1
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

        #print "Title: ", title_string
        #print "Author: ", author
        #print "Pages: ", pages
        #print "Date: ", date
        #print "Year: ", current_year
        #print "Book type: ", book_type
        #print "Recommended: ", recommended
        #print "-----"

        if current_year != prev_year:
            if year_count != 1:
                print('{:<65} {:>4} {:>6}'.format(year_string, str(book_count), str(page_count)))
            else:
                print('{:<65} {:>4} {:>5}'.format('Year', 'Books', 'Pages'))
            year_string = current_year + " "
            book_count = page_count = 0
            prev_year = current_year
            year_count = year_count +1

        if book_type == "Paper":
            year_string = year_string + "#"
        elif book_type == "Audiobook":
            year_string = year_string + "@"
        elif book_type == "Ebook":
            year_string = year_string + "+"

        if "/" in pages:
            pp, audio = pages.split('/')
            pc = int(pp.replace('p', ''))
            page_count = page_count + int(pp.replace('p', ''))
        else:
            pc = int(pages.replace('p', ''))
            page_count = page_count + int(pages.replace('p', ''))


        book_count = book_count +1
        total_books = total_books + 1
        total_pages = total_pages + pc




f.close()
# Final year goes here
if year_count != 1:
    print('{:<65} {:>4} {:>6}'.format(year_string, str(book_count), str(page_count)))
else:
    print('{:<65} {:>4} {:>5}'.format('Year', 'Books', 'Pages'))
year_string = current_year + " "
book_count = page_count = 0
prev_year = current_year
year_count = year_count +1
print('{:<65} {:>4} {:>6}'.format('Total', total_books, total_pages))
