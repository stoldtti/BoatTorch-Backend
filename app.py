import os
import json
import uuid
from datetime import date, timedelta, datetime
from square.client import Client as SquareClient
from models import db, Client, User, Unit, Booking, BookingDate, PriceDate
from sqlalchemy import desc
from flask import Flask, request, jsonify, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, origins=["http://localhost:3000"], methods=["GET", "POST", "PUT", "DELETE"])
api = Api(app)
db.init_app(app)


def queryHelper(table, filters: dict):
    """Query table with given filters

        Parameters:
        table (class): table to be queried,
        filters (dict): dictionary of filters

        Returns:
        json: json table of queryied results

    """
    try: 
        query = table.query

        for key in filters.keys():
            if not hasattr(table, key):
                raise Exception(f"column <{key}> does not exist in table")
            if filters[key]:
                query = query.filter( getattr(table, key) == filters[key])
        
        clients = query.all()
        print(clients)

        return clients
    
    except Exception as e:
        return {"message": f"error: {str(e)}"}
    

def deleteTableRow(table, id: int):
    try:
        oldClient = table.query.get(id)
        if oldClient:
            db.session.delete(oldClient)
            db.session.commit()

            return {
                "message": f"entry <{id}> removed",
                "removed": oldClient
            }
        
        else:
            raise Exception(f"table entry <{id}> does not exist")
    except Exception as e:
        return {"message": f"error: {str(e)}"}
    

def stringToDate(date_str: str):
    date_format = "%Y-%m-%dT%H:%M"
    return datetime.strptime(date_str, date_format)

def dateToString(date_obj: datetime):
    date_format = "%Y-%m-%dT%H:%M"
    return date_obj.strftime(date_format)


class Clients(Resource):
    
    def get(self):
        filters = request.args.to_dict()
        return jsonify(queryHelper(Client, filters))
        

    def put(self):
        client_id = request.args.get('client_id')
        data = request.get_json()  # Retrieve JSON data from the request body

        # Extract relevant fields from the JSON data
        companyName = data.get('companyName')
        email = data.get('email')
        firstName = data.get('ownerFirstName')
        lastName = data.get('ownerLastName')
        phone = data.get('ownerPhone')

        if client_id:
            oldClient = Client.query.get(client_id)
            if oldClient:
                oldClient.companyName = companyName
                oldClient.email = email
                oldClient.ownerFirstName = firstName
                oldClient.ownerLastName = lastName
                oldClient.ownerPhone = phone

                db.session.commit()
                return jsonify(oldClient)
            else:
                return jsonify({"error": f"Client {client_id} doesn't exist"})

        # create new client object
        new_client = Client(
            companyName=companyName,
            email=email,
            ownerFirstName=firstName,
            ownerLastName=lastName,
            ownerPhone=phone
        )
        
        db.session.add(new_client)
        db.session.commit()

        return jsonify(new_client)
        
    
    def delete(self):
        client_id = request.args.get('client_id')

        return jsonify(deleteTableRow(Client, client_id))



class Users(Resource):
    
    def get(self):
        filters = request.args.to_dict()
        return jsonify(queryHelper(User, filters))


    def put(self):
        user_id = request.args.get('user_id')
        data = request.get_json()  # Retrieve JSON data from the request body

        firstName = data.get('firstName')
        lastName = data.get('lastName')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        city = data.get('city')
        state = data.get('state')
        zip = data.get('zip')

        if user_id:
            oldUser = User.query.get(user_id)
            if oldUser:
                oldUser.firstName = firstName
                oldUser.lastName = lastName
                oldUser.email = email
                oldUser.phone = phone
                oldUser.address = address
                oldUser.city = city
                oldUser.state = state
                oldUser.zip = zip

                db.session.commit()
                return jsonify(oldUser)
            else:
                return jsonify({"error": f"User {user_id} doesn't exist"})

        # create new client object
        new_user = User(
            firstName = firstName,
            lastName = lastName,
            email = email,
            phone = phone,
            address = address,
            city = city,
            state = state,
            zip = zip
        )
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user)
        
    
    def delete(self):
        user_id = request.args.get('user_id')

        if user_id:
            oldUser = User.query.get(user_id)
            if oldUser:
                db.session.delete(oldUser)
                db.session.commit()

                return jsonify({"message": "User Removed"})
            else:
                return jsonify({"error": "User Not Found"})
        else:
            return jsonify({"message": "No user_id"})
        


class Units(Resource):
    
    def get(self):
        filters = request.args.to_dict()
        return jsonify(queryHelper(Unit, filters))
    


    def put(self):
        unit_id = request.args.get('unit_id')
        data = request.get_json()  # Retrieve JSON data from the request body

        client_id = data.get('client_id')
        name = data.get('name')
        pic = data.get('pic')
        info = data.get('info')

        if unit_id:
            oldUnit = Unit.query.get(unit_id)
            if oldUnit:
                oldUnit.client_id = client_id
                oldUnit.name = name
                oldUnit.pic = pic
                oldUnit.info = info

                db.session.commit()
                return jsonify(oldUnit)
            else:
                return jsonify({"error": f"Unit {unit_id} doesn't exist"})

        # create new client object
        new_unit = Unit(
            client_id = client_id,
            name = name,
            pic = pic,
            info = info
        )
        
        db.session.add(new_unit)
        db.session.commit()

        return jsonify(new_unit)
        
    
    def delete(self):
        unit_id = request.args.get('unit_id')

        if unit_id:
            oldUnit = Unit.query.get(unit_id)
            if oldUnit:
                db.session.delete(oldUnit)
                db.session.commit()

                return jsonify({"message": "Unit Removed"})
            else:
                return jsonify({"error": "Unit Not Found"})
        else:
            return jsonify({"message": "No unit_id"})
        

