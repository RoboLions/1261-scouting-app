import pymongo
from pymongo import MongoClient
from secrets import MONGO_DB_URI
import webbrowser
from ranking_alg import RankingAlgorithm

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


def getNumberOfTeams():
    return db.count()


# AHH YES the big one
def getAlgorithmicRankings():
    ranks = {}
    low = getLowRankings()
    high = getHighRankings()
    driver = getDriverRankings()
    climb = getClimbRankings()
    auto = getAutoRankings()
    reach = getReachRankings()
    for team in getAllTeamData():
        num = team['team_number']
        t_low = low.index(int(num))
        t_high = high.index(int(num))
        t_driver = driver.index(int(num))
        t_climb = climb.index(int(num))
        t_auto = auto.index(int(num))
        t_reach = reach.index(int(num))
        algorithm = RankingAlgorithm(low=t_low, high=t_high, driver=t_driver, climb=t_climb, auto=t_auto, reach=t_reach, total_teams=getNumberOfTeams())
        ranks[num] = algorithm.getScore()
    final = list(sorted(ranks.keys(), key=lambda team_number: ranks[team_number], reverse=True))
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


def getClimbRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            score = 0
            most_common_climb = str(match['climb']).lower()
            if most_common_climb == "balance":
                score = 3
            elif most_common_climb == "climb":
                score = 2
            elif most_common_climb == "park":
                score = 1
            elif most_common_climb == "cannot":
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


def getAutoRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            score = 0
            most_common_auto = str(match['auto']).lower()
            if most_common_auto == "4+ balls high":
                score = 5
            elif most_common_auto == "3 balls high":
                score = 4
            elif most_common_auto == "4+ balls low":
                score = 3
            elif most_common_auto == "3 balls low":
                score = 2
            elif most_common_auto == "auto line only":
                score = 1
            elif most_common_auto == "nothing":
                score = 0
            data.append(score)
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"auto_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['auto_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getReachRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            score = 0
            most_common_reach = str(match['type']).lower()
            if most_common_reach == "high":
                score = 2
            elif most_common_reach == "low":
                score = 1
            elif most_common_reach == "defense":
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