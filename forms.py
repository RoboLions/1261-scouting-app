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

class FindTeamForm(FlaskForm):
  team_number = IntegerField("Team Number", validators=[DataRequired(), NumberRange(1, 20000)])
  submit = SubmitField("Submit")