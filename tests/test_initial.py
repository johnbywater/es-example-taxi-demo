import pytest

from uuid import uuid4

car_id = uuid4()


@pytest.fixture
def uuid4():
    from uuid import uuid4
    return uuid4()


@pytest.fixture
def system():
    from taxidemo.taxisystem import TaxiSystem

    from eventsourcing.application.sqlalchemy import \
        SQLAlchemyApplication

    system = TaxiSystem(
        infrastructure_class=SQLAlchemyApplication,
        setup_tables=True,
    )

    system.setup()

    return system


def test_system_fixture(system):
    """Prove we can instantiate a system"""
    pass


def test_journey_complete(system):
    app = system.processes['cars']
    assert app.repository[car_id].is_arrived
