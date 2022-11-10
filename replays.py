import requests
import pprint
import json
import time

upload_url = "https://ballchasing.com/api/v2/upload?visibility=public"
token = 'HfPXqYhM1dsX0M1fZ2zHG3ceZbuRTOBOd4qShtHX'

def uploadStats(match_stats):
    r = requests.post('https://cwxskbsjnovkyqeloumw.supabase.co/rest/v1/rpc/fetchreplaytable', data = {'jay': match_stats}, headers = {'Content-Type': 'application/json', 'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3eHNrYnNqbm92a3lxZWxvdW13Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjMyNDgzODYsImV4cCI6MTk3ODgyNDM4Nn0.NtKg2p6BHRBbpm4FM0cAGA5lWWGkjWyt-oyvsQfZI_E', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3eHNrYnNqbm92a3lxZWxvdW13Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjMyNDgzODYsImV4cCI6MTk3ODgyNDM4Nn0.NtKg2p6BHRBbpm4FM0cAGA5lWWGkjWyt-oyvsQfZI_E'})
    if(r.status_code >= 200 and r.status_code <= 299):
        print("Success! Replays Uploaded!")
    
    




def fetch(token):
    fetch_url = "https://ballchasing.com/api/replays"
    params = {
        'group' : 'amogusballs-p8t77336hr'
    }
    r = requests.get(fetch_url, headers={
        'Authorization' : token
    },params=params)

    if(r.status_code == 200):
        print("Success! Replay Fetched!")
    
    replays = r.json()

    detailed_replays = []

    for replay in replays['list']:
        new_url = fetch_url + '/' + str(replay['id'])
        r = requests.get(new_url, headers={
            'Authorization' : token
        },params=params)

        if (r.status_code == 200):
            print("MORE SUCCESS! REPLAY WITH EXTRA STATS FETCHED")
        
        detailed_replays.append(r.json())
        time.sleep(0.8)
    
    return detailed_replays
    



replays = fetch(token)
match_stats = {}
for replay in replays:
    replay_index = replays.index(replay)
    for player in replays[replay_index]['blue']['players']:
        stats = player['stats']['core']
        if(player['name'] in match_stats):
            #will need to make average this is used as an example. Needs fixing!
            match_stats[player['name']]['shots'] += player['stats']['core']['shots']
            match_stats[player['name']]['shots_against'] += player['stats']['core']['shots_against']
            match_stats[player['name']]['goals'] += player['stats']['core']['goals']
            match_stats[player['name']]['goals_against'] += player['stats']['core']['goals_against']
            match_stats[player['name']]['saves'] += player['stats']['core']['saves']
            match_stats[player['name']]['assists'] += player['stats']['core']['assists']
            match_stats[player['name']]['score'] += player['stats']['core']['score']
            match_stats[player['name']]['shooting_percentage'] = round((match_stats[player['name']]['goals'] / match_stats[player['name']]['shots'])*100, 2)
            if (player['stats']['core']['mvp']):
                match_stats[player['name']]['mvp'] =+ 1
        else:
            match_stats.update({player['name'] : stats})
            if (player['stats']['core']['mvp']):
                match_stats[player['name']]['mvp'] = 1
            else:
                match_stats[player['name']]['mvp'] = 0
    for player in replays[replay_index]['orange']['players']:
        # pprint.pprint(player['stats']['core'])
        stats = player['stats']['core']
        if(player['name'] in match_stats):
            match_stats[player['name']]['shots'] += player['stats']['core']['shots']
            match_stats[player['name']]['shots_against'] += player['stats']['core']['shots_against']
            match_stats[player['name']]['goals'] += player['stats']['core']['goals']
            match_stats[player['name']]['goals_against'] += player['stats']['core']['goals_against']
            match_stats[player['name']]['saves'] += player['stats']['core']['saves']
            match_stats[player['name']]['assists'] += player['stats']['core']['assists']
            match_stats[player['name']]['score'] += player['stats']['core']['score']         
            match_stats[player['name']]['shooting_percentage'] = round((match_stats[player['name']]['goals'] / match_stats[player['name']]['shots'])*100, 2)
            if (player['stats']['core']['mvp']):
                match_stats[player['name']]['mvp'] =+ 1
        else:
            match_stats.update({player['name'] : stats})
            if (player['stats']['core']['mvp']):
                match_stats[player['name']]['mvp'] = 1
            else:
                match_stats[player['name']]['mvp'] = 0

# pprint.pprint(replays[0]['blue']['players'][0]['name'])
    #print out the names of each player for each replay!
    #based on team and whatever
print(match_stats)
jstats = json.dumps(match_stats, indent=4)

with open("D:/Bakkesmod Overlay Test/LiveMatchParser/hyper_ekes/match_stats.json", "w") as out:
    out.write(jstats)

uploadStats(str(match_stats))
time.sleep(3.0)