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
    if ("disabled" not in data):
        data["disabled"] = "n"
    if ("disconnected" not in data):
        data["disconnected"] = "n"
    team = int(data["team_number"])
    data = {  # to clear things up, this data is the data of a single match
        "team_number": team,
        "match": int(data["match"]),
        "starting_pos": data["starting_pos"],
        "mobility": data["mobility"],
        "speed": data['speed'],
        "disabled": data["disabled"],
        "disconnected": data["disconnected"],
        "disconnected_total_seconds": data["disconnected_total_seconds"],
        "auto_charge": data['auto_charge'],
        "teleop_charge": data['teleop_charge'],
        "name": data["name"],
        "cone_auto_top": int(data["cone_auto_top"]),
        "cone_auto_middle": int(data["cone_auto_middle"]),
        "cone_auto_hybrid": int(data["cone_auto_hybrid"]),
        "cone_teleop_top": int(data["cone_teleop_top"]),
        "cone_teleop_middle": int(data["cone_teleop_middle"]),
        "cone_teleop_hybrid": int(data["cone_teleop_hybrid"]),
        "cube_auto_top": int(data["cube_auto_top"]),
        "cube_auto_middle": int(data["cube_auto_middle"]),
        "cube_auto_hybrid": int(data["cube_auto_hybrid"]),
        "cube_teleop_top": int(data["cube_teleop_top"]),
        "cube_teleop_middle": int(data["cube_teleop_middle"]),
        "cube_teleop_hybrid": int(data["cube_teleop_hybrid"]),
        "notes": data["notes"],
        
    }
    db.setData(data)
    return render_template('confirm.html',
                           name = data['name'],
                           team_number=data['team_number'],
                           match=data['match'],
                           disabled= data['disabled'],
                           disconnected= data['disconnected'],
                           disconnected_total_seconds= data['disconnected_total_seconds'],
                           starting_pos= data['starting_pos'],
                           mobility = data["mobility"],  
                           cube_auto_top = data["cube_auto_top"],
                           cube_auto_middle = data["cube_auto_middle"],
                           cube_auto_hybrid = data["cube_auto_hybrid"],
                           cube_teleop_top = data["cube_teleop_top"],
                           cube_teleop_middle = data["cube_teleop_middle"],
                           cube_teleop_hybrid = data["cube_teleop_hybrid"],
                           cone_auto_top = data["cone_auto_top"], 
                           cone_auto_middle = data["cone_auto_middle"],
                           cone_auto_hybrid = data["cone_auto_hybrid"],
                           cone_teleop_top = data["cone_teleop_top"],
                           cone_teleop_middle = data["cone_teleop_middle"],
                           cone_teleop_hybrid = data["cone_teleop_hybrid"],
                           auto_charge = data["auto_charge"], 
                           teleop_charge = data['teleop_charge'],
                           speed = data['speed'],
                           notes = data['notes'])
                           


