from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Doctor(db.Model):
    # id = db.Column(db.Integer, nullable=False)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(40),nullable=False)
    address=db.Column(db.String(50),nullable=False)
    phone=db.Column(db.String(20),primary_key=True)
    degree=db.Column(db.String(30),nullable=False)
    specialization=db.Column(db.String(40),nullable=True)
    desc=db.Column(db.String(400),nullable=True)
    dob=db.Column(db.Date,nullable=False)
    experience=db.Column(db.Integer,nullable=False)

    password=db.Column(db.String(200),nullable=False)
    photo=db.Column(db.String(40),nullable=True)
    nmc_number=db.Column(db.String(50),nullable=True)
    # rating = db.Column(db.Integer, default=0)
    # nmc_photo=db.Column(db.String(100),nullable=True)

class Patient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(55),nullable=False)
    phone=db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(400), nullable=True)
    tem_address=db.Column(db.String(200),nullable=False)
    per_address=db.Column(db.String(200),nullable=False)
    
    closed_person1=db.Column(db.String(100),nullable=True)
    closed_person2=db.Column(db.String(100),nullable=True)
    closed_person3=db.Column(db.String(100),nullable=True)
    num1=db.Column(db.String(30),nullable=True)
    num2=db.Column(db.String(30),nullable=True)
    num3=db.Column(db.String(30),nullable=True)
    relation1=db.Column(db.String(30),nullable=True)
    relation2=db.Column(db.String(30),nullable=True)
    relation3=db.Column(db.String(30),nullable=True)
    password = db.Column(db.String(200), nullable=True)


    #conform_password = db.Column(db.String(200), nullable=False)

    def __repr__(self) ->str:
        return f"{self.sno}-{self.name }"
    
    