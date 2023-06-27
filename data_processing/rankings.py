import requests
import csv
from bs4 import BeautifulSoup

# Send a GET request to the URL
url = 'https://commons.wikimedia.org/wiki/Data:Men%27s_World_Rugby_rankings.tab'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table element
table = soup.find('table', class_='mw-tabular')

# Extract table headers
headers = [th.get_text(strip=True) for th in table.select('thead th')]
headers = headers[-31:]

# Extract table rows
rows = []
for tr in table.select('tbody tr'):
    row = [td.get_text(strip=True) for td in tr.select('td')]
    rows.append(row)

new_headers = ['Date','NZL','AUS','SAF','FRA','ENG','IRE','WAL','SCO','ITA','SAM','FIJ','TON','ARG','USA','CAN','ROM','GEO','JAP','URU','POR','NAM','RUS','SPA','POL','CHL','HKG','BRA','BEL','NED','SWI']

# Save data to CSV file
with open('rugby_rankings.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(new_headers)
    writer.writerows(rows)

print('CSV file saved successfully.')

