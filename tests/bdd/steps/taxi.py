from uuid import uuid4

from behave import *

from taxisystem import TaxiSystem

use_step_matcher("re")


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
