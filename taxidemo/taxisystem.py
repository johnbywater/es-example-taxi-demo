from eventsourcing.application.process import ProcessApplication
from eventsourcing.application.system import System


class TaxiSystem(System):
    def __init__(self, **kwargs):
        super(TaxiSystem, self).__init__(
            Office | Cars | Office,
            Office | Riders | Office,
            **kwargs
        )


class Office(ProcessApplication):
    pass


class Cars(ProcessApplication):
    pass


class Riders(ProcessApplication):
    pass