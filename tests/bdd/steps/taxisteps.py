from behave import given, when, then, use_step_matcher
from hamcrest import assert_that, equal_to, is_in

from taxisystem import TaxiSystem, Cars, Car, Riders, Rider, RiderBooking, Booking

use_step_matcher("parse")


@given("taxi system is running")
def step_impl(context):
    assert isinstance(context.system, TaxiSystem)
    assert_that('office', is_in(context.system.processes))
    assert_that('cars', is_in(context.system.processes))
    assert_that('riders', is_in(context.system.processes))

    # Register a car.
    cars = context.system.processes['cars']
    assert_that(cars, isinstance(cars, Cars))

    # Register for work.
    car1 = cars.register_car()
    car2 = cars.register_car()
    assert isinstance(car1, Car)
    assert isinstance(car2, Car)
    car1.__save__()
    car2.__save__()
    context.car_id1 = car1.id
    context.car_id2 = car2.id

    # Check the car is registered.
    assert_that(context.car_id1, is_in(cars.repository))
    assert_that(context.car_id2, is_in(cars.repository))

    # Start work.
    car1.is_available = True
    car2.is_available = True
    car1.__save__()
    car2.__save__()

    # Check the car is available.
    assert_that(cars.repository[car1.id].is_available)
    assert_that(cars.repository[car2.id].is_available)

    # Register a rider.
    riders = context.system.processes['riders']
    assert isinstance(riders, Riders)
    rider = riders.register_rider()
    rider.__save__()
    context.rider_id = rider.id

    # Check the rider is registered.
    assert_that(context.rider_id, is_in(riders.repository))


@when('a rider requests a ride from "{pickup}" to "{dropoff}"')
def step_impl(context, pickup, dropoff):
    # Get registered rider.
    riders = context.system.processes['riders']
    rider = riders.repository[context.rider_id]
    assert isinstance(rider, Rider)

    # Request ride.
    request_id = rider.request_ride(pickup=pickup, dropoff=dropoff)
    rider.__save__()

    # Remember request ID.
    context.request_id = request_id


@then('a car is booked from "{pickup}" to "{dropoff}"')
def step_impl(context, pickup, dropoff):
    riders = context.system.processes['riders']
    rider = riders.repository[context.rider_id]
    assert isinstance(rider, Rider)

    # Check the rider's projection of the office booking.
    booking_id = rider.requests[context.request_id].booking_id
    assert_that(booking_id)
    rider_booking = rider.bookings[booking_id]
    car_id = rider_booking.car_id
    assert_that(car_id)

    # Remember the booking ID and the car ID.
    context.the_booking_id = booking_id
    context.the_car_id = car_id

    # Check the office has the booking.
    office = context.system.processes['office']
    booking = office.repository[context.the_booking_id]
    assert isinstance(booking, Booking)
    assert_that(booking.car_id, equal_to(context.the_car_id))
    assert_that(booking.pickup, equal_to(pickup))
    assert_that(booking.dropoff, equal_to(dropoff))


@then('the car heads to pickup at "{pickup}" and dropoff at "{dropoff}"')
def step_impl(context, pickup, dropoff):
    # Get the car ID.
    app = context.system.processes['cars']
    car = app.repository[context.the_car_id]
    assert isinstance(car, Car)

    # Check the state of the car.
    assert_that(car.is_heading_to_pickup, equal_to(True))
    assert_that(car.offered_pickup, equal_to(pickup))
    assert_that(car.offered_dropoff, equal_to(dropoff))


@when("the car has arrived at the pickup position")
def step_impl(context):
    app = context.system.processes['cars']
    car = app.repository[context.the_car_id]
    assert isinstance(car, Car)

    # Press the "arrived" button (or auto-detect location match).
    car.arrived_at_pickup()
    car.__save__()

    assert_that(car.is_heading_to_pickup, equal_to(False))


@then("the office knows the car arrived at the pickup position")
def step_impl(context):
    office = context.system.processes['office']
    booking = office.repository[context.the_booking_id]

    # Check the office booking.
    assert_that(booking.is_car_arrived_at_pickup)


@then("the rider knows the car arrived at the pickup position")
def step_impl(context):
    riders = context.system.processes['riders']
    rider = riders.repository[context.rider_id]
    assert isinstance(rider, Rider)

    # Check the rider's booking projection.
    rider_booking = rider.bookings[context.the_booking_id]
    assert isinstance(rider_booking, RiderBooking)
    assert_that(rider_booking.is_car_arrived_at_pickup)


@when("the car has arrived at the dropoff position")
def step_impl(context):
    app = context.system.processes['cars']
    car = app.repository[context.the_car_id]
    assert isinstance(car, Car)

    # Press the "arrived" button (or auto-detect location match).
    car.arrived_at_dropoff()
    car.__save__()


@then("the office knows the car arrived at the dropoff position")
def step_impl(context):
    office = context.system.processes['office']
    booking = office.repository[context.the_booking_id]
    assert isinstance(booking, Booking)

    # Check the office booking.
    assert_that(booking.is_car_arrived_at_dropoff)


@then("the rider knows the car arrived at the dropoff position")
def step_impl(context):
    riders = context.system.processes['riders']
    rider = riders.repository[context.rider_id]
    assert isinstance(rider, Rider)

    # Check the rider's booking projection.
    rider_booking = rider.bookings[context.the_booking_id]
    assert isinstance(rider_booking, RiderBooking)
    assert_that(rider_booking.is_car_arrived_at_dropoff)