class Bookings(Resource):
    
    def get(self):
        filters = request.args.to_dict()
        return jsonify(queryHelper(Booking, filters))
    

    def put(self):
        booking_id = request.args.get('booking_id')
        data = request.get_json()  # Retrieve JSON data from the request body

        client_id = data.get('client_id')
        user_id = data.get('user_id')
        totalPrice = data.get('totalPrice')
        contractDate = data.get('contractDate')

        if booking_id:
            oldBooking = Booking.query.get(booking_id)
            if oldBooking:
                oldBooking.client_id = client_id
                oldBooking.user_id = user_id
                oldBooking.totalPrice = totalPrice
                oldBooking.contractDate = contractDate

                db.session.commit()
                return jsonify(oldBooking)
            else:
                return jsonify({"error": f"Booking {booking_id} doesn't exist"})

        # create new client object
        new_booking = Booking(
            client_id = client_id,
            user_id = user_id,
            totalPrice = totalPrice,
            contractDate = contractDate
        )
        
        db.session.add(new_booking)
        db.session.commit()

        return jsonify(new_booking)
        
    
    def delete(self):
        booking_id = request.args.get('booking_id')

        if booking_id:
            oldBooking = Booking.query.get(booking_id)
            if oldBooking:
                db.session.delete(oldBooking)
                db.session.commit()

                return jsonify({"message": "Booking Removed"})
            else:
                return jsonify({"error": "Booking Not Found"})
        else:
            return jsonify({"message": "No booking_id"})
        

class BookingDates(Resource):
    
    def get(self):
        filters = request.args.to_dict()
        return jsonify(queryHelper(BookingDate, filters))
    

    def put(self):
        bookingDate_id = request.args.get('bookingDate_id')
        data = request.get_json()  # Retrieve JSON data from the request body

        client_id = data.get('client_id')
        unit_id = data.get('unit')
        booking_id = data.get('booking_id')
        date = data.get('date')

        if bookingDate_id:
            oldBookingDate = BookingDate.query.get(bookingDate_id)
            if oldBookingDate:
                oldBookingDate.client_id = client_id
                oldBookingDate.unit_id = unit_id
                oldBookingDate.booking_id = booking_id
                oldBookingDate.date = date

                db.session.commit()
                return jsonify(oldBookingDate)
            else:
                return jsonify({"error": f"BookingDate {bookingDate_id} doesn't exist"})

        # create new bookingDate object
        new_bookingDate = BookingDate(
            client_id = client_id,
            unit_id = unit_id,
            booking_id = booking_id,
            date = date
        )
        
        db.session.add(new_bookingDate)
        db.session.commit()

        return jsonify(new_bookingDate)
        
    
    def delete(self):
        bookingDate_id = request.args.get('bookingDate_id')

        if bookingDate_id:
            oldBookingDate = BookingDate.query.get(bookingDate_id)
            if oldBookingDate:
                db.session.delete(oldBookingDate)
                db.session.commit()

                return jsonify({"message": "BookingDate Removed"})
            else:
                return jsonify({"error": "BookingDate Not Found"})
        else:
            return jsonify({"message": "No bookingDate_id"})
        


class PriceDates(Resource):
    
    def get(self):
        filters = request.args.to_dict()
        return jsonify(queryHelper(PriceDate, filters))
    

    def put(self):
        priceDate_id = request.args.get('priceDate_id')
        data = request.get_json()  # Retrieve JSON data from the request body

        client_id = data.get('client_id')
        unit_id = data.get('unit_id')
        price = data.get('price')
        deposit = data.get('deposit')
        start_date = data.get('start_date')

        if priceDate_id:
            oldPriceDate = PriceDate.query.get(priceDate_id)
            if oldPriceDate:
                oldPriceDate.client_id = client_id
                oldPriceDate.unit_id = unit_id
                oldPriceDate.price = price
                oldPriceDate.deposit = deposit
                oldPriceDate.start_date = start_date

                db.session.add(oldPriceDate)
                db.session.commit()
                return jsonify(oldPriceDate)
            else:
                return jsonify({"error": f"PriceDate {priceDate_id} doesn't exist"})

        # create new client object
        new_priceDate = PriceDate(
            client_id = client_id,
            unit_id = unit_id,
            price = price,
            deposit = deposit,
            start_date = start_date
        )
        
        db.session.add(new_priceDate)
        db.session.commit()

        return jsonify(new_priceDate)
        
    
    def delete(self):
        priceDate_id = request.args.get('priceDate_id')

        if priceDate_id:
            oldPriceDate = PriceDate.query.get(priceDate_id)
            if oldPriceDate:
                db.session.delete(oldPriceDate)
                db.session.commit()

                return jsonify({"message": "PriceDate Removed"})
            else:
                return jsonify({"error": "PriceDate Not Found"})
        else:
            return jsonify({"message": "No priceDate_id"})
        


