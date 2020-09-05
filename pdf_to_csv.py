#!/usr/bin/env python3

import sys
import os
import pandas as pd
import camelot
import re

if len(sys.argv)<=1 :
    sys.exit("PDF file expected as argument")
elif not os.path.isfile(sys.argv[1]):
    sys.exit("File does not exist.")

pdf_file = sys.argv[1]

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



print(tables)
print(table_frame)
print(table_frame.to_string())
