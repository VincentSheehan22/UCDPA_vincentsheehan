# Script to append player stats into one CSV file.

import os
import glob
import pandas as pd


os.chdir("/Users/vincentsheehan/PycharmProjects/nhl-analysis/Dataset - NHL_Skaters_All-Time_Summary")

extension = 'csv'
files = [i for i in glob.glob(f'*.{extension}')]

# Combine all files in the list.
files_combined = pd.concat([pd.read_csv(file) for file in files])

# Export to CSV.
files_combined.to_csv("0001-7461.csv", index=False, encoding='utf-8-sig')

