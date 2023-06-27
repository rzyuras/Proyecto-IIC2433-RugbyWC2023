import csv
from datetime import datetime

K_FACTOR = 32  # The constant K factor determines how much the ratings change after each match

# Read rugby_data.csv
with open('rugby_data.csv', 'r') as data_file:
    data_reader = csv.DictReader(data_file)
    data = list(data_reader)

# Read rugby_rankings.csv to obtain initial Elo ratings
with open('rugby_rankings.csv', 'r') as rankings_file:
    rankings_reader = csv.DictReader(rankings_file)
    rankings = list(rankings_reader)

# Initialize team ratings based on the closest world rugby ranking
team_ratings = {}  # Dictionary to store team ratings

for row in data:
    match_date = datetime.strptime(row['Date'], '%Y-%m-%d')

    closest_ranking = None
    closest_ranking_date_diff = None

    for ranking_row in rankings:
        ranking_date = datetime.strptime(ranking_row['Date'], '%Y-%m-%d')
        date_diff = abs((ranking_date - match_date).days)

        if closest_ranking is None or date_diff < closest_ranking_date_diff:
            closest_ranking = ranking_row
            closest_ranking_date_diff = date_diff

    home_team = row['Home Team']
    away_team = row['Away Team']

# Check if home team is in the ranking dictionary
    if home_team in closest_ranking:
        home_rank = int(closest_ranking[home_team])
    else:
        home_rank = 0  # Assign a default rank if missing in rankings

    # Check if away team is in the ranking dictionary
    if away_team in closest_ranking:
        away_rank = int(closest_ranking[away_team])
    else:
        away_rank = 0  # Assign a default rank if missing in rankings

    # Calculate initial Elo ratings based on world rugby ranking
    home_rating = 2000 - 10 * home_rank
    away_rating = 2000 - 10 * away_rank

    # Add the Elo ratings to the row
    row['Home Rank'] = home_rank
    row['Away Rank'] = away_rank
    row['Home Elo'] = home_rating
    row['Away Elo'] = away_rating
    

    # Update team ratings based on match result using the Elo update formula
    home_score = int(row['Home Score'])
    away_score = int(row['Away Score'])
    actual_home_score = 1 if home_score > away_score else 0
    actual_away_score = 1 if away_score > home_score else 0

    expected_home_score = 1 / (1 + 10 ** ((away_rating - home_rating) / 400))
    expected_away_score = 1 - expected_home_score

    home_new_rating = home_rating + K_FACTOR * (actual_home_score - expected_home_score)
    away_new_rating = away_rating + K_FACTOR * (actual_away_score - expected_away_score)

    # Store the updated ratings for the teams
    team_ratings[home_team] = home_new_rating
    team_ratings[away_team] = away_new_rating

# Write the updated data to a new file
output_file = 'rugby_data_with_elo.csv'
fieldnames = data[0].keys()

with open(output_file, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"The data with Elo ratings has been written to {output_file} successfully.")
