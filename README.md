# Working With The Strava API

Looking at different functions of the Strava API and finding interesting things to do with them

## Club Activities
CURRENTLY PRIMARILY GEARED TOWARDS RUNNING CLUBS

Automatically:
- Gets an access token for your user
- Generates a json of activities for a given club using the access token, the club ID and the number of activities to generate

My Functions:
- print_all_activities: Prints all activities that Strava still has saved to your club, with an option for tracking total distance run across these activities
- get_activities_by_athlete and print_activities_by_athlete: Generates and prints a dictionary mapping athletes to their activities and the total distance they have run
- print_athlete_mileage: Uses the dictionary to print the total distance run for each athlete
- get_athlete_leaderboard and print_athlete_leaderboard: Generates and prints an ordered list of athletes sorted by total distance run from most to least

Usage:

main() function runs the file with a series of booleans determining which of the other functions will be run.
Takes as parameters:
- str client_id, str client_secret, str refresh_token
- int club_id, int per_page (how many activities to generate)
- bool print_all: true -> print_all_activities
- bool print_all_total_dist: true -> keep track of total distance while printing all activities
- bool get_activities_dict: true -> get_activities_by_athlete
- bool print_activities_dict: true -> print_activities_by_athlete
- bool print_mileage: true -> print_athlete_mileage
- bool get_leaderboard: true -> get_athlete_leaderboard and print_athlete_leaderboard

