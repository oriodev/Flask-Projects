from app import db
from sqlalchemy.sql import func
  
class Thing(db.Model):
  __tablename__ = 'things'
  thing_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), nullable=False, unique=True, index=True)
  
  def __repr__(self):
    return f"thing(`{self.name}`)"
  

class Person(db.Model):
  __tablename__ = 'people'
  person_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), nullable=False, unique=True)
  
  def __repr__(self):
    return f"person(`{self.username}`)"
  
class Loan(db.Model):
  __tablename__ = 'loans'
  loan_id = db.Column(db.Integer, primary_key=True)
  thing_id = db.Column(db.ForeignKey('things.thing_id'), nullable=False)
  person_id = db.Column(db.ForeignKey('people.person_id'), nullable=False)
  borrowdatetime = db.Column(db.DateTime, nullable=False)
  returndatetime = db.Column(db.DateTime, nullable=True)
  
  def __repr__(self):
    return f"loan(`{self.thing_id}, {self.person_id}`)"
