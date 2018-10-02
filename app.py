from flask import Flask, render_template, request, session
import database as db

app = Flask(__name__)

@app.route('/')
def main():
    data = db.getData()
    team_number = request.args.get('team')
    return render_template('index.html',
                           number=team_number,
                           #balls=data['balls_thrown'],
                           climb=data['can_climb'],
                           color=data['team_color'],
                           notes=data['notes'])

@app.route('/submitData', methods=['POST']) # ONLY the post responses will be filtered here and dealt with here
def getSubmittedData():
    data = dict(request.form)
    #db.printDataInBrowser(data)
    return render_template('confirm.html',
                           number=data['team_number'],
                           #balls=data['balls_thrown'],
                           climb=data['can_climb'],
                           color=data['team_color'],
                           notes=data['notes'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
