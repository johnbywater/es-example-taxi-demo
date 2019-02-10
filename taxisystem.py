from collections import OrderedDict
from uuid import uuid4

from eventsourcing.application.process import ProcessApplication
from eventsourcing.application.system import System
from eventsourcing.domain.model.aggregate import AggregateRoot
from eventsourcing.domain.model.decorators import attribute


class Booking(AggregateRoot):
    def __init__(self, rider_id, request_id, pickup, dropoff, **kwargs):
        super(Booking, self).__init__(**kwargs)
        self._rider_id = rider_id
        self._request_id = request_id
        self._pickup = pickup
        self._dropoff = dropoff
        self._car_id = None
        self._is_car_arrived_at_pickup = False
        self._is_car_arrived_at_dropoff = False

    @property
    def rider_id(self):
        return self._rider_id

    @property
    def request_id(self):
        return self._request_id

    @property
    def pickup(self):
        return self._pickup

    @property
    def dropoff(self):
        return self._dropoff

    @property
    def car_id(self):
        return self._car_id

    @property
    def is_car_arrived_at_pickup(self):
        return self._is_car_arrived_at_pickup

    @property
    def is_car_arrived_at_dropoff(self):
        return self._is_car_arrived_at_dropoff

    class Event(AggregateRoot.Event):
        pass

    class Created(Event, AggregateRoot.Created):
        @property
        def rider_id(self):
            return self.__dict__['rider_id']

        @property
        def request_id(self):
            return self.__dict__['request_id']

        @property
        def pickup(self):
            return self.__dict__['pickup']

        @property
        def dropoff(self):
            return self.__dict__['dropoff']

    def accept_offer(self, car_id):
        self.__trigger_event__(
            event_class=self.RideOfferAccepted,
            car_id=car_id,
            rider_id=self.rider_id,
            request_id=self.request_id
        )

    class RideOfferAccepted(Event):
        @property
        def rider_id(self):
            return self.__dict__['rider_id']

        @property
        def car_id(self):
            return self.__dict__['car_id']

        def mutate(self, obj):
            obj._car_id = self.car_id

    def reject_offer(self, car_id):
        self.__trigger_event__(
            event_class=self.RideOfferRejected,
            car_id=car_id,
        )

    class RideOfferRejected(Event):
        @property
        def car_id(self):
            return self.__dict__['car_id']

    def track_car_arrived_at_pickup(self):
        self.__trigger_event__(
            event_class=self.CarArrivedAtPickup,
            rider_id=self.rider_id
        )

    class CarArrivedAtPickup(Event):
        @property
        def rider_id(self):
            return self.__dict__['rider_id']

        def mutate(self, obj):
            obj._is_car_arrived_at_pickup = True

    def track_car_arrived_at_dropoff(self):
        self.__trigger_event__(
            event_class=self.CarArrivedAtDropoff,
            rider_id=self.rider_id
        )

    class CarArrivedAtDropoff(Event):
        @property
        def rider_id(self):
            return self.__dict__['rider_id']

        def mutate(self, obj):
            obj._is_car_arrived_at_dropoff = True


