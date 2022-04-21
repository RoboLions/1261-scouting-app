import pymongo
from pymongo import MongoClient
import webbrowser
from ranking_alg import RankingAlgorithm

MONGO_DB_URI = "mongodb+srv://scoutingapp:robo1261Lions@robolions.k3nbx.mongodb.net/robolions?retryWrites=true&w=majority"

client = MongoClient(MONGO_DB_URI)
db = client.get_database().worlds

# To clear all data (a process that should be done after every event),
# go to mlab, sign in with webmaster@prhsrobotics.com, and go to the robolions collection
# and delete all documents in the robolions collection. Savvy?
# 2022: robolions is columbus comp data, albany is albany comp data, state is state comp data, etc. kapeesh?


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
                    "disconnected": data_dict['disconnected'],
                    "disconnected_total_seconds": data_dict['disconnected_total_seconds'],
                    "crossed_tarmac": data_dict['crossed_tarmac'],
                    "match": data_dict['match'],
                    "auto_upper": data_dict['auto_upper'],
                    "auto_lower": data_dict['auto_lower'],
                    "teleop_upper": data_dict['teleop_upper'],
                    "teleop_lower": data_dict['teleop_lower'],
                    "type":data_dict['type'],
                    "driver":data_dict['driver'],
                    "defense":data_dict['defense'],
                    "position":data_dict['position'],
                    "speed":data_dict['speed'],
                    "stability":data_dict['stability'],
                    "accuracy":data_dict['accuracy'],
                    "climb": data_dict['climb'],
                    "climb_seconds": data_dict['climb_seconds'],
                    "notes": data_dict['notes'],
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


def getNumberOfTeams():
    return db.count_documents({})


# AHH YES the big one
def getAlgorithmicRankings():
    ranks = {}
    au = getAutoUpperRankings()
    al = getAutoLowerRankings()
    tu = getTeleopUpperRankings()
    tl = getTeleopLowerRankings()
    climb = getClimbRankings()
    driver = getDriverRankings()
    reach = getReachRankings()
    for team in getAllTeamData():
        num = team['team_number']
        t_au = au.index(int(num))
        t_al = al.index(int(num))
        t_tu = tu.index(int(num))
        t_tl = tl.index(int(num))
        t_driver = driver.index(int(num))
        t_climb = climb.index(int(num))
        t_reach = reach.index(int(num))
        algorithm = RankingAlgorithm(au=t_au, al=t_al, tu=t_tu, tl=t_tl, driver=t_driver, climb=t_climb, reach=t_reach, total_teams=getNumberOfTeams())
        ranks[num] = algorithm.getScore()
    final = list(sorted(ranks.keys(), key=lambda team_number: ranks[team_number], reverse=True))
    return final


def getAutoUpperRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['auto_upper']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"au_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['au_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getAutoLowerRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['auto_lower']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"al_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['al_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

def getTeleopUpperRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['teleop_upper']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"tu_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['tu_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

def getTeleopLowerRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['teleop_lower']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"tl_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['tl_avg']
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


def getClimbRankings():
    # based off to what rung they can climb to, doesn't account for time taken to climb
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            score = 0
            most_common_climb = str(match['climb']).lower()
            if most_common_climb == "traverse":
                score = 4
            elif most_common_climb == "high":
                score = 3
            elif most_common_climb == "mid":
                score = 2
            elif most_common_climb == "low":
                score = 1
            elif most_common_climb == "cannot":
                score = 0
            elif most_common_climb == "did not":
                score = 0
            elif most_common_climb == "attempted":
                score = 0
            data.append(score)
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"climb_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['climb_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getReachRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            score = 0
            most_common_reach = str(match['type']).lower()
            if most_common_reach == "shoots high from launchpad":
                score = 4
            elif most_common_reach == "shoots high and low":
                score = 3
            elif most_common_reach == "shoots high":
                score = 2
            elif most_common_reach == "shoots low":
                score = 1
            elif most_common_reach == "cannot shoot":
                score = 0
            data.append(score)
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"type_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['type_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

def getDefenseRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            score = 0
            most_common_defense = str(match['type']).lower()
            if most_common_defense == "good defense":
                score = 2
            elif most_common_defense == "bad defense":
                score = 1
            elif most_common_defense == "no defense":
                score = 0
            data.append(score)
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"type_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['type_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def printDataInBrowser(data_dict):
    webbrowser.open_new_tab('https://www.google.com/?q=' + str(data_dict))  # yes
