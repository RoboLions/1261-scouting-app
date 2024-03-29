from flask import Flask, render_template, request, url_for, redirect, flash
import database as db
from forms import ChargedUpForm, FindTeamForm, PitScoutingForm
import os
from google.cloud import storage
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']


@app.route('/')
def main():
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
                           mobility = data['mobility'],  
                           cube_auto_top = data["cube_auto_top"],
                           cube_auto_middle = data["cube_auto_middle"],
                           cube_auto_hybrid = data["cube_auto_hybrid"],
                           cone_auto_top = data["cone_auto_top"], 
                           cone_auto_middle = data["cone_auto_middle"],
                           cone_auto_hybrid = data["cone_auto_hybrid"],
                           cube_teleop_top = data["cube_teleop_top"],
                           cube_teleop_middle = data["cube_teleop_middle"],
                           cube_teleop_hybrid = data["cube_teleop_hybrid"],
                           cone_teleop_top = data["cone_teleop_top"],
                           cone_teleop_middle = data["cone_teleop_middle"],
                           cone_teleop_hybrid = data["cone_teleop_hybrid"],
                           auto_charge = data["auto_charge"], 
                           teleop_charge = data['teleop_charge'],
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
        name="Cone Teleop Rankings"
    elif config == "ConeAuto_avg":
        data = db.getConeAutoRankings()
        name="Cone Auto Rankings"
    elif config == "ConeTeleop_avg":
        data = db.getConeTeleopRankings()
        name="Cone Teleop Rankings"
    elif config == "CubeAuto_avg":
        data = db.getCubeAutoRankings()
        name="Cube Auto Rankings"

    elif config == "CubeTeleop_avg":
        data = db.getCubeTeleopRankings()
        name="Cube Teleop Rankings"

    elif config == "cone_auto_top":
        data = db.getConeAutoTopRankings()
        name="Cone Auto Top Rankings"

    elif config == "cone_auto_middle":
        data = db.getConeAutoMiddleRankings()
        name="Cone Auto Middle Rankings"

    elif config == "cone_auto_hybrid":
        data = db.getConeAutoHybridRankings()
        name="Cone Auto Hybrid:"

    elif config == "cube_auto_top":
        data = db.getCubeAutoTopRankings()
        name="Cube Auto Top Rankings:"
    elif config == "cube_auto_middle":
        data = db.getCubeAutoMiddleRankings()
        name="Cube Auto Middle Rankings:"
    elif config == "cube_auto_hybrid":
        data = db.getCubeAutoHybridRankings()  
        name="Cube Auto Hybrid Rankings:"

    elif config == "cone_teleop_top":
        data = db.getConeTeleopTopRankings()
        name="Cone Teleop Top Rankings:"

    elif config == "cone_teleop_middle":
        data = db.getConeTeleopMiddleRankings()
        name="Cube Teleop Middle Rankings:"

    elif config == "cone_teleop_hybrid":
        data = db.getConeTeleopHybridRankings()
        name="Cone Teleop Hybrid Rankings:"
    elif config == "cube_teleop_top":
        data = db.getCubeTeleopTopRankings()
        name="Cube Teleop Top Rankings:"
    elif config == "cube_teleop_middle":
        data = db.getCubeTeleopMiddleRankings()
        name="Cube Teleop Middle Rankings:"

    elif config == "cube_teleop_hybrid":
        data = db.getCubeTeleopHybridRankings()
        name="Cube Teleop Hybrid Rankings:"
    
    elif config == "auto_charge": 
        data = db.getChargingPortAuto()
        name="Auto Charging Station Rankings:"

    elif config == "teleop_charge": 
        data = db.getChargingPortTeleop()
        name="Teleop Charging Station Rankings:"
    else:
        data = db.getConeTeleopRankings()  # algorithmic rankings are default
    return render_template("rankings.html",
                           name=name,
                           teams=data,
                           teams_len=len(data)
                           )

@app.route('/findteam', methods=["GET", "POST"])
def findTeam():
    form = FindTeamForm()
    if form.is_submitted():
        data = dict(request.form)
        return redirect(url_for("getTeamData", team=int(data["team_number"])))
    return render_template("find_team.html", form=form)

@app.route('/pit-scouting', methods=["GET", "POST"])
def pitScouting():
    form = PitScoutingForm()
    if request.method=="POST":
        data = dict(request.form)
        file = request.files['image']
        if file.filename.split('.')[-1] not in ['jpg','jpeg','png']:
            flash('Not a valid extension')
            return render_template("pit_scouting.html", form=form)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        storage_client = storage.Client()
        bucket = storage_client.bucket('1261-pit-scouting-images')
        blob = bucket.blob(filename)
        if blob.exists():
            flash('File already exists')
            return render_template("pit_scouting.html", form=form)
        generation_match_precondition = 0
        blob.upload_from_filename(os.path.join(app.config['UPLOAD_FOLDER'], filename), if_generation_match=generation_match_precondition)
    return render_template("pit_scouting.html", form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))