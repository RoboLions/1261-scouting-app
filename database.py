import pymongo
from pymongo import MongoClient
import webbrowser
from ranking_alg import RankingAlgorithm

MONGO_DB_URI = "mongodb+srv://scoutingapp:robo1261Lions@robolions.k3nbx.mongodb.net/robolions?retryWrites=true&w=majority"

client = MongoClient(MONGO_DB_URI)
db = client.get_database().test2023

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
                    "match": data_dict['match'],
                    "cone_auto_top": data_dict['cone_auto_top'],
                    "cone_auto_middle": data_dict['cone_auto_middle'],
                    "cone_auto_hybrid": data_dict['cone_auto_hybrid'],
                    "cone_teleop_top": data_dict['cone_teleop_top'],
                    "cone_teleop_middle": data_dict['cone_teleop_middle'],
                    "cone_teleop_hybrid": data_dict['cone_teleop_hybrid'],
                    "cube_auto_top": data_dict['cube_auto_top'],
                    "cube_auto_middle": data_dict['cube_auto_middle'],
                    "cube_auto_hybrid": data_dict['cube_auto_hybrid'],
                    "cube_teleop_top": data_dict['cube_teleop_top'],
                    "cube_teleop_middle": data_dict['cube_teleop_middle'],
                    "cube_teleop_hybrid": data_dict['cube_teleop_hybrid'],
                    "auto_charge": data_dict['auto_charge'],
                    "teleop_charge": data_dict['teleop_charge'],
                    "starting_pos": data_dict['starting_pos'],
                    "name": data_dict['name'],
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

# def getAlgorithmicRankings():
#     ranks = {}
#     auto_top = getConeAutoTop()
#     al = getAutoLowerRankings()
#     tu = getTeleopUpperRankings()
#     tl = getTeleopLowerRankings()
#     climb = getClimbRankings()
#     driver = getDriverRankings()
#     reach = getReachRankings()
#     for team in getAllTeamData():
#         num = team['team_number']
#         t_au = auto_top.index(int(num))
#         t_al = al.index(int(num))
#         t_tu = tu.index(int(num))
#         t_tl = tl.index(int(num))
#         t_driver = driver.index(int(num))
#         t_climb = climb.index(int(num))
#         t_reach = reach.index(int(num))
#         algorithm = RankingAlgorithm(au=t_au, al=t_al, tu=t_tu, tl=t_tl, driver=t_driver, climb=t_climb, reach=t_reach, total_teams=getNumberOfTeams())
#         ranks[num] = algorithm.getScore()
#     final = list(sorted(ranks.keys(), key=lambda team_number: ranks[team_number], reverse=True))
#     return final

# Average of Cone Top, Mid, and Hybrid AUTO
def getConeAutoRankings():
    getConeAutoTopRankings()
    getConeAutoMiddleRankings()
    getConeAutoHybridRankings()
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = [team['ConeAutoTop_avg'], team['ConeAutoMiddle_avg'], team['ConeAutoHybrid_avg']]
        average = sum(rankings[int(team['team_number'])]) / len(rankings[int(team['team_number'])])
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"ConeAuto_avg": average}
            }
        )
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team["ConeAuto_avg"]
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

# Average of Cube Top, Mid, and Hybrid AUTO
def getCubeAutoRankings():
    getCubeAutoTopRankings()
    getCubeAutoMiddleRankings()
    getCubeAutoHybridRankings()
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = [team['CubeAutoTop_avg'], team['CubeAutoMiddle_avg'], team['CubeAutoHybrid_avg']]
        average = sum(rankings[int(team['team_number'])]) / len(rankings[int(team['team_number'])])
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"CubeAuto_avg": average}
            }
        )
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team["CubeAuto_avg"]
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

# Average of Cone Top, Mid, and Hybrid TELEOP
def getConeTeleopRankings():
    getConeTeleopTopRankings()
    getConeTeleopMiddleRankings()
    getConeTeleopHybridRankings()
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = [team['ConeTeleopTop_avg'], team['ConeTeleopMiddle_avg'], team['ConeTeleopHybrid_avg']]
        average = sum(rankings[int(team['team_number'])]) / len(rankings[int(team['team_number'])])
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"ConeTeleop_avg": average}
            }
        )
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team["ConeTeleop_avg"]
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

