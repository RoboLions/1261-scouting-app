import pymongo
from pymongo import MongoClient
from secrets import MONGO_DB_URI
import webbrowser

client = MongoClient(MONGO_DB_URI)
db = client.get_database().robolions

# To clear all data (a process that should be done after every event),
# go to mlab, sign in with webmaster@prhsrobotics.com, and go to the robolions collection
# and delete all documents in the robolions collection. Savvy?


def getTeamLikabilityIndex(team_number):
    pass  # TODO CONNECT GOOGLE SHEETS TO PYTHON


def getData(team_number):
    if isinstance(team_number, dict):
        team_number = team_number['team_number']
    col = db.find_one({"team_number": team_number})
    matchlist = list(dict(col)['matches'])
    return matchlist


def getMostCommonClimb(team_number):
    data = getData(team_number)
    climbs = {}
    maximum = 0
    most_common = ""
    for match in data:
        try:
            climbs[match['climb']] += 1
        except KeyError:
            climbs[match['climb']] = 1
    for climb in climbs:
        if climbs[climb] > maximum:
            most_common = climb
    return most_common


def getMostCommonAuto(team_number):
    data = getData(team_number)
    autos = {}
    maximum = 0
    most_common = ""
    for match in data:
        try:
            autos[match['auto']] += 1
        except KeyError:
            autos[match['auto']] = 1
    for auto in autos:
        if autos[auto] > maximum:
            most_common = auto
    return most_common


def getMostCommonReach(team_number):
    data = getData(team_number)
    reaches = {}
    maximum = 0
    most_common = ""
    for match in data:
        try:
            reaches[match['type']] += 1
        except KeyError:
            reaches[match['type']] = 1
    for reach in reaches:
        if reaches[reach] > maximum:
            most_common = reach
    return most_common


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
                "disabled": data_dict['disabled'],
                "match": data_dict['match'],
                "auto": data_dict['auto'],
                "lower": data_dict['lower'],
                "outer": data_dict['outer'],
                "inner": data_dict['inner'],
                "climb": data_dict['climb'],
                "type":data_dict['type'],
                "driver":data_dict['driver'],
                "notes": data_dict['notes'],
                "scout_name": data_dict['scout_name']
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
    ranks = {}
    low = getLowRankings()
    high = getHighRankings()
    driver = getDriverRankings()
    climb = getClimbRankings()
    auto = getAutoRankings()
    reach = getReachRankings()
    categories = [low, high, driver, climb, auto, reach]
    for cat in categories:
        for team in cat:
            try:
                ranks[team] += cat.index(team)
            except:
                ranks[team] = 0
                ranks[team] += cat.index(team)
    final = list(sorted(ranks.keys(), key=lambda team_number: ranks[team_number], reverse=False))
    return final


def getLowRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['lower']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"low_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['low_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getHighRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            outer = int(match['outer'])
            inner = int(match['inner'])
            score = inner*2+outer
            data.append(score)
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"high_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['high_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getDriverRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['driver']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"driver_avg": average}
             }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['driver_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getAutoRankings():
    rankings = {}
    for team in getAllTeamData():
        score = 0
        most_common_auto = getMostCommonAuto(team)
        if most_common_auto == "4+ Balls High":
            score = 5
        elif most_common_auto == "3 Balls High":
            score = 4
        elif most_common_auto == "4+ Balls Low":
            score = 3
        elif most_common_auto == "3 Balls Low":
            score = 2
        elif most_common_auto == "Auto Line only":
            score = 1
        elif most_common_auto == "Nothing":
            score = 0
        rankings[int(team['team_number'])] = score
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getClimbRankings():
    rankings = {}
    for team in getAllTeamData():
        score = 0
        most_common_climb = getMostCommonClimb(team)
        if most_common_climb == "Balance":
            score = 3
        elif most_common_climb == "Climb":
            score = 2
        elif most_common_climb == "Park":
            score = 1
        elif most_common_climb == "Cannot":
            score = 0
        rankings[int(team['team_number'])] = score
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getReachRankings():
    rankings = {}
    for team in getAllTeamData():
        score = 0
        most_common_reach = getMostCommonReach(team)
        if most_common_reach == "High":
            score = 2
        elif most_common_reach == "Low":
            score = 1
        elif most_common_reach == "Defense":
            score = 0
        rankings[int(team['team_number'])] = score
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def printDataInBrowser(data_dict):
    webbrowser.open_new_tab('https://www.google.com/?q=' + str(data_dict))