from flask import Flask, render_template, request, url_for, redirect
import database as db
from forms import InfiniteRechargeForm, FindTeamForm
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def main():
    form = InfiniteRechargeForm()
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

    data = {  # to clear things up, this data is the data of a single match
        "team_number": team,
        "match": int(data["match"]),
        "disabled": disabled,
        "auto": int(data["auto"]),
        "lower": int(data["lower"]),
        "outer": int(data["outer"]),
        "inner": int(data["inner"]),
        "climb": int(data["climb"]),
        "type": int(data["type"]),
        "driver": int(data["driver"]),
        "notes": data["notes"],
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

@app.route('/rankings')
def toRankings():
    return render_template('rankings.html',
                           name="algorithm",
                           data=db.getAlgorithmicRankings())


@app.route('/getrankings', methods=['POST'])
def getRankingData():
    config = dict(request.form)['config']
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

@app.route('/findteam', methods=["GET", "POST"])
def findTeam():
    form = FindTeamForm()
    if form.is_submitted():
        data = dict(request.form)
        return redirect(url_for("getTeamData", team=int(data["team_number"])))
    return render_template("find_team.html", form=form)

if __name__ == '__main__':
    app.run()