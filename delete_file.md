#!/bin/bash

# Define the directory and pattern combined in the path
DIRECTORY="/path/to/your/folder/*-resource.txt"
LOG_FILE="/path/to/your/logfile.log"

# Start logging
echo "Starting the deletion process at $(date)" >> "$LOG_FILE"

# Loop through all files matching the pattern
for file in $DIRECTORY; do
  if [[ -f "$file" ]]; then
    rm -f "$file"
    echo "Deleted: $file" >> "$LOG_FILE"
  fi
done

# Log completion message
echo "Deletion process completed at $(date)" >> "$LOG_FILE"
