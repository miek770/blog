#!/bin/bash

# Main reference
# https://tex.stackexchange.com/questions/34054/tex-to-image-over-command-line

# Arguments
# $1 = tex_string
# $2 = output file name (no extension)

echo "Converting LaTeX string '$1' to $2.png..."

# Create the PDF, using `formula.tex` as a template
pdflatex -output-directory tmp "\def\formula{$1}\input{formula.tex}"

# Create the PNG
# https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion
# convert -density 300 "tmp/formula.pdf" -quality 90 "tmp/$2.png"
# convert "tmp/formula.pdf" -resize 200% -quality 90 "tmp/$2.png"
# convert "tmp/formula.pdf" -scale 200% -quality 90 "tmp/$2.png"
#convert "tmp/formula.pdf" -colorspace RGB +sigmoidal-contrast 11.6933 \
#  -define filter:filter=Sinc -define filter:window=Jinc -define filter:lobes=3 \
#  -resize 150% -sigmoidal-contrast 11.6933 -colorspace sRGB -quality 100 "tmp/$2.png"
convert "tmp/formula.pdf" -scale 150% -quality 100 "tmp/$2.png"

# Cleanup
rm tmp/formula.*