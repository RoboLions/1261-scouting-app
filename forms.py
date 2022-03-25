from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange, ValidationError
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
    crossed_tarmac = BooleanField("Crossed Tarmac during Auto")
    auto_upper = IntegerField("Auto - Upper", validators=[DataRequired()])
    auto_lower = IntegerField("Auto - Lower", validators=[DataRequired()])
    teleop_upper = IntegerField("Teleop - Upper", validators=[DataRequired()])
    teleop_lower = IntegerField("Teleop - Lower", validators=[DataRequired()])
    climb = SelectField("Climb", choices=[
        ("cannot", "Did not Climb"),
        ("low", "Low Rung"),
        ("mid", "Mid Rung"),
        ("high", "High Rung"),
        ("traverse", "Traverse Rung")
    ])
    type = SelectField("Robot's Reach", choices=[
        ("cannot shoot", "Cannot hold game pieces"),
        ("shoots low", "Can shoot balls into lower hub only"),
        ("shoots high", "Can shoot balls into upper hub only"),
        ("shoots high and low", "Can shoot balls into either the upper or lower hub"),
        ("shoots high from launchpad", "Can shoot balls into upper hub from launch pad")
    ])
    driver = SelectField("Rate Driver Skill", choices=[
        (5, "Very Good"),
        (4, "Good"),
        (3, "Average"),
        (2, "Bad"),
        (1, "Very Bad")
    ])
    defense = BooleanField("Played Defense")
    notes = StringField("Notes", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")


class FindTeamForm(FlaskForm):
    team_number = IntegerField("Team Number", validators=[DataRequired(), NumberRange(1, 20000)])
    submit = SubmitField("Submit")
