from flask import redirect, abort, render_template
from app import app, db
from app.models import Thing, Person, Loan
from app.forms import BorrowForm, ReturnForm, LeaveForm, AdminForm, JoinForm, LoanFilterForm
from datetime import datetime

#
# INDEX
#
@app.route('/')
def index():
  
  things = [[thing.name, thing.thing_id] for thing in Thing.query.all()]
  people = [[person.username, person.person_id] for person in Person.query.all()]
  
  return render_template('index.html', things=things, people=people)

#
# ADMIN
#
@app.route('/admin', methods=['GET', 'POST'])
def admin():
  form = AdminForm()
  
  if form.validate_on_submit():
    new_thing = Thing(name=form.thingName.data)
    db.session.add(new_thing)
        
    try:
      db.session.commit()
      return redirect('/')
    except:
      db.session.rollback()
  
  return render_template('admin.html', form=form)

#
# JOIN
#
@app.route('/join', methods=['GET', 'POST'])
def join():
  form = JoinForm()
  
  if form.validate_on_submit():
    new_person = Person(username=form.username.data)
    db.session.add(new_person)
    
    try:
      db.session.commit()
      return redirect('/')
    except:
      return redirect('/join')
  
  return render_template('join.html', form=form)

#
# BORROW
#
@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
  form = BorrowForm()
  
  if form.validate_on_submit():
    
    studentLoanStatus = (Loan.query.filter(
      Loan.person_id == form.personId.data,
      Loan.returndatetime.is_(None)
    )).first() == None
    
    thingLoanStatus = (Loan.query.filter(
      Loan.thing_id == form.thingId.data,
      Loan.returndatetime.is_(None)
    )).first() == None
        
    if (studentLoanStatus and thingLoanStatus):
      
      new_loan = Loan(thing_id=form.thingId.data, person_id=form.personId.data, borrowdatetime=datetime.now())
      db.session.add(new_loan)
      
      try:
        db.session.commit()
        return redirect('/loans')
      except:
        db.session.rollback()
    else:
      print('nope:', studentLoanStatus, thingLoanStatus)
      return redirect('/borrow')
    
  return render_template('borrow.html', form=form)

#
# LOANS
#
@app.route('/loans', defaults={'person_id': None, 'thing_id': None}, methods=['GET', 'POST'])
@app.route('/loans/person/<int:person_id>', methods=['GET', 'POST'])
@app.route('/loans/thing/<int:thing_id>', methods=['GET', 'POST'])
def loans(person_id=None, thing_id=None):
  
  form = LoanFilterForm()
  
  if form.validate_on_submit():
    person = form.person.data
    thing = form.thing.data
    
    if (person != 'None'):
      return redirect('/loans/person/' + person)
    elif (thing != 'None'):
      return redirect('/loans/thing/' + thing)
    else:  
      return redirect('/loans')
  
  print('hi?')
  
  if (person_id is not None):
    loans = [[loan.person_id, loan.thing_id, loan.returndatetime] for loan in Loan.query.filter_by(person_id=person_id).all()]
  elif (thing_id is not None):
    loans = [[loan.person_id, loan.thing_id, loan.returndatetime] for loan in Loan.query.filter_by(thing_id=thing_id).all()]
  else:
    loans = [[loan.person_id, loan.thing_id, loan.returndatetime] for loan in Loan.query.order_by(Loan.person_id).all()]
  
  loans_with_names = []
  
  for loan in loans:
    new_loan = []
    new_loan.append(Person.query.filter_by(person_id=loan[0]).first().username)
    new_loan.append(Thing.query.filter_by(thing_id=loan[1]).first().name)
    new_loan.append(loan[2])
    loans_with_names.append(new_loan)
  
  return render_template('loans.html', loans=loans_with_names, form=form)

#
# RETURN
#
@app.route('/return', methods=['GET', 'POST'])
def returnThing():
  form = ReturnForm()
  
  if form.validate_on_submit():
    # find the entry
    # it'll be the one with personId and thingId and null
    # and then update returndatetime
    # and go to loans
    
    loan_to_return = (Loan.query.filter(
      Loan.person_id == form.personId.data,
      Loan.thing_id == form.thingId.data,
      Loan.returndatetime.is_(None)
    )).first()
    
    if (loan_to_return):
      loan_to_return.returndatetime = datetime.now()
      
      try:
        db.session.commit()
        return redirect('/loans')
      except:
        db.session.rollback()
        return redirect('/return') 
  
  return render_template('return.html', form=form)

#
# LEAVE
#
@app.route('/leave', methods=['GET', 'POST'])
def leave():
  form = LeaveForm()
  
  if form.validate_on_submit():
    entries = Loan.query.filter_by(person_id=form.personId.data).all()
    person = Person.query.filter_by(person_id=form.personId.data).first()
    
    db.session.delete(person)
    
    if (entries):
      for entry in entries:
        db.session.delete(entry)
      
      try:
        db.session.commit()
        print('hi?')
        return redirect('/loans')
      except:
        return redirect('/leave')
    else:
        return redirect('/leave')
  
  return render_template('leave.html', form=form)