#Average of Cube Top, Mid, and Hybrid TELEOP
def getCubeTeleopRankings():
    getCubeTeleopTopRankings()
    getCubeTeleopMiddleRankings()
    getCubeTeleopHybridRankings()
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = [team['CubeTeleopTop_avg'], team['CubeTeleopMiddle_avg'], team['CubeTeleopHybrid_avg']]
        average = sum(rankings[int(team['team_number'])]) / len(rankings[int(team['team_number'])])
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"CubeTeleop_avg": average}
            }
        )
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team["CubeTeleop_avg"]
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

#________________________________________________________________________________________________________________________
#Cone AUTO

def getConeAutoTopRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cone_auto_top']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"ConeAutoTop_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['ConeAutoTop_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getConeAutoMiddleRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cone_auto_middle']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"ConeAutoMiddle_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['ConeAutoMiddle_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

def getConeAutoHybridRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cone_auto_middle']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"ConeAutoHybrid_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['ConeAutoHybrid_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final
# _______________________________________________________________________________________________________________________________________________________________________________________________________
# Cube AUTO
def getCubeAutoTopRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cube_auto_top']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"CubeAutoTop_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['CubeAutoTop_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getCubeAutoMiddleRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cube_auto_middle']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"CubeAutoMiddle_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['CubeAutoMiddle_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

def getCubeAutoHybridRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cube_auto_middle']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"CubeAutoHybrid_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['CubeAutoHybrid_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final
#_____________________________________________________________________________________________________________________________________________________________________________
#Cone TELEOP

def getConeTeleopTopRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cone_teleop_top']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"ConeTeleopTop_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['ConeTeleopTop_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getConeTeleopMiddleRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cone_teleop_middle']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"ConeTeleopMiddle_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['ConeTeleopMiddle_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

def getConeTeleopHybridRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cone_teleop_hybrid']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"ConeTeleopHybrid_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['ConeTeleopHybrid_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

# _______________________________________________________________________________________________________________________________________________________________________________________________________
# Cube TELEOP

def getCubeTeleopTopRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cube_teleop_top']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"CubeTeleopTop_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['CubeTeleopTop_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final


def getCubeTeleopMiddleRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cube_teleop_middle']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"CubeTeleopMiddle_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['CubeTeleopMiddle_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

def getCubeTeleopHybridRankings():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            data.append(int(match['cube_teleop_middle']))
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"CubeTeleopHybrid_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['CubeTeleopHybrid_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final
# 

def getChargingPortAuto():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            score = 0
            auto_charge = str(match['auto_charge']).lower()
            if auto_charge == "engaged auto":
                score = 2
            elif auto_charge == "docked auto":
                score = 1
            elif auto_charge == "n/a":
                score = 0
            data.append(score)
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"AutoCharge_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['auto_charge_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

def getChargingPortTeleop():
    data = []
    for team in getAllTeamData():
        for match in team['matches']:
            score = 0
            teleop_charge = str(match['teleop_charge']).lower()
            if teleop_charge == "engaged teleop":
                score = 2
            elif teleop_charge == "docked teleop":
                score = 1
            elif teleop_charge == "n/a":
                score = 0
            data.append(score)
        average = sum(data) / len(data)
        db.update_one(
            {"team_number":team['team_number']},
            {'$set':
                 {"TeleopCharge_avg": average}
            }
        )
        data = []
    rankings = {}
    for team in getAllTeamData():
        rankings[int(team['team_number'])] = team['TeleopCharge_avg']
    final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    return final

#def getDefenseRankings():
#   data = []
#    for team in getAllTeamData():
    #     for match in team['matches']:
    #         score = 0
    #         most_common_defense = str(match['type']).lower()
    #         if most_common_defense == "good defense":
    #             score = 2
    #         elif most_common_defense == "bad defense":
    #             score = 1
    #         elif most_common_defense == "no defense":
    #             score = 0
    #         data.append(score)
    #     average = sum(data) / len(data)
    #     db.update_one(
    #         {"team_number":team['team_number']},
    #         {'$set':
    #              {"type_avg": average}
    #         }
    #     )
    #     data = []
    # rankings = {}
    # for team in getAllTeamData():
    #     rankings[int(team['team_number'])] = team['type_avg']
    # final = list(sorted(rankings.keys(), key=lambda team_number: rankings[team_number], reverse=True))
    # return final


def printDataInBrowser(data_dict):
    webbrowser.open_new_tab('https://www.google.com/?q=' + str(data_dict))  # yes
