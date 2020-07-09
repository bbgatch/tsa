import requests
import lxml.html as lh
import pandas as pd
from datetime import datetime

# Guided by:
# https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059

# URL we want to pull data from.
url = "https://www.tsa.gov/coronavirus/passenger-throughput"

# Create handle for the site contents.
page = requests.get(url)

# Stor the contents of the website.
doc = lh.fromstring(page.content)

# Parse data stored between <tr>..</tr> of HTML tr_elements = doc.xpath('//tr')
tr_elements = doc.xpath('//tr')

# Pulling out the header names
colnames = []
for t in tr_elements[0]:
    name = t.text_content()
    colnames.append(name)
    print(name)

# Renaming column names.
colnames = ['Date', 'Travelers 2020', 'Travelers 2019']

# Creating lists of table data.
data = [[], [], []]
for row in tr_elements[1:]:
    i = 0
    for cell in row.iterchildren():
        datum = cell.text_content()
        datum = str(datum)
        data[i].append(datum)
        i += 1

# Converting to dictionary for easier transition to Pandas dataframe.
tsa = dict(zip(colnames, data))

# Converting from dictionary to Pandas dataframe.
tsa = pd.DataFrame(tsa)

# Changing data types.
tsa['Date'] = pd.to_datetime(tsa['Date'])
tsa['Travelers 2019'] = pd.to_numeric(tsa['Travelers 2019'].str.replace(',', ''))
tsa['Travelers 2020'] = pd.to_numeric(tsa['Travelers 2020'].str.replace(',', ''))

# Sorting by Date.
tsa = tsa.sort_values(by = 'Date')

# Getting today's date for filename.
today_date = datetime.today().strftime('%Y-%m-%d')

# Save dataframe as CSV with today's date included in filename.
tsa.to_csv("tsa_" + today_date + ".csv", index = False)