class AvailableUnits(Resource):

    # returns available units and price for given date and client
    def get(self):
        client_id = request.args.get('client_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')


        # all units owned by client
        clientUnits = Unit.query.filter(Unit.client_id == client_id).all()

        # prices for client units until end_date
        clientPriceDates = PriceDate.query.filter(
            PriceDate.client_id == client_id, 
            PriceDate.start_date < end_date
        ).order_by(
            desc(PriceDate.start_date)
        ).all()

        availableUnits = {}
        date = stringToDate(end_date)
        for priceDate in clientPriceDates:
            
            while (date >= stringToDate(priceDate.start_date) and date >= stringToDate(start_date)):
                dateString = dateToString(date)
                availableUnits[dateString] = []
                
                for unit in clientUnits:
                    bookedUnit = BookingDate.query.filter(
                        BookingDate.client_id == client_id, 
                        BookingDate.unit_id == unit.id,
                        BookingDate.date == dateString
                    ).first()

                    if (bookedUnit == None):
                        unitPrices = {
                            "unit_id": unit.id,
                            "price": priceDate.price,
                            "deposit": priceDate.deposit
                        }

                        availableUnits[dateString].append(unitPrices)
                
                date -= timedelta(days=1)

        return jsonify(availableUnits)



class Payment(Resource):
    
    def post(self):
        data = request.get_json()  # Retrieve JSON data from the request body

        token = data.get('token')
        amount = int(data.get('amount'))
        unique_key = str(uuid.uuid4())


        client = SquareClient(
            access_token= "EAAAl3pTdEwFrPa1U_4mBBHJrCzvwMSz_55b5VuOOEEzb7_EeYQFnDU9O-cLFnN-",
            environment="sandbox")

        result = client.payments.create_payment(
            body = {
                "source_id": token,
                "idempotency_key": unique_key,
                "amount_money": {
                    "amount": amount,
                    "currency": "USD"
                },
                "accept_partial_authorization": True
            }
        )

        if result.is_success():
            return jsonify(result.body)
        elif result.is_error():
            return jsonify(result.errors)
        else:
            return jsonify({"message": "something went wrong with payments"})
        
class BookUnits(Resource):
    
    def put(self):

        try:
            data = request.get_json()  # Retrieve JSON data from the request body
            user = data.get('user')
            client_id = data.get('client_id')


            # create a new User object
            new_user = User(
                firstName = user.get('firstName'),
                lastName = user.get('lastName'),
                email = user.get('email'),
                phone = user.get('phone'),
                address = user.get('address'),
                city = user.get('city'),
                state = user.get('state'),
                zip = user.get('zip')
            )
            db.session.add(new_user)
            db.session.commit()


            user_id = new_user.id
            totalPrice = float(data.get('totalPrice'))
            totalDeposit = float(data.get('totalDeposit'))
            contractDate = dateToString(datetime.today())

            # create new Booking object
            new_booking = Booking(
                client_id = client_id,
                user_id = user_id,
                totalPrice = totalPrice,
                totalDeposit = totalDeposit,
                contractDate = contractDate
            )
            db.session.add(new_booking)
            db.session.commit()

            dates = data.get('dates')

            for item in dates:
                booking_date = item.get('date')
                unit_id = item.get('unit_id')
                price = item.get('price')
                deposit = item.get('deposit')
                # create new bookingDate object
                new_bookingDate = BookingDate(
                    client_id = client_id,
                    unit_id = unit_id,
                    price = price,
                    deposit = deposit,
                    booking_id = new_booking.id,
                    date = booking_date
                )
            
                db.session.add(new_bookingDate)

            db.session.commit()

            return jsonify({"message": "success"})
        except Exception as e:
            return jsonify({"message": f"error: {str(e)}"})
        
    def delete(self):
        try:
            booking_id = request.args.get('booking_id')
            response = {}

            bookingDates = BookingDate.query.filter(BookingDate.booking_id == booking_id)

            response['bookingDates'] = []
            for bookingDate in bookingDates:
                response['bookingDates'].append(deleteTableRow(BookingDate, bookingDate.id))

            response["bookingDate"] = deleteTableRow(Booking, booking_id)
            
            return jsonify(response)
        except Exception as e:
            return jsonify({"message": f"error: {str(e)}"})

## Actually setup the Api resource routing here
##
api.add_resource(Clients, '/clients')
api.add_resource(Users, '/users')
api.add_resource(Units, '/units')
api.add_resource(Bookings, '/bookings')
api.add_resource(BookingDates, '/booking_dates')
api.add_resource(PriceDates, '/price_dates')
api.add_resource(Payment, '/payment') # square payment
api.add_resource(BookUnits, '/book_units') # create Booking
api.add_resource(AvailableUnits, '/available_units') # create Booking





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)
