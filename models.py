from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    companyName:str = db.Column(db.String(80), unique=True, nullable=False)
    email:str = db.Column(db.String(120), unique=True, nullable=False)
    ownerFirstName:str = db.Column(db.String(80), nullable=False)
    ownerLastName:str = db.Column(db.String(80), nullable=False)
    ownerPhone:str = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<User {self.companyName}>'
    
# # user info
# class User(db.Model):
#     id:int = db.Column(db.Integer, primary_key=True)
#     firstName:str = db.Column(db.String(80), nullable=False)
#     lastName:str = db.Column(db.String(80), nullable=False)
#     email:str = db.Column(db.String(120), unique=True, nullable=False)
#     phone:str = db.Column(db.String(20), nullable=True)

#     def __repr__(self):
#         return f'<User {self.lastName}>'

# rental contract info
class Contract(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    clientID:int = db.Column(db.Integer, nullable=False)
    firstName:str = db.Column(db.String(80), nullable=True)
    lastName:str = db.Column(db.String(80), nullable=False)
    email:str = db.Column(db.String(120), nullable=False)
    rentDates:str = db.Column(db.String(500), nullable=False)
    # unitID = db.Column(db.Integer, nullable=False)
    # totalPrice = db.Column(db.Float, nullable=False)
    # contractDate = db.Column(db.Date, nullable=False)
    # startDate = db.Column(db.Date, nullable=False)
    # endDate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<User {self.lastName}>'

class Availability(db.Model):
    clientID:int = db.Column(db.Integer, nullable=False)
    unitId:int = db.Column(db.Integer, nullable=False)
    date:str = db.Column(db.String(20), nullable=False)
    available:str = db.Column(db.String(20), nullable=False) # blocked, booked, open
    price:int = db.Column(db.Integer, nullable=False)
    contractId:str = db.Column(db.String(80))
    restrictions:str = db.Column(db.String(200))


    def __repr__(self):
        return f'<User {self.lastName}>'