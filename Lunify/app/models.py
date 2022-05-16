from . import db
from werkzeug.security import generate_password_hash


class UserProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

class Scan(db.Model):
    __tablename__ = 'Scans'

    id = db.Column(db.Integer, primary_key=True)
    photo=db.Column(db.String(255))
    user_id=db.Column(db.Integer)

    def __init__(self, photo, user_id ):
        self.photo= photo
        self.user_id= user_id

    def get_id(self):
        return str(self.id)  # python 3 support

class Result(db.Model):
    __tablename__ = 'Results'

    id = db.Column(db.Integer, primary_key=True)
    photo=db.Column(db.String(255))
    
    location=db.Column(db.String(255))
    patname=db.Column(db.String(255))
    empid=db.Column(db.String(255))
    identification = db.Column(db.String(80))
    confidence=db.Column(db.String(80))
    date_scanned=db.Column(db.Date)
    user_id=db.Column(db.Integer)

    def __init__(self, photo,location,patname,empid,identification,confidence,date_scanned, user_id ):
        self.photo= photo
        self.location=location
        self.patname=patname
        self.empid=empid
        self.identification=identification
        self.confidence=confidence
        self.date_scanned=date_scanned
        self.user_id= user_id

    def get_id(self):
        return str(self.id)  # python 3 support