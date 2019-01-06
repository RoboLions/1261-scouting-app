import csv
import database as db
from tba_scraper import competition_data

def writeCSV():
    with open('data.csv', mode='w') as data_file:
        writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['team_number', 'auto', 'cargo', 'hatches', 'habitat', 'robot_type', 'rank', 'total_score', 'average_score'])

        for teamdata in db.getAllTeamData():
            team_number = teamdata['team_number']
            auto = db.getMostCommonAuto(team_number)
            cargo = teamdata['cargo_avg']
            hatches = teamdata['hatch_avg']
            habitat = db.getMostCommonHabitat(team_number)
            robot_type = teamdata['matches'][0]['type']
            rank = competition_data.getRanking(team_number)
            total_score = competition_data.getTotalScore(team_number)
            avg_score = competition_data.getAverageScore(team_number)

            writer.writerow([team_number, auto, cargo, hatches, habitat, robot_type, rank, total_score, avg_score])
        data_file.close()