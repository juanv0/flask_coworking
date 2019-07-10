from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, index=True)
    fecha = db.Column(db.Date)
    hora = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    telefono = db.Column(db.Integer)
    name = db.Column(db.String(300))
    password_hash = db.Column(db.String(128))
    salas = db.relationship('Sala', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def salas_reservadas(self, el_id):
        return Sala.query.filter_by(user_id=el_id)


@login.user_loader
def user_loader(id):
    return User.query.get(int(id))
