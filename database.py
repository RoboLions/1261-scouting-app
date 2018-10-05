import pymongo
from pymongo import MongoClient
from secrets import MONGO_DB_URI
import webbrowser

client = MongoClient(MONGO_DB_URI)
db = client.get_database().robolions

def getData(team_number):
    if isinstance(team_number, dict):
        team_number = team_number['team_number']
    col = db.find_one({"team_number": team_number})
    return dict(col)

def setData(data_dict):
    if db.find_one({"team_number":data_dict['team_number']}) is None:  # creates a document for the given team
        db.insert_one({"team_number": int(data_dict['team_number'])})      # assuming that it doesn't exist
    db.update_one(
        {"team_number":data_dict['team_number']},
        {'$set':
            {"auto": data_dict['auto'],
             "switch_cubes": data_dict['switch_cubes'],
             "scale_cubes": data_dict['scale_cubes'],
             "vault_cubes": data_dict['vault_cubes'],
             "can_climb": data_dict['can_climb'],
             "notes": data_dict['notes']}
        }
    )

def printDataInBrowser(data_dict):
    webbrowser.open_new_tab('https://www.google.com/?q=' + str(data_dict))