class Car(AggregateRoot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_available = False
        self._offered_booking_id = None
        self._offered_pickup = None
        self._offered_dropoff = None
        self._is_heading_to_pickup = False
        self._is_arrived_at_pickup = False

    @property
    def offered_pickup(self):
        return self._offered_pickup

    @property
    def offered_dropoff(self):
        return self._offered_dropoff

    @attribute
    def is_available(self):
        pass

    @attribute
    def is_heading_to_pickup(self):
        pass

    @attribute
    def is_arrived_at_pickup(self):
        pass

    class Event(AggregateRoot.Event):
        pass

    class Created(Event, AggregateRoot.Created):
        pass

    class AttributeChanged(Event, AggregateRoot.AttributeChanged):
        pass

    def offer_ride(self, booking_id, pickup, dropoff):
        self.__trigger_event__(
            self.RideOffered,
            booking_id=booking_id,
            pickup=pickup,
            dropoff=dropoff
        )

    class RideOffered(Event):
        @property
        def booking_id(self):
            return self.__dict__['booking_id']

        @property
        def pickup(self):
            return self.__dict__['pickup']

        @property
        def dropoff(self):
            return self.__dict__['dropoff']

        def mutate(self, obj):
            assert isinstance(obj, Car)
            obj._is_available = False
            obj._offered_booking_id = self.booking_id
            obj._offered_pickup = self.pickup
            obj._offered_dropoff = self.dropoff

    def arrived_at_pickup(self):
        self.__trigger_event__(
            event_class=self.ArrivedAtPickup,
            booking_id=self._offered_booking_id
        )

    class ArrivedAtPickup(Event):
        @property
        def booking_id(self):
            return self.__dict__['booking_id']

        def mutate(self, obj):
            obj._is_heading_to_pickup = False
            obj._is_arrived_at_pickup = True

    def arrived_at_dropoff(self):
        self.__trigger_event__(
            self.ArrivedAtDropoff,
            booking_id=self._offered_booking_id
        )

    class ArrivedAtDropoff(Event):
        @property
        def booking_id(self):
            return self.__dict__['booking_id']

        def mutate(self, obj):
            obj._is_arrived_at_dropoff = True


class Rider(AggregateRoot):
    def __init__(self, **kwargs):
        super(Rider, self).__init__(**kwargs)
        self.requests = OrderedDict()
        self.bookings = OrderedDict()

    class Event(AggregateRoot.Event):
        pass

    class Created(Event, AggregateRoot.Created):
        pass

    def request_ride(self, pickup, dropoff):
        request_id = uuid4()
        self.__trigger_event__(
            event_class=self.RideRequested,
            request_id=request_id,
            pickup=pickup,
            dropoff=dropoff
        )
        return request_id

    class RideRequested(Event):
        @property
        def request_id(self):
            return self.__dict__['request_id']

        @property
        def pickup(self):
            return self.__dict__['pickup']

        @property
        def dropoff(self):
            return self.__dict__['dropoff']

        def mutate(self, obj):
            obj.requests[self.request_id] = RiderRequest(
                pickup=self.pickup,
                dropoff=self.dropoff
            )

    def track_booking_created(self, request_id, booking_id):
        self.__trigger_event__(
            event_class=self.BookingCreated,
            request_id=request_id,
            booking_id=booking_id
        )

    class BookingCreated(Event):
        @property
        def request_id(self):
            return self.__dict__['request_id']

        @property
        def booking_id(self):
            return self.__dict__['booking_id']

        def mutate(self, obj):
            obj.requests[self.request_id].booking_id = self.booking_id
            obj.bookings[self.booking_id] = RiderBooking(request_id=self.request_id)

    def track_ride_offer_accepted(self, booking_id, car_id):
        self.__trigger_event__(
            event_class=self.RideOfferAccepted,
            booking_id=booking_id,
            car_id=car_id
        )

    class RideOfferAccepted(Event):
        @property
        def booking_id(self):
            return self.__dict__['booking_id']

        @property
        def car_id(self):
            return self.__dict__['car_id']

        def mutate(self, obj):
            obj.bookings[self.booking_id].car_id = self.car_id

    def track_car_arrived_at_pickup(self, booking_id):
        self.__trigger_event__(
            event_class=self.CarArrivedAtPickup,
            booking_id=booking_id
        )

    class CarArrivedAtPickup(Event):
        @property
        def booking_id(self):
            return self.__dict__['booking_id']

        def mutate(self, obj):
            rider_booking = obj.bookings[self.booking_id]
            assert isinstance(rider_booking, RiderBooking)
            rider_booking.is_car_arrived_at_pickup = True

    def track_car_arrived_at_dropoff(self, booking_id):
        self.__trigger_event__(
            event_class=self.CarArrivedAtDropoff,
            booking_id=booking_id
        )

    class CarArrivedAtDropoff(Event):
        @property
        def booking_id(self):
            return self.__dict__['booking_id']

        def mutate(self, obj):
            rider_booking = obj.bookings[self.booking_id]
            assert isinstance(rider_booking, RiderBooking)
            rider_booking.is_car_arrived_at_dropoff = True


class RiderRequest(object):
    def __init__(self, pickup, dropoff):
        self.booking_id = None
        self.pickup = pickup
        self.dropoff = dropoff


class RiderBooking(object):
    def __init__(self, request_id):
        self.request_id = request_id
        self.car_id = None
        self.is_car_arrived_at_pickup = False
        self.is_car_arrived_at_dropoff = False


class Office(ProcessApplication):
    persist_event_type = Booking.Event

    def policy(self, repository, event):
        if isinstance(event, Rider.RideRequested):
            return self.create_booking(
                rider_id=event.originator_id,
                request_id=event.request_id,
                pickup=event.pickup,
                dropoff=event.dropoff
            )

        elif isinstance(event, Car.RideOffered):
            booking = repository[event.booking_id]
            assert isinstance(booking, Booking)
            car_id = event.originator_id
            if booking.car_id is None:
                booking.accept_offer(car_id)
            else:
                booking.reject_offer(car_id)

        elif isinstance(event, Car.ArrivedAtPickup):
            booking = repository[event.booking_id]
            assert isinstance(booking, Booking)
            booking.track_car_arrived_at_pickup()

        elif isinstance(event, Car.ArrivedAtDropoff):
            booking = repository[event.booking_id]
            assert isinstance(booking, Booking)
            booking.track_car_arrived_at_dropoff()

    @staticmethod
    def create_booking(rider_id, request_id, pickup, dropoff):
        return Booking.__create__(
            rider_id=rider_id,
            request_id=request_id,
            pickup=pickup,
            dropoff=dropoff
        )


class Cars(ProcessApplication):
    persist_event_type = Car.Event

    def policy(self, repository, event):
        if isinstance(event, Booking.Created):
            # Cars make offer if available.
            for car_id in self.repository.event_store.record_manager.all_sequence_ids():
                car = repository[car_id]
                assert isinstance(car, Car)
                if car.is_available:
                    car.offer_ride(
                        booking_id=event.originator_id,
                        pickup=event.pickup,
                        dropoff=event.dropoff,
                    )

        elif isinstance(event, Booking.RideOfferAccepted):
            car = repository[event.car_id]
            car.is_heading_to_pickup = True

        elif isinstance(event, Booking.RideOfferRejected):
            car = repository[event.car_id]
            car.is_available = True

    @staticmethod
    def register_car():
        return Car.__create__()


class Riders(ProcessApplication):
    persist_event_type = Rider.Event

    @staticmethod
    def policy(repository, event):
        if isinstance(event, Booking.Created):
            rider = repository[event.rider_id]
            assert isinstance(rider, Rider)
            rider.track_booking_created(event.request_id, event.originator_id)

        elif isinstance(event, Booking.RideOfferAccepted):
            rider = repository[event.rider_id]
            assert isinstance(rider, Rider)
            rider.track_ride_offer_accepted(event.originator_id, event.car_id)

        elif isinstance(event, Booking.CarArrivedAtPickup):
            rider = repository[event.rider_id]
            assert isinstance(rider, Rider)
            rider.track_car_arrived_at_pickup(event.originator_id)

        elif isinstance(event, Booking.CarArrivedAtDropoff):
            rider = repository[event.rider_id]
            assert isinstance(rider, Rider)
            rider.track_car_arrived_at_dropoff(event.originator_id)

    @staticmethod
    def register_rider():
        return Rider.__create__()


class TaxiSystem(System):
    def __init__(self, **kwargs):
        super(TaxiSystem, self).__init__(
            Office | Cars | Office | Riders | Office,
            **kwargs
        )
