from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, BooleanField
from wtforms.validators import Optional, DataRequired, NumberRange, ValidationError
from wtforms.widgets import TextArea


 class InfiniteRechargeForm(FlaskForm):
    team_number = IntegerField("Team Number", validators=[DataRequired(), NumberRange(1,20000)])
    match = IntegerField("Match Number", validators=[DataRequired()])
    disabled = BooleanField("Disabled/AFK")
    auto = SelectField("Autonomous", choices=[
        (5, "4+ Balls in High Port"),
        (4, "1-3 Balls in High Port"),
        (3, "4+ Balls in Low Port"),
        (2, "1-3 Balls in Low Port"),
        (1, "Only Crossed Auto Line"),
        (0, "None of the Above/Stayed Motionless")
    ])
    lower = IntegerField("Lower Port", validators=[DataRequired()])
    outer = IntegerField("Outer Port", validators=[DataRequired()])
    inner = IntegerField("Inner Port", validators=[DataRequired()])
    climb = SelectField("Climb", choices=[
        (3, "Is Climbed and Balanced"),
        (2, "Climbs but doesn't balance"),
        (1, "Drives to inside Rendezvous Point"),
        (0, "Did not go to any platforms")
    ])
    type = SelectField("Robot's Reach", choices=[
        (2, "Uses shooter to shoot balls high"),
        (1, "Can dump balls low only"),
        (0, "Can't hold any game pieces")
    ])
    driver = IntegerField("Rate Driver Skill", validators=[DataRequired(), NumberRange(0,100)])
    notes = StringField("Notes", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")


class RapidReactForm(FlaskForm):
    team_number = IntegerField("Team Number", validators=[DataRequired(), NumberRange(1, 20000)])
    match = IntegerField("Match Number", validators=[DataRequired()])
    disabled = BooleanField("Disabled/AFK")
    disconnected = BooleanField("Disconnected during the match")
    disconnected_total_seconds = IntegerField("Total seconds disconnected", validators=[DataRequired()], default=0)
    # disconnected_total_seconds = IntegerField("Total seconds disconnected", validators=[Optional(strip_whitespace=True)])
    crossed_tarmac = BooleanField("Crossed Tarmac during Auto")
    auto_upper = IntegerField("Auto - Upper", validators=[DataRequired()])
    auto_lower = IntegerField("Auto - Lower", validators=[DataRequired()])
    teleop_upper = IntegerField("Teleop - Upper", validators=[DataRequired()])
    teleop_lower = IntegerField("Teleop - Lower", validators=[DataRequired()])
    defense = SelectField("Defense", choices=[
        ("no defense", "No defense"),
        ("bad defense", "Bad defense"),
        ("good defense", "Good defense")
    ])
    type = SelectField("Type of Shooter", choices=[
        ("cannot shoot", "Cannot hold game pieces"),
        ("shoots low", "Can shoot balls into lower hub only"),
        ("shoots high", "Can shoot balls into upper hub only"),
        ("shoots high and low", "Can shoot balls into either the upper or lower hub")
    ])
    position = SelectField("Shooting Position", choices=[
        ("hub", "Touching the Lower Hub"),
        ("tarmac", "Inside of the Tarmac"),
        ("outside tarmac", "Outside of the Tarmac"),
        ("anywhere","Anywhere on the Field")
    ])
    speed = SelectField("Robot's Speed", choices=[
        ("slow", "Drives Slow"),
        ("fast", "Drives Fast")
    ])
    stability = SelectField("Robot Stability", choices=[
        ("very stable", "Very Stable"),
        ("penguin walk", "Penguin Walk"),
        ("tilting", "Tilting during matches"),
        ("flipped over", "Flipped Over")
    ])
    driver = SelectField("Rate Driver Skill", choices=[
        (3, "Good"),
        (2, "Average"),
        (1, "Bad")
    ])
    accuracy = SelectField("Rate Robot Accuracy", choices=[
        (1, "Always Missed Shots"),
        (2, "Frequently Missed Shots"),
        (3, "Sometimes Missed Shots"),
        (4, "Rarely Missed Shots"),
        (5, "Never Missed Shots")
    ])
    climb = SelectField("Climb", choices=[
        ("cannot", "Cannot Climb"),
        ("did not" , "Can climb, but didn't"),
        ("attempted", "Attempted climb, but failed"),
        ("low", "Low Rung"),
        ("mid", "Mid Rung"),
        ("high", "High Rung"),
        ("traverse", "Traverse Rung")
    ])
    climb_seconds = SelectField("Climb Time", choices=[
        ("less than 10s", "Less than 10 seconds"),
        ("around 20s", "Around 20 seconds"),
        ("around 30s", "Around 30 seconds"),
        ("more than 40s", "More than 40 seconds")
    ])
    notes = StringField("Notes", validators=[DataRequired()], widget=TextArea())
    name = StringField("Name", validators=[DataRequired()])

    submit = SubmitField("Submit")
# 2023 
class ChargedUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    team_number = IntegerField("Team Number", validators=[DataRequired(), NumberRange(1, 20000)])
    match = IntegerField("Match Number", validators=[DataRequired()])
    starting_pos = SelectField("Starting Position", choices=[
        ("Left", "Left"),
        ("Middle", "Middle"),
        ("Right", "Right")
    ])
    mobility = SelectField("Mobility", choices=[
        ("Yes", "Yes, left community during auto"),
        ("No", "No, didn't leave community during auto")
    ])
    cone_auto_top = IntegerField ("Cone Auto - Top", default = 0, validators=[DataRequired()])
    cone_auto_middle = IntegerField("Cone Auto - Middle", default = 0, validators=[DataRequired()])
    cone_auto_hybrid= IntegerField("Cone Auto - Hybrid", default = 0, validators=[DataRequired()])

    cube_auto_top = IntegerField ("Cube Auto - Top", default = 0, validators=[DataRequired()])
    cube_auto_middle = IntegerField("Cube Auto - Middle", default = 0, validators=[DataRequired()])
    cube_auto_hybrid= IntegerField("Cube Auto - Hybrid", default = 0, validators=[DataRequired()])

    cone_teleop_top = IntegerField ("Cone Teleop - Top", default = 0, validators=[DataRequired()])
    cone_teleop_middle = IntegerField("Cone Teleop - Middle", default = 0, validators=[DataRequired()])
    cone_teleop_hybrid= IntegerField("Cone Teleop - Hybrid", default = 0, validators=[DataRequired()])

    cube_teleop_top = IntegerField ("Cube Teleop - Top", default = 0, validators=[DataRequired()])
    cube_teleop_middle = IntegerField("Cube Teleop - Middle", default = 0, validators=[DataRequired()])
    cube_teleop_hybrid= IntegerField("Cube Teleop - Hybrid", default = 0, validators=[DataRequired()])
    defense = IntegerField("Defense Percentage", validators=[DataRequired(), NumberRange(0,100)])
    # 0% means that the team did not play any defense. please dont forgor to add that in the question.
    auto_charge = SelectField("Charging Station State Auto", choices=[
        ("N/A", "No Dock nor Engage"),
        ("docked auto", "Docked Points Earned"),
        ("engaged auto", "Engaged Points Earned")
    ]) 
    teleop_charge = SelectField("Charging Station State TeleOp", choices=[
        ("N/A", "No Dock nor Engage"),
        ("1docked teleop", "1 Docked Points Earned"),
        ("2docked teleop", "2 Docked Points Earned"),
        ("3docked teleop", "3 Docked Points Earned"),
        ("1engaged teleop", "1Engaged Points Earned"),
        ("2engaged teleop", "2Engaged Points Earned"),
        ("3engaged teleop", "3Engaged Points Earned"),
    ])
    speed = IntegerField ("speed", default = 0, validators=[DataRequired(), NumberRange (1, 10)]) 
    disabled = BooleanField("Disabled/AFK")
    disconnected = BooleanField("Disconnected")
    disconnected_total_seconds = StringField("Total Seconds Disconnected")
    notes = StringField("Notes", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")

class FindTeamForm(FlaskForm):
    team_number = IntegerField("Team Number", validators=[DataRequired(), NumberRange(1, 20000)])
    submit = SubmitField("Submit")
