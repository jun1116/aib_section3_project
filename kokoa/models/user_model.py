from kokoa import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # email = db.Column(db.String(64), nullable=False)
    # age = db.Column(db.Integer,unique=True, nullable=False)

    def __repr__(self):
        return f"User id : {self.id},  User name : {self.username}"
        # return f"User id : {self.id},  User name : {self.username}, E-mail : {self.email}"

class Company(db.Model):
    __tablename__='company'
    id = db.Column(db.Integer, primary_key = True)
    companyname = db.Column(db.String(64), unique=True, nullable=False)
    def __repr__(self):
        return f"Company id : {self.id},  Company name : {self.companyname}"

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    company_id = db.Column(db.Integer(), db.ForeignKey('company.id', ondelete='CASCADE'))
    
    user = db.relationship('User', backref=db.backref('rooms', cascade='all, delete-orphan'))
    company = db.relationship('Company', backref=db.backref('rooms', cascade='all, delete-orphan'))
    def __repr__(self):
        return f"Room id : {self.id},  User - Company : {self.user_id} - {self.company_id}"

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key = True)
    text= db.Column(db.String(150), nullable=False)
    room_id = db.Column(db.Integer(), db.ForeignKey('room.id', ondelete='CASCADE'))
    isuser = db.Column(db.Boolean(), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    room = db.relationship('Room', backref=db.backref('chats', cascade='all, delete-orphan'))
    def __repr__(self):
        return f"chat_id : {self.id}, text : {self.text}, room_id : {self.room_id}"

    
    
    # embedding = db.Column(db.PickleType,nullable=True)
