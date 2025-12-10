#!/bin/bash

set -euo pipefail

# Change this config to your name/email
source labrat.conf

# Clear old output
# > "$OUTPUT"
OUTPUTTEMP='./lastWeekOutput.txt'
printf "\n\n`date +%F` ----\n" >> "$OUTPUT"
# Find all .git folders and loop through their parent directories
find "$BASE_DIR" -type d -name ".git" | while read gitdir; do
    REPO_DIR=$(dirname "$gitdir")
    	echo "$REPO_DIR"
        echo "repository: $REPO_DIR" >> "$OUTPUT"

	    (
	            cd "$REPO_DIR" && \
			            git log --since="1 week ago" --author="$AUTHOR" --format='%h %ad %s' --date=short >> "$OUTPUT"
		)
			    echo "" >> "$OUTPUT"

		    done

		    echo "Done! Logs saved to $OUTPUT"

if [[ "$SUMMARIZE" == 'true' ]]; then
	echo "Generating summary"
	pixi run python translate.py --text $OUTPUT --d "`date +%F`"
fi
