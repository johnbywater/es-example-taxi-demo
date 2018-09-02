from flask import Flask
from flask_restful import Resource, Api
from taxirunner import (new_ride, set_car_arrived_at_dropoff,
                        set_car_arrived_at_pickup, ride_details, init_system)


app = Flask(__name__)
api = Api(app)


class NewRide(Resource):
    """Invoke to generate a new ride request to get a request_id"""
    def get(self):
        request_id = new_ride('here', 'there')
        return {'request_id': str(request_id)}


class Status(Resource):
    """Invoke with the request_id to get status"""
    def get(self, request_id):
        return ride_details(request_id)


class ArrivedAtPickup(Resource):
    """Invoke with the request_id to advance to the next state"""
    # TODO: convert to get&post
    def get(self, request_id):
        set_car_arrived_at_pickup(request_id)


class ArrivedAtDropoff(Resource):
    """Invoke with the request_id to advance to the next state"""
    # TODO: convert to get&post
    def get(self, request_id):
        set_car_arrived_at_dropoff(request_id)
        return


api.add_resource(NewRide, '/new')
api.add_resource(Status, '/<uuid:request_id>')
api.add_resource(ArrivedAtPickup, '/arrived_at_pickup/<uuid:request_id>')
api.add_resource(ArrivedAtDropoff, '/arrived_at_dropoff/<uuid:request_id>')

if __name__ == '__main__':
    init_system()
    app.run(debug=True)
