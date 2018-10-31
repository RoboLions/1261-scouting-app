from flask import Flask, render_template, request
import database as db

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')  # the main page


@app.route('/submitdata', methods=['POST']) # ONLY the post responses will be filtered here and dealt with here
def submitData():
    formdata = dict(request.form)
    global num  # this process must be done with each integer that is collected
    try:
        num = int(formdata['team_number'][0])
    except:
        num = 0
    global switch
    try:
        switch = int(formdata['switch_cubes'][0])
    except:
        switch = 0
    global scale
    try:
        scale = int(formdata['scale_cubes'][0])
    except:
        scale = 0
    global vault
    try:
        vault = int(formdata['vault_cubes'][0])
    except:
        vault = 0
    data = {  # to clear things up, this data is the data of a single match
        'team_number': num,
        'auto': str(formdata['auto'][0]),
        'switch_cubes': switch,
        'scale_cubes': scale,
        'vault_cubes': vault,
        'can_climb': str(formdata['can_climb'][0]),
        'type': str(formdata['type'][0]),
        'notes': str(formdata['notes'][0])
    }
    db.setData(data)
    return render_template('confirm.html',
                           number=data['team_number'],
                           auto=data['auto'],
                           switch=data['switch_cubes'],
                           scale=data['scale_cubes'],
                           vault=data['vault_cubes'],
                           climb=data['can_climb'],
                           type=data['type'],
                           notes=data['notes'])


@app.route('/getdata')
def getTeamData():
    team_number = request.args.get('team')
    if team_number is None or team_number == 0:
        return """ No team number was specified, therefore no team data was fetched from the database. Please try again! """
    matches = db.getData(int(team_number))
    if matches is None or matches == []:  # if there is no match data in the list 'matches'
        return """ This team has not been scouted yet! Get on that! """
    try:
        return render_template('team_data.html',
                               number=team_number,
                               auto=[match['auto'] for match in matches],
                               switch=[match['switch_cubes'] for match in matches],
                               scale=[match['scale_cubes'] for match in matches],
                               vault=[match['vault_cubes'] for match in matches],
                               climb=[match['can_climb'] for match in matches],
                               type=[match['type'] for match in matches],
                               notes=[match['notes'] for match in matches])
    except KeyError:
        return """ This team has not been scouted yet! Get on that! """


@app.route('/exportdata')
def exportDataAsCSV():
    return("""TODO""")


@app.route('/rankings')
def toRankings():
    return render_template('rankings.html',
                           name="algorithm",
                           data=db.getAlgorithmicRankings())


@app.route('/getrankings', methods=['POST'])
def getRankingData():
    config = dict(request.form)['config'][0]
    if config == "default":
        data = db.getAlgorithmicRankings()
    elif config == "switch":
        data = db.getSwitchRankings()
    elif config == "scale":
        data = db.getScaleRankings()
    elif config == "vault":
        data = db.getVaultRankings()
    else:
        data = db.getAlgorithmicRankings() # algorithmic rankings are default
    if config == "default":
        config = "algorithm"
    return render_template("rankings.html",
                           name=str(config).capitalize(),
                           data=data)

if __name__ == '__main__':
    app.run()