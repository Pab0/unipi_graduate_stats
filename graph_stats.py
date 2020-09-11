#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv)<=2:
    sys.exit("Expected two arguments: one CSV data file and one CSV enrollment year file.")

csv_file = sys.argv[1]
enroll_file = sys.argv[2]

# Read total enrollments per year
enroll_df = pd.read_csv(enroll_file)
enroll_years = dict(enroll_df.values.tolist())

# Read graduation_data
df = pd.read_csv(csv_file)
df.columns = ['enrol_year', 'grad_year', 'years_studied']
cohorts_available = df.enrol_year.unique()
grad_freq = dict()
for cohort in cohorts_available:
    grad_freq[cohort] = dict()
    counts = df.query('enrol_year==@cohort').years_studied.value_counts()
    for years,students in counts.iteritems():
        grad_freq[cohort][years] = students
    print(list(grad_freq[cohort].values()))

#TODO: normalize data

# Plot data
width = 0.20

# Plot 0
plt.title("Years needed to graduate, general")
plt.hist(df.years_studied)
plt.savefig("histogram.png")

# Plot 1
plt.title("Years students needed to graduate, by enrollment year")
index=0
for cohort in cohorts_available:
    unique_years = np.array(list(grad_freq[cohort].keys()))
    print(unique_years)
    plt.bar(unique_years+[width*index]*len(unique_years), list(grad_freq[cohort].values()), width, label=cohort)
    index += 1

plt.legend(loc='best')
plt.xlabel("Years studied")
plt.ylabel("# of students")
plt.savefig("students_per_year_studied.png")

# Plot 2
index = 0

