from flask import Flask, render_template, request, session
import database as db

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/submitData', methods=['POST']) # ONLY the post responses will be filtered here and dealt with here
def submitData():
    formdata = dict(request.form)
    global num
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
    data = {
        'team_number': num,
        'auto': str(formdata['auto'][0]),
        'switch_cubes': switch,
        'scale_cubes': scale,
        'vault_cubes': vault,
        'can_climb': True if formdata['can_climb'][0] == "Yes" else False,
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
                           notes=data['notes'])


@app.route('/getData')
def getTeamData():
    team_number = request.args.get('team')
    if team_number is None or team_number == 0:
        return(""" No team number was specified, therefore no team data was fetched from the database. Please try again! """)
    data = db.getData(int(team_number))
    if data is None:
        return(""" This team has not been scouted yet! Get on that! """)
    try:
        return render_template('team_data.html',
                           number=data['team_number'],
                           auto=data['auto'],
                           switch=data['switch_cubes'],
                           scale=data['scale_cubes'],
                           vault=data['vault_cubes'],
                           climb=data['can_climb'],
                           notes=data['notes'])
    except KeyError:
        return(""" This team has not been scouted yet! Get on that! """)

if __name__ == '__main__':
    app.run(debug=True, port=5000)