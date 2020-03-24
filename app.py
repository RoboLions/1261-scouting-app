from flask import Flask, render_template, request
import database as db

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')  # the main page


@app.route('/submitdata', methods=['POST']) # ONLY the post responses will be filtered here and dealt with here
def submitData():
    formdata = dict(request.form)
    global match
    try:
        match = int(formdata['match'][0])
    except:
        match = 0
    global num  # this process must be done with each integer that is collected
    try:
        num = int(formdata['team_number'][0])
    except:
        num = 0
    global lower
    try:
        lower = int(formdata['lower'][0])
    except:
        lower = 0
    global outer
    try:
        outer = int(formdata['outer'][0])
    except:
        outer = 0
    global inner
    try:
        inner = int(formdata['inner'][0])
    except:
        inner = 0
    global driver
    try:
        driver = int(formdata['driver'][0])
    except:
        driver = 0
    global disabled
    try:
        throwaway_var = formdata['disabled']
        disabled = True
    except:
        disabled = False
    scout_name = str(formdata['scout_name'][0])

    data = {  # to clear things up, this data is the data of a single match
        'team_number': num,
        'match': match,
        'disabled': disabled,
        'auto': str(formdata['auto'][0]),
        'lower': lower,
        'outer': outer,
        'inner': inner,
        'climb': str(formdata['climb'][0]),
        'type': str(formdata['type'][0]),
        'driver': driver,
        'notes': str(formdata['notes'][0]),
        'scout_name': scout_name
    }
    db.setData(data)
    return render_template('confirm.html',
                           number=data['team_number'],
                           match=data['match'],
                           disabled=data['disabled'],
                           auto=data['auto'],
                           lower=data['lower'],
                           outer=data['outer'],
                           inner=data['inner'],
                           climb=data['climb'],
                           type=data['type'],
                           driver=data['driver'],
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
                               match=[match['match'] for match in matches],
                               disabled=[match['disabled'] for match in matches],
                               auto=[match['auto'] for match in matches],
                               lower=[match['lower'] for match in matches],
                               outer=[match['outer'] for match in matches],
                               inner=[match['inner'] for match in matches],
                               climb=[match['climb'] for match in matches],
                               type=[match['type'] for match in matches],
                               driver=[match['driver'] for match in matches],
                               notes=[match['notes'] for match in matches])
    except KeyError:
        return """ This team has not been scouted yet! Get on that! """


@app.route('/exportdata', methods=["POST"])
def exportDataAsCSV():
    return ''' Ah yes '''


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
        config = "algorithm"
    elif config == "low":
        data = db.getLowRankings()
    elif config == "high":
        data = db.getHighRankings()
    elif config == "driver":
        data = db.getDriverRankings()
    elif config == "auto":
        data = db.getAutoRankings()
    elif config == "reach":
        data = db.getReachRankings()
    elif config == "climb":
        data = db.getClimbRankings()
    else:
        data = db.getAlgorithmicRankings()  # algorithmic rankings are default
    return render_template("rankings.html",
                           name=str(config).capitalize(),
                           data=data)


@app.route('/match', methods=['POST'])
def getMatchData():
    allData = db.getAllTeamData()
    '''
    if matches is None or matches == []:  # if there is no match data in the list 'matches'
        return """ This team has not been scouted yet! Get on that! """
    try:
        return render_template('match.html',
                               number=team_number,
                               match=[match['match'] for match in matches],
                               disabled=[match['disabled'] for match in matches],
                               auto=[match['auto'] for match in matches],
                               cargo=[match['cargo'] for match in matches],
                               hatches=[match['hatches'] for match in matches],
                               habitat=[match['habitat'] for match in matches],
                               type=[match['type'] for match in matches],
                               driver=[match['driver'] for match in matches],
                               notes=[match['notes'] for match in matches])
    except KeyError:
        return """ This team has not been scouted yet! Get on that! """
    '''

if __name__ == '__main__':
    app.run()