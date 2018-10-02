import pymongo
from pymongo import MongoClient
from secrets import MONGO_DB_URI
import webbrowser

client = MongoClient(MONGO_DB_URI, connectTimeoutMS=30000)
db = client.get_database().robolions

def getData():
    col = db.find_one({"team_number":1261})
    return col

def setData(data_dict):
    db.update_one(
        {"team_number":1261},
        {'$set':
            {"balls_thrown": data_dict['balls_thrown'],
             "can_climb": data_dict['can_climb'],
             "team_color": data_dict['team_color'],
             "notes": data_dict['notes']}
        }
    )

def printDataInBrowser(data_dict):
    webbrowser.open_new_tab('https://www.google.com/?q=' + str(data))
