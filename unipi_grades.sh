#!/bin/bash

announcements_dir="announcements"

# 1. Download files
# ./get_docs.py

# 2. Convert files to PDFs
for announcement_file in $announcements_dir/*; do
	# Skip files already generated from previous runs
	if [[ $announcement_file == *.pdf ]]
	then
		continue
	fi

	# Determine original file type
	file_type="$(file -b "$announcement_file" | sed 's/,.*//g')"
	case $file_type in
		"Composite Document File V2 Document"|"Microsoft Word 2007+")
			lowriter --headless --convert-to pdf --outdir "$announcements_dir" $announcement_file > /dev/null 2>&1
			;;
		"PDF document")
			cp "$announcement_file" "$announcement_file.pdf"
			;;
		# No need to convert HTML files.
	esac
done

# 3. Filter announcements that include the proper template
undergrad_template="undergrad.template"
for announcement_file in $announcements_dir/*.pdf; do
	is_undergrad=$(pdf2txt $announcement_file | grep -f $undergrad_template)
	if [ -z "$is_undergrad" ]; then
		rm "$announcement_file"
	fi
done

# 4. Extract graduation date
last_year=0
graduations_in_year=0
for announcement_file in $announcements_dir/*.pdf; do
	year=$(pdf2txt "$announcement_file" | grep -Eo -f undergrad_date.template | awk '{print $NF}')
	if (( year > last_year )); then
		graduations_in_year=0
	else
		graduations_in_year=$((graduations_in_year+1))
	fi
	last_year=$year
	mv "$announcement_file" "$announcements_dir"/"$year"."$graduations_in_year"."pdf"
done
	
# 5. Extract table to CSV
for pdf_file in "$announcements_dir"/*.pdf; do
	./pdf_to_csv.py "$pdf_file"
done
