#!/usr/bin/env python3
# Invocation: ./pdf_to_csv.py PDF_SOURCE GRADUATION_TIME
# Arguments:
#   PDF_SOURCE: PDF file with table to be converted
#   GRADUATION_TIME: String indicating the graduation time, in "YEAR.MONTH" format
# Usage: Takes a PDF containing a (multi-page) table of graduating students, and extracts it to a csv file.

import sys
import os
import pandas as pd
import camelot
import re

if len(sys.argv)<=1 :
    sys.exit("PDF file expected as argument.")
elif not os.path.isfile(sys.argv[1]):
    sys.exit("PDF file does not exist.")
elif len(sys.argv)<=2:
    sys.exit("Graduation time missing.")

pdf_file = sys.argv[1]
graduation_date = sys.argv[2]

# Read tables into DataFrame
tables = camelot.read_pdf(pdf_file, pages='all')
table_frame = pd.concat([table_page.df for table_page in tables])
table_frame.reset_index(inplace=True,drop=True)
# Remove header row, set proper row names
table_frame.columns = ['#','ID','Surname','Name','Father\'s name']
table_frame.drop([0],inplace=True)
# Remove inline newlines from text
nl = re.compile('\n')
table_frame['ID'] = [nl.sub('', x) for x in table_frame['ID']]
table_frame['Surname'] = [nl.sub('', x) for x in table_frame['Surname']]
table_frame['Name'] = [nl.sub('', x) for x in table_frame['Name']]
table_frame['Father\'s name'] = [nl.sub('', x) for x in table_frame['Father\'s name']]

# Write DataFrame to csv
table_frame.to_csv(graduation_date, index=False, header=False)

