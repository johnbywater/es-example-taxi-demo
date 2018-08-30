import json
import os
import tempfile

import pytest

import api
import taxirunner
from taxirunner import init_system


@pytest.fixture
def client():
    _, tmpfile = tempfile.mkstemp()
    os.environ['DB_URI'] = f'sqlite://///{tmpfile}'

    # TODO: stop abusing the rider_id global in taxirunner
    taxirunner.system, taxirunner.rider_id = init_system()
    api.app.config['TESTING'] = True
    client = api.app.test_client()
    yield client
    os.unlink(tmpfile)


def test_client_fixture(client):
    pass


def test_root_without_id_fails(client):
    rv = client.get('/')
    assert rv.status_code == 404


def test_new_request(client):
    rv = client.get('/new')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data['request_id']


def test_full_lifecycle(client):
    rv = client.get('/new')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data['request_id']
    request_id = data['request_id']

    rv = client.get(f'/{request_id}')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data['request_id']
    request_id = data['request_id']
    assert data['booking_id']
    assert data['car_id']
    assert data['is_heading_to_pickup']
    assert not data['is_arrived_at_pickup']
    assert not data['is_car_arrived_at_dropoff']

    rv = client.get(f'/arrived_at_pickup/{request_id}')
    assert rv.status_code == 200
    data = json.loads(rv.data)

    rv = client.get(f'/arrived_at_dropoff/{request_id}')
    assert rv.status_code == 200
    data = json.loads(rv.data)

    rv = client.get(f'/{request_id}')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data['request_id'] == request_id
    assert data['booking_id']
    assert data['car_id']
    assert not data['is_heading_to_pickup']
    assert data['is_arrived_at_pickup']
    assert data['is_car_arrived_at_dropoff']
    






