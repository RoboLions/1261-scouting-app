from flask import Flask, render_template, request, url_for, redirect
import database as db
from forms import RapidReactForm, FindTeamForm
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def main():
    form = RapidReactForm()
    return render_template('index.html', form=form)  # the main page


@app.route('/submitdata', methods=['POST']) # ONLY the post responses will be filtered here and dealt with here
def submitData():
    data = dict(request.form)
    team = int(data["team_number"])
    disabled = None
    try:
        throwaway_var = data["disabled"]
        disabled = True
    except KeyError:
        disabled = False
    crossed_tarmac = None
    try:
        throwaway_var2 = data["crossed_tarmac"]
        crossed_tarmac = True
    except KeyError:
        crossed_tarmac = False
    disconnected = None
    try:
        throwaway_var3 = data["disconnected"]
        disconnected = True
    except KeyError:
        disconnected = False
    # defense = None
    # try:
    #     throwaway_var3 = data["defense"]
    #     defense = True
    # except KeyError:
    #     defense = False
    data = {  # to clear things up, this data is the data of a single match
        "team_number": team,
        "match": int(data["match"]),
        "match_name": data["match_name"],
        "disabled": disabled,
        "disconnected": disconnected,
        "disconnected_total_seconds": int(data["disconnected_total_seconds"]),
        "crossed_tarmac": crossed_tarmac,
        "auto_upper": int(data["auto_upper"]),
        "auto_lower": int(data["auto_lower"]),
        "teleop_upper": int(data["teleop_upper"]),
        "teleop_lower": int(data["teleop_lower"]),
        "type": data["type"],
        "driver": int(data["driver"]),
        "defense": int(data["defense"]), #defense,
        "position": data["position"],
        "speed": data["speed"],
        # "height": data["height"],
        "accuracy": int(data["accuracy"]),
        "climb": data["climb"],
        "notes": data["notes"],
    }
    db.setData(data)
    return render_template('confirm.html',
                           number=data['team_number'],
                           match=data['match'],
                           match_name=data['match_name'],
                           disabled=data['disabled'],
                           disconnected=data['disconnected'],
                           disconnected_total_seconds=data['disconnected_total_seconds'],
                           crossed_tarmac=data['crossed_tarmac'],
                           auto_upper=data['auto_upper'],
                           auto_lower=data['auto_lower'],
                           teleop_upper=data['teleop_upper'],
                           teleop_lower=data['teleop_lower'],
                           defense=data['defense'],
                           type=data['type'],
                           position=data['position'],
                           speed=data['speed'],
                           # height=data['height'],
                           stability=data['stability'],
                           driver=data['driver'],
                           accuracy=data['accuracy'],
                           climb=data['climb'],
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
                               match_name=[match['match_name'] for match in matches],
                               disabled=[match['disabled'] for match in matches],
                               disconnected=[match['disconnected'] for match in matches],
                               disconnected_total_seconds=[match['disconnected_total_seconds'] for match in matches],
                               crossed_tarmac=[match['crossed_tarmac'] for match in matches],
                               auto_upper=[match['auto_upper'] for match in matches],
                               auto_lower=[match['auto_lower'] for match in matches],
                               teleop_upper=[match['teleop_upper'] for match in matches],
                               teleop_lower=[match['teleop_lower'] for match in matches],
                               type=[match['type'] for match in matches],
                               driver=[match['driver'] for match in matches],
                               defense=[match['defense'] for match in matches],
                               position=[match['position'] for match in matches],
                               speed=[match['speed'] for match in matches],
                               # height=[match['height'] for match in matches],
                               stability=[match['stability'] for match in matches],
                               accuracy=[match['accuracy'] for match in matches],
                               climb=[match['climb'] for match in matches],
                               notes=[match['notes'] for match in matches])
    except KeyError:
        return """ This team has not been scouted yet! Get on that! """

@app.route('/rankings')
def toRankings():
    return render_template('rankings.html',
                           name="Algorithm",
                           data=db.getAlgorithmicRankings())


@app.route('/getrankings', methods=['POST'])
def getRankingData():
    config = dict(request.form)['config']
    if config == "default":
        data = db.getAlgorithmicRankings()
        config = "algorithm"
    elif config == "auto_upper":
        data = db.getAutoUpperRankings()
    elif config == "auto_lower":
        data = db.getAutoLowerRankings()
    elif config == "teleop_upper":
        data = db.getTeleopUpperRankings()
    elif config == "teleop_lower":
        data = db.getTeleopLowerRankings()
    elif config == "driver":
        data = db.getDriverRankings()
    elif config == "reach":
        data = db.getReachRankings()
    elif config == "climb":
        data = db.getClimbRankings()
    elif config == "defense":
        data = db.getDefenseRankings()
    else:
        data = db.getAlgorithmicRankings()  # algorithmic rankings are default
    return render_template("rankings.html",
                           name=str(config).capitalize(),
                           data=data)

@app.route('/findteam', methods=["GET", "POST"])
def findTeam():
    form = FindTeamForm()
    if form.is_submitted():
        data = dict(request.form)
        return redirect(url_for("getTeamData", team=int(data["team_number"])))
    return render_template("find_team.html", form=form)

if __name__ == '__main__':
    app.run()