#!/bin/bash
# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <file_path> <remote_destination>"
    exit 1
fi

# Define the file path and remote destination
FILE_PATH=$1
REMOTE_DEST=$2

# Use scp to copy the file
xrdcp -f "$FILE_PATH" "$REMOTE_DEST"

# Check if the scp command was successful
if [ $? -eq 0 ]; then
    echo "File successfully copied to $REMOTE_DEST"
else
    echo "Failed to copy file to $REMOTE_DEST"
fi
