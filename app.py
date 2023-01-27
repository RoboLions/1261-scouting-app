from flask import Flask, render_template, request, url_for, redirect
import database as db
from forms import ChargedUpForm, FindTeamForm
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def main():
 #   form = RapidReactForm()
    form = ChargedUpForm()
    return render_template('index.html', form=form)  # the main page


@app.route('/submitdata', methods=['POST']) # ONLY the post responses will be filtered here and dealt with here
def submitData():
    data = dict(request.form)
    team = int(data["team_number"])
    data = {  # to clear things up, this data is the data of a single match
        "team_number": team,
        "match": int(data["match"]),
        "defense": data["defense"],
        "auto_charge": data['auto_charge'],
        "teleop_charge": data['teleop_charge'],
        "name": data["name"],
        "cone_auto_top": int(data["cone_auto_top"])
        "cone_auto_middle": int(data["cone_auto_middle"])
        "cone_auto_hybrid": int(data["cone_auto_hybrid"])
        "cone_teleop_upper": int(data["cone_teleop_upper"])
        "cone_teleop_upper": int(data["cone_teleop_upper"])
        "cone_teleop_hybrid": int(data["cone_teleop_hybrid"])
        "cube_auto_top": int(data["cube_auto_top"])
        "cube_auto_middle": int(data["cube_auto_middle"])
        "cube_auto_hybrid": int(data["cube_auto_hybrid"])
        "cube_teleop_upper": int(data["cube_teleop_upper"])
        "cube_teleop_upper": int(data["cube_teleop_upper"])
        "cube_teleop_hybrid": int(data["cube_teleop_hybrid"])
        
    }
    db.setData(data)
    return render_template('confirm.html',
                           number=data['team_number'],
                           match=data['match'],
                           disabled=data['disabled'],
                           disconnected=data['disconnected'],
                           disconnected_total_seconds=data['disconnected_total_seconds'],
                           auto_charge = data ['auto_charge'],
                           teleop_charge = data ['teleop_charge'],
                           defense=data['defense'],
                           type=data['type'],
                           speed=data['speed'],
                           stability=data['stability'],
                           driver=data['driver'],
                           name=data['name'],
                           notes=data['notes'])
                           


@app.route('/getdata')
def getTeamData():
    team_number = request.args.get('team')
    if team_number is None or team_number == 0:
        return """ No team number was specified, therefore no team data was fetched from the database. Please try again! """
    matches = db.getData(int(team_number))
    if matches is None or matches == []:  # if there is no match data in the list 'matches'
        return """ This team has not been scouted yet! Get on that! """
    auto_upper_tmp = []
    auto_lower_tmp = []
    teleop_upper_tmp = []
    teleop_lower_tmp = []
    for match in matches:
        auto_upper_tmp.append(match["auto_upper"])
        auto_lower_tmp.append(match["auto_lower"])
        teleop_upper_tmp.append(match["teleop_upper"])
        teleop_lower_tmp.append(match["teleop_lower"])
    avg_auto_upper = sum(auto_upper_tmp)/len(auto_upper_tmp)
    avg_auto_upper = round(avg_auto_upper, 3)
    avg_auto_lower = sum(auto_lower_tmp)/len(auto_lower_tmp)
    avg_auto_lower = round(avg_auto_lower, 3)
    avg_teleop_upper = sum(teleop_upper_tmp)/len(teleop_upper_tmp)
    avg_teleop_upper = round(avg_teleop_upper, 3)
    avg_teleop_lower = sum(teleop_lower_tmp)/len(teleop_lower_tmp)
    avg_teleop_lower= round(avg_teleop_lower, 3)

    try:
        return render_template('team_data.html',
                               number=team_number,
                               matches=matches,
                               matches_len=len(matches),
                               avg_auto_upper=avg_auto_upper,
                               avg_auto_lower=avg_auto_lower,
                               avg_teleop_upper=avg_teleop_upper,
                               avg_teleop_lower=avg_teleop_lower
                               )
    

    except KeyError:
        return """ This team has not been scouted yet! Get on that! """

@app.route('/rankings')
def toRankings():
    teams = db.getAlgorithmicRankings()
    return render_template('rankings.html',
                           name="Algorithm",
                           teams_len=len(teams),
                           teams=db.getAlgorithmicRankings())


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
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))