#!/bin/bash

announcements_dir="announcements"

# 1. Download files
# ./get_docs.py

# 2. Convert files to PDFs
for announcement_file in $announcements_dir/*; do
	# Skip files already generated from previous runs
	echo "$announcement_file"
	if [[ $announcement_file == *.pdf ]]
	then
		echo "skipping pdf"
		continue
	fi

	file_type="$(file -b "$announcement_file" | sed 's/,.*//g')"
	# No need to convert HTML files.
	case $file_type in
		"Composite Document File V2 Document"|"Microsoft Word 2007+")
			lowriter --headless --convert-to pdf --outdir "$announcements_dir" $announcement_file
			;;
		"PDF document")
			cp "$announcement_file" "$announcement_file.pdf"

	esac
done



# Extract table to CSV
for pdf_file in "$announcements_dir/*.pdf"; do
	./pdf_to_csv.py "$pdf_file" "${pdf_file%:*}"
done
