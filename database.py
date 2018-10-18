import pymongo
from pymongo import MongoClient
from secrets import MONGO_DB_URI
import webbrowser

client = MongoClient(MONGO_DB_URI)
db = client.get_database().robolions

# To clear all data (a process that should be done after every event),
# go to mlab, sign in with webmaster@prhsrobotics.com, and go to the robolions collection
# and delete all documents in the robolions collection. Savvy?

def getData(team_number):
    if isinstance(team_number, dict):
        team_number = team_number['team_number']
    col = db.find_one({"team_number": team_number})
    matchlist = list(dict(col)['matches'])
    return matchlist

def setData(data_dict):
    if db.find_one({"team_number":data_dict['team_number']}) is None:  # creates a document for the given team
        db.insert_one({"team_number": int(data_dict['team_number'])})      # assuming that it doesn't exist
        db.update_one(
            {"team_number":data_dict['team_number']},
            {'$set':
                {'matches': []}  # create an empty list of matches to store individual match data
            }
        )
    db.update_one(
        {"team_number":data_dict['team_number']},
        {'$push':               # push a new match's data into the above created empty list (or full list if this is not the first
            {"matches":         # time this team has played in this specific event
                {
                "auto": data_dict['auto'],
                "switch_cubes": data_dict['switch_cubes'],
                "scale_cubes": data_dict['scale_cubes'],
                "vault_cubes": data_dict['vault_cubes'],
                "can_climb": data_dict['can_climb'],
                "type":data_dict['type'],
                "notes": data_dict['notes']
                }
            }
        }
    )


def getCollection():
    return db


def getAllTeamData():
    teams = []
    cursor = db.find()
    for team in cursor:
        teams.append(team)
    return teams

# AHH YES the big one
def getAlgorithmicRankings():
    # TODO create the algorithm and rank teams accordingly, no point in doing so till 2019 season tho
    return getSwitchRankings()

def getSwitchRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['switch_cubes']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$push':
                 {"switch_avg": average}
             }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['switch_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number]))
    return final


def getScaleRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['scale_cubes']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$push':
                 {"scale_avg": average}
             }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['scale_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number]))
    return final


def getVaultRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['vault_cubes']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$push':
                 {"vault_avg": average}
             }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['vault_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number]))
    return final


def printDataInBrowser(data_dict):
    webbrowser.open_new_tab('https://www.google.com/?q=' + str(data_dict))