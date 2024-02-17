from flask import redirect, abort, render_template
from app import app, db
from app.forms import FriendForm
from app.models import Friend


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/friends')
def friends():
  
  friendnames = [friend.name for friend in Friend.query.all()]
  
  return render_template('friends.html', friendnames=friendnames)

# @app.route('/friends/<name>')
# def friends(name):
#   return render_template('friends.html',friendname=name)

@app.route('/makeafriend', methods=['GET', 'POST'])
def makeafriend():
  form = FriendForm()
  
  if form.validate_on_submit():
    new_friend = Friend(name=form.name.data)
    db.session.add(new_friend)
    
    try:
      db.session.commit()
      return redirect(url_for('index'))
    except:
      db.session.rollback()
  
  return render_template('makeafriend.html', form=form)