# Converter for LaTeX to Anki

This code converts LaTeX files to Anki cards. The LaTeX files must be formatted in a specific way. The code extracts the questions and answers from the LaTeX files and creates a CSV file that can be imported into Anki.

The code here is specifically written for the "Vertiefungs" Modules of the TUM Physics Bachelor. The LaTeX files are made by Andre Scholz.

# Get the Anki cards

The newest version of the anki cards can be found in the release section of this repository.

# Develop

## Requirements

The code is written for Linux and requires the following packages:

- latex
- dvipng
- imagemagick
- optipng
- latex2png (sudo apt-get install latex2rtf)

## Convert

To convert the LaTeX files to Anki cards, run the following command:

```bash
python3 convert.py [name_of_the_LaTeX_file]
```
