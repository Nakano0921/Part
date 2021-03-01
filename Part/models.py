from Part import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, index=True)
    username = db.Column(db.String(30), index=True)
    password = db.Column(db.String(30))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def add_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

@login_manager.user_loader
def load_restaurantuser(user_id):
    return RestaurantUser.query.get(user_id)

class RestaurantUser(UserMixin, db.Model):

    __tablename__ = 'restaurantuser'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, index=True)
    representative = db.Column(db.String(30), index=True)
    password = db.Column(db.String(30))

    def __init__(self, email, representative, password):
        self.email = email
        self.representative = representative
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def add_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()