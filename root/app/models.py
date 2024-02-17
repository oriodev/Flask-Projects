from app import db

class Friend(db.Model):
  __tablename__ = 'friends'
  friend_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), nullable=False, unique=False, index=True)
  
  def __repr__(self):
    return f"friend(`{self.name}`)"