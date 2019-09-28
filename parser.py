try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

print()
import requests
from bs4 import BeautifulSoup
import re
import sys
import os

if len(sys.argv) != 2:
    print("Input file with task to find on pythoshka")
    exit(1)

# to search 
path = sys.argv[1]

if not os.path.exists(path):
    print("File does not exist")
    exit(1)

with open(path, "r") as read:
    queryList = read.readlines()

    for i, query in enumerate(queryList):
        print("Handling task number: {}".format(i))
        url = ""
        flagFound = False

        for j in search(query, tld="com", lang='ru', num=5, stop=10, pause=2):
            if j.find("pythoshka") != -1:
                url = j
                flagFound = True
                break

        if not flagFound:
            print("Task on pythoshka not found")
            continue

        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'html.parser')

        code = ""
        regex = re.compile('brush*')
        for codeDivs in soup.find_all("pre", {"class": regex}):
            code += codeDivs.get_text()

        with open("out_{}.py".format(i), "w") as file:
            # avoiding first \n char
            file.write(code[1:])



