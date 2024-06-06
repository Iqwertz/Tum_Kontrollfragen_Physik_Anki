#Takes a input tex file and converts it to a anki deck
# Usage: python convert.py input.tex output.apkg
# 

import genanki
import re
import sys
import os

# Read the input file
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()
    
# Write the output file
def write_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)
        
input = read_file(sys.argv[1])
outputPath = sys.argv[2]

#Split into chapters
chaptersList = input.split("\\subsection")
chaptersList = chaptersList[1:]

#Create dictionary of chapters
# chapters = {chapterName: [chapterContent, [[question, answer], [question, answer], ...]]}
chapters = {}
for chapter in chaptersList:
    #Get the chapter name
    name = re.search(r'{(.*?)}', chapter).group(1)
    #Get the chapter content
    content = re.search(r'{.*?}(.*)', chapter, re.DOTALL).group(1)
    #Add the chapter to the dictionary
    chapters[name] = [content]


#Create a list of cards for each chapter
for chapter in chapters:
    #Get the content of the chapter
    content = chapters[chapter][0]
    #Split the content into cards
    cards = content.split("\\noindent\\textbf")
    cards = cards[1:]
    
    #Create a question and answer for each card
    for card in cards:
        #Get the question // everything between the curly braces
        question = re.search(r'{(.*?)}', card).group(1)
        #Get the answer // everything after the curly braces
        answer = re.search(r'{.*?}(.*)', card, re.DOTALL).group(1)
        #Add the card to the chapter
        chapters[chapter].append([question, answer])
        
        
for chapter in chapters:
    for card in chapters[chapter]:
        print(card)
        
#Render the cards to images
#create temp folder:
os.system("mkdir temp")

for chapter in chapters:
    counter = 0
    for card in chapters[chapter]:
        question = "\\noindent\\textbf{" + card[0] + "}"
        answer = card[1]
        #run pnglatex and check if there is any output
        print("convert: " + question)
        os.system("pnglatex -d 300 -f" + question + "-o temp/" + chapter + "_question_" + str(counter) + ".png ")