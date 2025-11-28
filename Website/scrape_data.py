# Youimport requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from datetime import datetime

# URL of the SAMRC Weekly Deaths Report page
BASE_URL = "https://www.samrc.ac.za/reports/report-weekly-deaths-south-africa"

def get_latest_data():
    print("Fetching SAMRC page...")
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the link to the Excel file (usually contains "excess" and "data")
    # Note: This logic looks for the specific anchor text pattern SAMRC uses
    file_link = None
    for a in soup.find_all('a', href=True):
        if 'data for basic excess' in a.text.lower() or 'weekly deaths data' in a.text.lower():
            file_link = a['href']
            break

    if not file_link:
        print("Could not find data link.")
        return

    print(f"Found file: {file_link}")

    # Download the Excel file
    data_response = requests.get(file_link)
    with open('temp_data.xlsx', 'wb') as f:
        f.write(data_response.content)

    print("Processing Excel file...")
    # Read Excel - SAMRC usually has a 'Weekly Excess' sheet or similar
    # We load the sheet that typically contains the summary
    try:
        df = pd.read_excel('temp_data.xlsx', sheet_name=1) # Usually the 2nd sheet has the data
    except:
        # Fallback if sheet structure changes
        df = pd.read_excel('temp_data.xlsx')

    # CLEANING: This depends heavily on their specific format, which changes slightly.
    # This is a generic cleaner for the standard column headers they use.
    # We look for 'Week Date', 'Weekly Excess', etc.

    output_data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
        "source_url": file_link,
        "weeks": [],
        "deaths": []
    }

    # Iterate rows to find data (skipping header rows)
    # This assumes column 0 is Date/Week and Column 2 or 3 is Excess Deaths
    # You may need to adjust indices based on the specific Excel layout at the time
    for index, row in df.iterrows():
        # Simple heuristic to find data rows
        if isinstance(row[0], datetime) or (isinstance(row[0], str) and "-" in row[0]):
            try:
                week_date = str(row[0])
                # Assuming 'Total Deaths' or 'Excess' is in a specific column.
                # Let's grab column 1 (Weekly Deaths) for this example
                death_count = row[1]

                if pd.notna(death_count) and isinstance(death_count, (int, float)):
                    output_data["weeks"].append(week_date.split(" ")[0]) # Shorten date
                    output_data["deaths"].append(int(death_count))
            except Exception as e:
                continue

    # Save to JSON for the HTML website to read
    with open('mortality_data.json', 'w') as json_file:
        json.dump(output_data, json_file)

    print("Success! Data saved to mortality_data.json")

if __name__ == "__main__":
    get_latest_data()
r snippets
#
# Atom snippets allow you to enter a simple prefix in the editor and hit tab to
# expand the prefix into a larger code block with templated values.
#
# You can create a new snippet in this file by typing "snip" and then hitting
# tab.
#
# An example CoffeeScript snippet to expand log to console.log:
#
# '.source.coffee':
#   'Console log':
#     'prefix': 'log'
#     'body': 'console.log $1'
#
# Each scope (e.g. '.source.coffee' above) can only be declared once.
#
# This file uses CoffeeScript Object Notation (CSON).
# If you are unfamiliar with CSON, you can read more about it in the
# Atom Flight Manual:
# http://flight-manual.atom.io/using-atom/sections/basic-customization/#_cson
