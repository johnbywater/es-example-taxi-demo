import os

from eventsourcing.application.sqlalchemy import SQLAlchemyApplication
from hamcrest import assert_that, equal_to, is_in

from taxisystem import TaxiSystem, Car, Rider, Booking

# set for service, reset by api tests
os.environ['DB_URI'] = 'sqlite:///taxi_testing.sq3'


def init_system():
    """Called locally and for api testing"""

    sys = TaxiSystem(
        infrastructure_class=SQLAlchemyApplication,
        setup_tables=True,
    )

    with sys:
        assert isinstance(sys, TaxiSystem)

        # Register a car.
        cars = sys.processes['cars']

        # Register for work.
        car1 = cars.register_car()
        car2 = cars.register_car()
        car1.__save__()
        car2.__save__()

        # Ready for work
        car1.is_available = True
        car2.is_available = True
        car1.__save__()
        car2.__save__()

        # Check the car is available.
        assert_that(cars.repository[car1.id].is_available)
        assert_that(cars.repository[car2.id].is_available)

        # Register a rider.
        riders = sys.processes['riders']
        rider = riders.register_rider()
        rider.__save__()
        rid_id = rider.id

        # Check the rider is registered.
        assert_that(rid_id, is_in(riders.repository))

        # Get registered rider.
        riders = sys.processes['riders']
        rider = riders.repository[rid_id]
        assert isinstance(rider, Rider)

    return sys, rid_id


# works for now. Also monkey patched by api tests
system, rider_id = init_system()


# TODO: Result of copy-paste. Simplify
def has_car_arrived_at_pickup(request_id):
    with system:
        riders = system.processes['riders']
        rider = riders.repository[rider_id]

        booking_id = rider.requests[request_id].booking_id
        assert_that(booking_id)

        rider_booking = rider.bookings[booking_id]
        car_id = rider_booking.car_id
        assert_that(car_id)

        cars = system.processes['cars']
        car = cars.repository[car_id]
        assert isinstance(car, Car)

        return car.is_arrived_at_pickup


def new_ride(pickup, dropoff):
    with system:
        riders = system.processes['riders']
        rider = riders.repository[rider_id]
        assert isinstance(rider, Rider)

        request_id = rider.request_ride(pickup=pickup, dropoff=dropoff)
        rider.__save__()
        return request_id


def set_car_arrived_at_pickup(request_id):
    with system:
        riders = system.processes['riders']
        rider = riders.repository[rider_id]

        booking_id = rider.requests[request_id].booking_id
        assert_that(booking_id)

        rider_booking = rider.bookings[booking_id]
        car_id = rider_booking.car_id
        assert_that(car_id)

        cars = system.processes['cars']
        car = cars.repository[car_id]
        assert isinstance(car, Car)

        car.arrived_at_pickup()
        car.__save__()


def set_car_arrived_at_dropoff(request_id):
    with system:
        riders = system.processes['riders']
        rider = riders.repository[rider_id]

        booking_id = rider.requests[request_id].booking_id
        assert_that(booking_id)

        rider_booking = rider.bookings[booking_id]
        car_id = rider_booking.car_id
        assert_that(car_id)

        cars = system.processes['cars']
        car = cars.repository[car_id]
        assert isinstance(car, Car)

        car.arrived_at_dropoff()
        car.__save__()


def ride_details(request_id):
    with system:

        riders = system.processes['riders']
        rider = riders.repository[rider_id]

        booking_id = rider.requests[request_id].booking_id
        assert_that(booking_id)
        rider_booking = rider.bookings[booking_id]
        car_id = rider_booking.car_id
        assert_that(car_id)

        office = system.processes['office']
        booking = office.repository[booking_id]
        assert isinstance(booking, Booking)
        assert_that(booking.car_id, equal_to(car_id))

        cars = system.processes['cars']
        car = cars.repository[car_id]
        assert isinstance(car, Car)

        booking = office.repository[booking_id]

        return dict(request_id=str(request_id),
                    booking_id=str(booking_id),
                    car_id=str(booking.car_id),
                    is_heading_to_pickup=car.is_heading_to_pickup,
                    is_arrived_at_pickup=car.is_arrived_at_pickup,
                    is_car_arrived_at_dropoff=booking.is_car_arrived_at_dropoff
                    )


