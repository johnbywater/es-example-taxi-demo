from uuid import uuid4

from behave import *
from eventsourcing.application.process import ProcessApplication
from eventsourcing.application.system import System

use_step_matcher("re")


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


@given("Taxi system is running")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert isinstance(context.system, TaxiSystem)
    assert 'office' in context.system.processes
    assert 'cars' in context.system.processes
    assert 'riders' in context.system.processes


@when("A rider hails a taxi")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.car_id = uuid4()


@then("A taxi arrives")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    app = context.system.processes['cars']
    assert app.repository[context.car_id].is_arrived
