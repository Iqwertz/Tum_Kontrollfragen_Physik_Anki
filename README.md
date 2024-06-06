## Requirements

The code is written for Linux and requires the following packages:

- latex
- dvipng
- imagemagick
- optipng

Converted with: https://github.com/mneri/pnglatex/blob/master/pnglatex

for pnglatex the execution flag must be set with `chmod +x pnglatex`

pnglatex -d 800 -m 10 -s 20 -f "\\noindent\\textbf{4. Wie ändert sich die Exergie eines Systems A, wenn dieses System eine Wärmemenge $Q$ isotherm aufnimmt oder abgibt?}\\" -H header.tex -l output.log

install latex2png with `sudo apt-get install latex2png`
