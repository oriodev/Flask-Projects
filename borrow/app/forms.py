from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from app.models import Person, Thing
  
class BorrowForm(FlaskForm):
  personId = IntegerField('person id', validators=[DataRequired()])
  thingId = IntegerField('thing id', validators=[DataRequired()])
  submit = SubmitField('borrow the thing!')
  
class ReturnForm(FlaskForm):
  personId = IntegerField('person id', validators=[DataRequired()])
  thingId = IntegerField('thing id', validators=[DataRequired()])
  submit = SubmitField('return the thing!')
  
class LeaveForm(FlaskForm):
  personId = IntegerField('person id', validators=[DataRequired()])
  submit = SubmitField('leave!')
  
class AdminForm(FlaskForm):
  thingName = StringField('thing name', validators=[DataRequired()])
  submit = SubmitField('add the thing!')
  
class JoinForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  submit = SubmitField('join!')
  
class LoanFilterForm(FlaskForm):
  person = SelectField('person')
  thing = SelectField('thing')
  submit = SubmitField('filter!')
  
  
  def __init__(self, *args, **kwargs):
    super(LoanFilterForm, self).__init__(*args, *kwargs)
    self.person.choices = [(None, 'no filter')] + [(person.person_id, person.username) for person in Person.query.all()]
    self.thing.choices = [(None, 'no filter')] + [(thing.thing_id, thing.name) for thing in Thing.query.all()]
  