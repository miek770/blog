#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_file>"
  exit 1
fi

# Input file name provided as an argument
input_file="$1"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
  echo "Error: Input file '$input_file' not found."
  exit 1
fi

# Extract filename without path and extension
filename=$(basename -- "$input_file")
# filename="${filename%.*}"
filename="${filename%%_*}"

# Generate a temporary file name for intermediate results
temp_file="tmp/result_temp.png"

# Scale the image to the specified width
convert "$input_file" -resize 768x "$temp_file"

# Crop the image to the specified height (centered)
convert "$temp_file" -gravity center -crop x150+0+0 "web/media/$filename.png"

rm "$temp_file"

echo "Banner saved as 'web/media/$filename.png'."
