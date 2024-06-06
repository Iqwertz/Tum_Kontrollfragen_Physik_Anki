#Takes a input tex file and converts it to a anki deck
# Usage: python convert.py input.tex
# 

import genanki
import re
import sys
import os
import hashlib
import random

# Read the input file
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()
    
# Write the output file
def write_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)
        
inputPath = sys.argv[1] 
inputFilename = os.path.basename(inputPath)
input = read_file(sys.argv[1])

#Split into chapters
chaptersList = input.split("\\subsection")
chaptersList = chaptersList[1:]

print("Starting conversion...")

#Create dictionary of chapters
# chapters = {chapterName: [[chapterContent, [[question, answer], [question, answer], ...]]]}
chapters = {}
for chapter in chaptersList:
    #Get the chapter name
    name = re.search(r'{(.*?)}', chapter).group(1)
    #Get the chapter content
    content = re.search(r'{.*?}(.*)', chapter, re.DOTALL).group(1)
    #Add the chapter to the dictionary
    chapters[name] = content


qaChapters = {}
#Create a list of cards for each chapter
for chapter in chapters:
    #Get the content of the chapter
    content = chapters[chapter]
    #Split the content into cards
    cards = content.split("\\noindent\\textbf")
    cards = cards[1:]
    
    qaCards = []
    #Create a question and answer for each card
    for card in cards:
        #Get the question // everything between the curly braces
        question = re.search(r'{(.*?)}', card).group(1)
        #Get the answer // everything after the curly braces
        answer = re.search(r'{.*?}(.*)', card, re.DOTALL).group(1)

        qaCards.append([question, answer])
        
    qaChapters[chapter] = qaCards
        

#Anki Models:
cardModel = genanki.Model(
    int(hashlib.sha256(inputFilename.encode("utf-8")).hexdigest()[:7], base=16),
    inputFilename,
    fields=[
      {'name': 'Frage'},
      {'name': 'Antwort'},
    ],

    templates=[
      {
        'name': inputFilename + ' StandardCard',
        'qfmt': '{{Frage}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Antwort}}',
      },
    ],
  )

cardModelSorted = genanki.Model(
       int(hashlib.sha256(inputFilename.encode("utf-8")).hexdigest()[:7], base=16) + 1,
    inputFilename + ' sortiert',
    fields=[
      {'name': 'Frage'},
      {'name': 'Antwort'},
    ],

    templates=[
      {
        'name': inputFilename + ' StandardCard Sorted',
        'qfmt': '{{Frage}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Antwort}}',
      },
    ],
  )

mediaFiles = []
sortedDecks = []
unsortedDeck = genanki.Deck(
    random.randint(0, 100000),
      "TUM "+inputFilename+" Kurzfragen"
)

#Render the cards to images
#delete temp folder if it exists
os.system("rm -rf temp")
#create temp folder:
os.system("mkdir temp")

def generateTexString(content):
    #Read header
    header = read_file("assets/header.tex")
    return header + "" + content + "" + "\\end{document}"

chapterCounter = 0
for chapter in qaChapters:
    sanitizedChapter = chapter.replace(" ", "")
    counter = 0
    chapterCounter += 1
    sortedDeck = genanki.Deck(
      random.randint(0, 100000),
      "TUM " + inputFilename + " Kurzfragen (sortiert)::" + str(chapterCounter) + ": " + chapter
    )
    for card in qaChapters[chapter]:
        print("Rendering card " + str(counter) + " of chapter " + sanitizedChapter)
        question = "\\noindent\\textbf{" + card[0] + "}"
        answer = card[1]
        #Write the question to a tex file
        questionTex = generateTexString(question)
        questionFileName = "temp/" + sanitizedChapter + "_" + str(counter) + "_question.tex"
        write_file(questionFileName, questionTex)
        #Write the answer to a tex file
        answerTex = generateTexString(answer)
        answerFileName = "temp/" + sanitizedChapter + "_" + str(counter) + "_answer.tex"
        write_file(answerFileName, answerTex)
        
        noExtensionAnswerFileName = "temp/" + sanitizedChapter + "_" + str(counter) + "_answer"
        noExtensionQuestionFileName = "temp/" + sanitizedChapter + "_" + str(counter) + "_question"
        #Render the question with latex2png
        os.system("latex2png -d 600 -c " + questionFileName)
        os.system("convert -border 50x50 -bordercolor white " + noExtensionQuestionFileName + ".png " + noExtensionQuestionFileName + ".png")
        
        #Render the answer with latex2png
        os.system("latex2png -d 600 -c " + answerFileName)
        os.system("convert -border 50x50 -bordercolor white " + noExtensionAnswerFileName + ".png " + noExtensionAnswerFileName + ".png")
        
        mediaFiles.append(noExtensionQuestionFileName + ".png")
        mediaFiles.append(noExtensionAnswerFileName + ".png")
        
        questionName = (noExtensionQuestionFileName + ".png").split("/")[-1]
        answerName = (noExtensionAnswerFileName + ".png").split("/")[-1]
        
        sortedFormatedQuestion = "<img id=\""+inputFilename+"sorted\" src=\"" + questionName + "\">"
        sortedFormatedAnswer = "<img id=\""+inputFilename+"sorted\" src=\"" + answerName + "\">"
        
        unsortedFormatedQuestion = "<img id=\""+inputFilename+"\" src=\"" + questionName + "\"> " #Added " " to make the questions of the unsorted deck have a diffrent hash than the sorted deck
        unsortedFormatedAnswer = "<img id=\""+inputFilename+"\" src=\"" + answerName + "\"> "
        
        sortedDeck.add_note(genanki.Note(
            model=cardModelSorted,
            fields=[sortedFormatedQuestion, sortedFormatedAnswer]
        ))
        
        unsortedDeck.add_note(genanki.Note(
            model=cardModel,
            fields=[unsortedFormatedQuestion, unsortedFormatedAnswer]
        ))
        
        counter += 1
        
    sortedDecks.append(sortedDeck)

sortedPackage = genanki.Package(sortedDecks)
sortedPackage.media_files = mediaFiles
sortedPackage.write_to_file(inputFilename + "_sorted.apkg")

unsortedPackage = genanki.Package(unsortedDeck)
unsortedPackage.media_files = mediaFiles
unsortedDeck.write_to_file(inputFilename + ".apkg")


#delete temp folder
os.system("rm -rf temp")