@app.route('/getdata')
def getTeamData():
    team_number = request.args.get('team')
    if team_number is None or team_number == 0:
        return """ No team number was specified, therefore no team data was fetched from the database. Please try again! """
    matches = db.getData(int(team_number))
    if matches is None or matches == []:  # if there is no match data in the list 'matches'
        return """ This team has not been scouted yet! Get on that! """
    auto_cone_top_tmp = []
    auto_cone_middle_tmp = []
    auto_cone_hybrid_tmp = []
    auto_cube_top_tmp = []
    auto_cube_middle_tmp = []
    auto_cube_hybrid_tmp = []
    teleop_cone_top_tmp = []
    teleop_cone_middle_tmp = []
    teleop_cone_hybrid_tmp = []
    teleop_cube_top_tmp = []
    teleop_cube_middle_tmp = []
    teleop_cube_hybrid_tmp = []
    for match in matches:
        auto_cone_top_tmp.append(match["cone_auto_top"])
        auto_cone_middle_tmp.append(match["cone_auto_middle"])
        auto_cone_hybrid_tmp.append(match["cone_auto_hybrid"])
        auto_cube_top_tmp.append(match["cube_auto_top"])
        auto_cube_middle_tmp.append(match["cube_auto_middle"])
        auto_cube_hybrid_tmp.append(match["cube_auto_hybrid"])
        teleop_cone_top_tmp.append(match["cone_teleop_top"])
        teleop_cone_middle_tmp.append(match["cone_teleop_middle"])
        teleop_cone_hybrid_tmp.append(match["cone_teleop_hybrid"])
        teleop_cube_top_tmp.append(match["cube_teleop_top"])
        teleop_cube_middle_tmp.append(match["cube_teleop_middle"])
        teleop_cube_hybrid_tmp.append(match["cube_teleop_hybrid"])
    avg_auto_cone_top = sum(auto_cone_top_tmp)/len(auto_cone_top_tmp)
    avg_auto_cone_top = round(avg_auto_cone_top, 3)
    avg_auto_cone_middle = sum(auto_cone_middle_tmp)/len(auto_cone_middle_tmp)
    avg_auto_cone_middle = round(avg_auto_cone_middle, 3)
    avg_auto_cone_hybrid = sum(auto_cone_hybrid_tmp)/len(auto_cone_hybrid_tmp)
    avg_auto_cone_hybrid = round(avg_auto_cone_hybrid, 3)
    avg_auto_cube_top = sum(auto_cube_top_tmp)/len(auto_cube_top_tmp)
    avg_auto_cube_top = round(avg_auto_cube_top, 3)
    avg_auto_cube_middle = sum(auto_cube_middle_tmp)/len(auto_cube_middle_tmp)
    avg_auto_cube_middle = round(avg_auto_cube_middle, 3)
    avg_auto_cube_hybrid = sum(auto_cube_hybrid_tmp)/len(auto_cube_hybrid_tmp)
    avg_auto_cube_hybrid = round(avg_auto_cube_hybrid, 3)
    avg_teleop_cone_top = sum(teleop_cone_top_tmp)/len(teleop_cone_top_tmp)
    avg_teleop_cone_top = round(avg_teleop_cone_top, 3)
    avg_teleop_cone_middle = sum(teleop_cone_middle_tmp)/len(teleop_cone_middle_tmp)
    avg_teleop_cone_middle = round(avg_teleop_cone_middle, 3)
    avg_teleop_cone_hybrid = sum(teleop_cone_hybrid_tmp)/len(teleop_cone_hybrid_tmp)
    avg_teleop_cone_hybrid = round(avg_teleop_cone_hybrid, 3)
    avg_teleop_cube_top = sum(teleop_cube_top_tmp)/len(teleop_cube_top_tmp)
    avg_teleop_cube_top = round(avg_teleop_cube_top, 3)
    avg_teleop_cube_middle = sum(teleop_cube_middle_tmp)/len(teleop_cube_middle_tmp)
    avg_teleop_cube_middle = round(avg_teleop_cube_middle, 3)
    avg_teleop_cube_hybrid = sum(teleop_cube_hybrid_tmp)/len(teleop_cube_hybrid_tmp)
    avg_teleop_cube_hybrid = round(avg_teleop_cube_hybrid, 3)
    

    try:
        return render_template('team_data.html',
                               number=team_number,
                               matches=matches,
                               matches_len=len(matches),
                               avg_auto_cone_top=avg_auto_cone_top,
                               avg_auto_cone_middle=avg_auto_cone_middle,
                               avg_auto_cone_hybrid=avg_auto_cone_hybrid,
                               avg_auto_cube_top=avg_auto_cube_top,
                               avg_auto_cube_middle=avg_auto_cube_middle,
                               avg_auto_cube_hybrid=avg_auto_cube_hybrid,
                               avg_teleop_cone_top=avg_teleop_cone_top,
                               avg_teleop_cone_middle=avg_teleop_cone_middle,
                               avg_teleop_cone_hybrid=avg_teleop_cone_hybrid,
                               avg_teleop_cube_top=avg_teleop_cube_top,
                               avg_teleop_cube_middle=avg_teleop_cube_middle,
                               avg_teleop_cube_hybrid=avg_teleop_cube_hybrid,
                               )
    

    except KeyError:
        return """ This team has not been scouted yet! Get on that! """

@app.route('/rankings')
def toRankings():
    teams = db.getConeTeleopRankings()
    return render_template('rankings.html',
                           name="Average Teleop Cone",
                           teams_len=len(teams),
                           teams=teams)


@app.route('/getrankings', methods=['POST'])
def getRankingData():
    config = dict(request.form)['config']
    if config == "default":
        data = db.getConeTeleopRankings()
        config = "ConeTeleop_avg"
    elif config == "ConeAuto_avg":
        data = db.getConeAutoRankings()
    elif config == "ConeTeleop_avg":
        data = db.getConeTeleopRankings()
    elif config == "CubeAuto_avg":
        data = db.getCubeAutoRankings()
    elif config == "CubeTeleop_avg":
        data = db.getCubeTeleopRankings()
    elif config == "cone_auto_top":
        data = db.getConeAutoTopRankings()
    elif config == "cone_auto_middle":
        data = db.getConeAutoMiddleRankings()
    elif config == "cone_auto_hybrid":
        data = db.getConeAutoHybridRankings()
    elif config == "cube_auto_top":
        data = db.getCubeAutoTopRankings()
    elif config == "cube_auto_middle":
        data = db.getCubeAutoMiddleRankings()
    elif config == "cube_auto_hybrid":
        data = db.getCubeAutoHybridRankings()  
    elif config == "cone_teleop_top":
        data = db.getConeTeleopTopRankings()
    elif config == "cone_teleop_middle":
        data = db.getConeTeleopMiddleRankings()
    elif config == "cone_teleop_hybrid":
        data = db.getConeTeleopHybridRankings()
    elif config == "cube_teleop_top":
        data = db.getCubeTeleopTopRankings()
    elif config == "cube_teleop_middle":
        data = db.getCubeTeleopMiddleRankings()
    elif config == "cube_teleop_hybrid":
        data = db.getCubeTeleopHybridRankings()
    #elif config == "defense":
    #    data = db.getDefenseRankings()
    else:
        data = db.getConeTeleopRankings()  # algorithmic rankings are default
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