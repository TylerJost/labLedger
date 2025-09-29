#!/bin/bash

# Change these to your name/email
AUTHOR="${1:-tjost@bwh.harvard.edu}"
BASE_DIR="${2:-/data}"  # Change to the base directory containing your repos
OUTPUT="${3:-/home/tyj566/misc/testEnv/gitLog.txt}"
SUMMARIZE="${4:-true}"

# Clear old output
> "$OUTPUT"

# Find all .git folders and loop through their parent directories
find "$BASE_DIR" -type d -name ".git" | while read gitdir; do
    REPO_DIR=$(dirname "$gitdir")
    	echo "$REPO_DIR"
        echo "=== $REPO_DIR ===" >> "$OUTPUT"
	    (
	            cd "$REPO_DIR" && \
			            git log --since="1 week ago" --author="$AUTHOR" --format='%h %ad %s' --date=short >> "$OUTPUT"
		        )
			    echo "" >> "$OUTPUT"
		    done

		    echo "Done! Logs saved to $OUTPUT"

if [[ "$SUMMARIZE" == 'true' ]]; then
	echo "Generating summary"
	pixi run python translate.py --text $OUTPUT
fi
