from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class Client(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    companyName:str = db.Column(db.String(80), nullable=False)
    email:str = db.Column(db.String(120), nullable=False)
    ownerFirstName:str = db.Column(db.String(80), nullable=False)
    ownerLastName:str = db.Column(db.String(80), nullable=False)
    ownerPhone:str = db.Column(db.String(20))
    # add rebate codes

    def __repr__(self):
        return f'<User {self.companyName}>'
    
    
# user info
@dataclass
class User(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    firstName:str = db.Column(db.String(80), nullable=False)
    lastName:str = db.Column(db.String(80), nullable=False)
    email:str = db.Column(db.String(120), nullable=False)
    phone:str = db.Column(db.String(20))
    address:str = db.Column(db.String(120))
    city:str = db.Column(db.String(120))
    state:str = db.Column(db.String(120))
    zip:str = db.Column(db.String(120))

    def __repr__(self):
        return f'<User {self.lastName}>'

#unit availability info for each day for each unit
@dataclass
class Unit(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    client_id:int = db.Column(db.Integer, nullable=False)
    name:str = db.Column(db.String(255), nullable=False)
    pic:str = db.Column(db.String(255)) #picture of unit
    info:str = db.Column(db.String()) #tubing, dogs, capacity, hp etc.

    def __repr__(self):
        return f'<User {self.name} & {self.client_id}>'
    
# unit info
@dataclass
class Booking(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    client_id:int = db.Column(db.Integer, nullable=False)
    user_id:int = db.Column(db.Integer, nullable=False)
    contractDate:str = db.Column(db.String, nullable=False) #date of contract creation
    totalPrice:float = db.Column(db.Float, nullable=False)
    totalDeposit:float = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<User {self.user_id}>'
    
@dataclass
class BookingDate(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    date:str = db.Column(db.String(500), nullable=False)
    price:float = db.Column(db.Float, nullable=False)
    deposit:float = db.Column(db.Float, nullable=False)
    booking_id:int = db.Column(db.Integer)
    client_id:int = db.Column(db.Integer, nullable=False)
    unit_id:int = db.Column(db.Integer, nullable=False)
    
@dataclass
class PriceDate(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    unit_id:int = db.Column(db.Integer, nullable=False)
    client_id:int = db.Column(db.Integer, nullable=False)
    start_date:str = db.Column(db.String(80), nullable=False)
    price:float = db.Column(db.Float, nullable=False) #blocked marked
    deposit:float = db.Column(db.Float, nullable=False) #blocked marked

    def __repr__(self):
        return f'<User {self.start_date} & {self.unit_id}>'
    