#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>"
    return
fi

# Assign the first argument to the variable 'file'
file=$1

# Check if the file exists
if [ ! -f "$file" ]; then
    echo "Error: File '$file' not found!"
    return
fi

# Remove the file
rm "$file"

# Check if the removal was successful
if [ $? -eq 0 ]; then
    echo "File '$file' successfully removed."
else
    echo "Error: Failed to remove '$file'."
    return
fi
