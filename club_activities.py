import requests
import urllib3

# Request a new access token
def request_access_token(client_id, client_secret, refresh_token):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    auth_url = "https://www.strava.com/oauth/token"

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))

    return access_token

# Build the API url to get club activities
def get_club_activities(access_token, club_id, per_page):
    club_activities_url = f"https://www.strava.com/api/v3/clubs/{club_id}/activities?" \
                f"access_token={access_token}&per_page={per_page}"

    # Get the response in json format
    response = requests.get(club_activities_url)
    activities = response.json()

    return activities

# Print all activities accessed by the API call in get_club_activities
"""
Format: 
===== ACTIVITY =====
Athlete: 
Workout Title: 
Distance:
Total Distance: (optional)
"""
# Total distance is a running total of the distance run across all activities, 
# Is tallied when total_distance parameter is set to True
# Distances in miles (rounded to 2 decimals)
# NOTE: NEED TO WORK ON CATCHING UnicodeEncodeError MAYBE
def print_all_activities(activities, total_distance):
    total_dist_meters = 0
    
    for i, activity in enumerate(activities):
        total_dist_meters += activity['distance']
        print('='*5, f'ACTIVITY {i}', '='*5)
        print('Athlete:', activity['athlete']['firstname'], activity['athlete']['lastname'])
        print('Workout Title:', activity['name'])
        print('Distance:', round(activity['distance']/1609.34, 2), 'miles')
        if total_distance == True:
            print('Total Distance (miles):', round(total_dist_meters/1609.34, 2))
        print('='*15)

    if total_distance == True:
        total_dist_miles = total_dist_meters / 1609.34

        print("Total Miles So Far:", round(total_dist_miles, 2))

# Builds and returns dictionary "activities_by_athlete"
# key: athlete name, values: "runs" (list of their activities), "mileage" (float value of their distance run)
def get_activities_by_athlete(activities):
    activities_by_athlete = {}
    for activity in activities:
        athlete = f"{activity['athlete']['firstname']} {activity['athlete']['lastname']}"
        if athlete in activities_by_athlete:
            activities_by_athlete[athlete]["runs"].append(activity)
        else:
            activities_by_athlete[athlete] = {
                "runs": [activity],
                "mileage": 0
            }
        activities_by_athlete[athlete]["mileage"] += activity['distance']

    return activities_by_athlete

# Uses activities_by_athlete dictionary to print all activities grouped by athlete
# Distances in miles (rounded to 2 decimals)
"""
Format:
===== ATHLETE: =====
Workout Title: 
Distance:
=
Total Distance:
===============
"""
def print_activities_by_athlete(activities_by_athlete):
    for athlete in activities_by_athlete:
        print('='*5, f'ATHLETE: {athlete}', '='*5)
        activities = activities_by_athlete[athlete]["runs"]
        for activity in activities:
            print('Workout Title:', activity['name'])
            print('Distance:', round(activity['distance']/1609.34, 2), 'miles')
            print("=")
        print('Total Distance:', round(activities_by_athlete[athlete]["mileage"]/1609.34, 2), 'miles')
        print('='*15)

# Prints mileage of each athlete in the activities_by_athlete dictionary
"""
Format:
===== ATHLETE: =====
Number of Runs:
Mileage: 
==============
"""
def print_athlete_mileage(activities_by_athlete):
    for athlete in activities_by_athlete:
        print('='*5, f'ATHLETE: {athlete}', '='*5)
        print('Number of Runs:', len(activities_by_athlete[athlete]["runs"]))
        print('Mileage:', round(activities_by_athlete[athlete]["mileage"]/1609.34, 2), 'miles')
        print('='*15)

# Uses activities_by_athlete dictionary to get list of athletes in order of mileage from highest to lowest 
# Returns leaderboard
def get_athlete_leaderboard(activities_by_athlete):
    leaderboard = []
    inserted = False
    for athlete_a in activities_by_athlete:
        if not leaderboard:
            leaderboard.append(athlete_a)
        else:
            for i, athlete_b in enumerate(leaderboard):
                if activities_by_athlete[athlete_b]["mileage"] < activities_by_athlete[athlete_a]["mileage"]:
                    leaderboard.insert(i, athlete_a)
                    inserted = True
                    break
            if inserted == False:
                leaderboard.append(athlete_a)
        inserted = False
    return leaderboard

# Uses activities_by_athlete dictionary and leaderboard list to print the number of runs and total mileage
# of each athlete on the leaderboard in order
"""
Format:
===== #[place] =====
Number of Runs:
Mileage:
==============
"""
def print_athlete_leaderboard(activities_by_athlete, leaderboard):
    for i, a in enumerate(leaderboard):
        print('='*5, f'#{i+1}: {a}', '='*5)
        print('Number of Runs:', len(activities_by_athlete[a]["runs"]))
        print('Mileage:', round(activities_by_athlete[a]["mileage"]/1609.34, 2), 'miles')
        print('='*15)

# Main function with boolean statements to decide which functions to run
def main(client_id, client_secret, refresh_token, club_id, per_page, print_all, print_all_total_dist, 
         get_activities_dict, print_activities_dict, print_mileage, get_leaderboard):

    access_token = request_access_token(client_id, client_secret, refresh_token)
    activities = get_club_activities(access_token, club_id, per_page)

    if print_all == True:
        print_all_activities(activities, print_all_total_dist)
    
    if get_activities_dict == True:
        activities_by_athlete = get_activities_by_athlete(activities)

    if print_activities_dict == True:
        if get_activities_dict == False:
            print("print_activities_dict ERROR: activities_by_athlete dictionary not generated")
        else:
            print_activities_by_athlete(activities_by_athlete)
    
    if print_mileage == True:
        if get_activities_dict == False:
            print("print_mileage ERROR: activities_by_athlete dictionary not generated")
        else:
            print_athlete_mileage(activities_by_athlete)

    if get_leaderboard == True:
        if get_activities_dict == False:
            print("get_leaderboard ERROR: activities_by_athlete dictionary not generated")
        else:
            leaderboard = get_athlete_leaderboard(activities_by_athlete)
            print_athlete_leaderboard(activities_by_athlete, leaderboard)

# User Input:
# club_id, found in the URL when you access your club on the Strava website
# https://www.strava.com/clubs/#######/
club_id = 1161246

# per_page, the number of activities to read into the app from your club's total activities on Strava
# NOTE: maximum is 200, Strava only saves a certain amount of time into the past
# 200 activities will not necesssarily by available
per_page = 100

client_id = ""
client_secret = ""
refresh_token = ""

# print_all, set to true if you want to run the print_all_activities function to print all athlete activities
# Set print_all_total_dist to true if you want a running total of club mileage to be printed with the activities
print_all = True
print_all_total_dist = True

# get_activities_dict, set to true if you want to use the get_activities_by_athlete function 
# to build the activities_by_athlete dictionary
get_activities_dict = True

# print_activities_dict, set to true if you want to use the print_activities_by_athlete function to
# print all activities grouped by athlete
# Error generated if get_activities_dict is not set to True
print_activities_dict = True

# print_mileage, set to true if you want to use the print_athlete_mileage function to
# print mileage of each athlete in the activities_by_athlete dictionary
# Error generated if get_activities_dict is not set to True
print_mileage = True

# get_leaderboard, set to true if you want to use the get_athlete_leaderboard and print_athlete_leaderboard
# functions to build and print the athlete leaderboard
get_leaderboard = True

main(client_id, client_secret, refresh_token, club_id, per_page, print_all, print_all_total_dist, 
         get_activities_dict, print_activities_dict, print_mileage, get_leaderboard)

    
