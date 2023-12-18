from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# HeroPower association table
hero_power_association = db.Table(
    'hero_power_association',
    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id')),
    db.Column('power_id', db.Integer, db.ForeignKey('power.id')),
    db.Column('strength', db.String(50), nullable=False),
)

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)
    powers = db.relationship('Power', secondary=hero_power_association, backref='heroes', lazy='dynamic')

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
