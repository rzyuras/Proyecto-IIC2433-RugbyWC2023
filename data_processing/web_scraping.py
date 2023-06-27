import csv
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Set path to chromedriver executable
chrome_driver_path = '/usr/local/bin/chromedriver'

# Create a Chrome WebDriver instance
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

# Navigate to the website
driver.get('http://www.lassen.co.nz/pickandgo.php')

# Find the form fields and submit button
fyear_input = driver.find_element(By.NAME, 'txtfyear')
tyear_input = driver.find_element(By.NAME, 'txttyear')
submit_button = driver.find_element(By.NAME, 'Submit')

# Enter the desired values in the form fields
fyear_input.send_keys('2003')
tyear_input.send_keys('2023')

# Submit the form
submit_button.click()

# Wait for the page to load (add appropriate wait time if necessary)
driver.implicitly_wait(10)

# Get the resulting page source
page_source = driver.page_source

# Create a BeautifulSoup object to parse the page source
soup = BeautifulSoup(page_source, 'html.parser')

# Find all table rows excluding the header row
table = soup.find("table", attrs={"border": "0", "cellpadding": "2", "style": "border: 1px solid #000;"})

# Create a list to store the extracted data
data = []

# Process each row
for row in table.find_all("tr", bgcolor=lambda value: value != "#FFFFCC"):
    # Extract the required data using BeautifulSoup methods
    columns = row.find_all("td")

    # Extract the date and match information
    date = columns[0].text.strip()
    tournament = columns[1].text.strip()
    round_num = columns[2].text.strip()

    # Date to datetime object
    date = datetime.strptime(date, "%a, %d %b %Y").date()

    # Split the match into home and away teams
    match = columns[3].text.strip()
    home_team, away_team = match.split(" v ")

    # Extract the score, tries, and points
    score = columns[4].text.strip()
    tries = columns[5].text.strip()
    points = columns[6].text.strip()

    # Split the score into home and away values
    home_score, away_score = score.split("-")

    # Split the tries into home and away values
    home_tries, away_tries = tries.split(":")

    # Split the points into home and away values
    home_points, away_points = points.split("-")

    # Extract the venue and neutral information
    venue = columns[7].text.strip()
    neutral = 1 if columns[8].text.strip() == "Y" else 0

    # Append the extracted data as a dictionary to the data list
    data.append({
        "Date": date,
        "Tournament": tournament,
        "Round": round_num,
        "Home Team": home_team,
        "Away Team": away_team,
        "Home Score": home_score,
        "Away Score": away_score,
        "Home Tries": home_tries,
        "Away Tries": away_tries,
        "Home Points": home_points,
        "Away Points": away_points,
        "Venue": venue,
        "Neutral": neutral
    })

# Define the path of the CSV file
csv_file = "rugby_data.csv"

# Write the data to the CSV file
with open(csv_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

print("Data saved to:", csv_file)