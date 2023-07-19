#!/bin/bash

# Main reference
# https://tex.stackexchange.com/questions/34054/tex-to-image-over-command-line

# Arguments
# $1 = tex_string
# $2 = output file name (no extension)
# $3 = small image (if $3 == "--small")

# Determine the template file to use based on the optional argument
if [[ "$3" == "--small" ]]; then
  echo "Converting LaTeX string '$1' to $2.png..."
  template="inline"
else
  echo "Converting LaTeX formula '$1' to $2.png..."
  template="formula"
fi

# Create the PDF, using `formula.tex` as a template
pdflatex -output-directory tmp "\def\formula{$1}\input{$template}.tex"

# Create the PNG
convert "tmp/$template.pdf" -quality 90 "tmp/$2.png"

# Cleanup
rm tmp/$template.*
