"""Module to test Viewset functionality and features"""
import json

import pytest
from tests.support.sample_app import app
from tests.support.sample_app.entities import Dog
from tests.support.sample_app.entities import Human


class TestGenericAPIResourceSet:
    """Class to test GenericAPIResourceSet functionality and methods"""

    @pytest.fixture(scope="function")
    def client(self):
        """ Setup client for test cases """
        yield app.test_client()

    def test_set_show(self, client):
        """ Test retrieving an entity using the resource set"""
        # Create a human object
        Human.create(id=1, name='John')

        # Fetch this human by ID
        rv = client.get('/humans/1')
        assert rv.status_code == 200
        expected_resp = {
            'human': {'contact': None, 'id': 1, 'name': 'John'}
        }
        assert rv.json == expected_resp

        # Delete the human now
        human = Human.get(1)
        human.delete()

    def test_set_list(self, client):
        """ Test listing an entity using the resource set"""
        # Create Human objects
        Human.create(id=2, name='Jane')
        Human.create(id=3, name='Mary')

        # Get the list of humans
        rv = client.get('/humans?order_by[]=id')
        assert rv.status_code == 200
        assert rv.json['total'] == 2
        assert rv.json['humans'][0] == {'id': 2, 'name': 'Jane', 'contact': None}

    def test_set_create(self, client):
        """ Test creating an entity using the resource set """

        # Create a human object
        rv = client.post('/humans', data=json.dumps(dict(id=1, name='John')),
                         content_type='application/json')
        assert rv.status_code == 201

        expected_resp = {
            'human': {'contact': None, 'id': 1, 'name': 'John'}
        }
        assert rv.json == expected_resp

        # Delete the human now
        human = Human.get(1)
        human.delete()

    def test_set_update(self, client):
        """ Test updating an entity using the resource set """

        # Create a human object
        Human.create(id=1, name='John')

        # Update the human object
        rv = client.put('/humans/1', data=json.dumps(dict(contact='9000900090')),
                        content_type='application/json')
        assert rv.status_code == 200

        expected_resp = {
            'human': {'contact': '9000900090', 'id': 1, 'name': 'John'}
        }
        assert rv.json == expected_resp

        # Delete the human now
        human = Human.get(1)
        human.delete()

    def test_set_delete(self, client):
        """ Test deleting an entity using the resource set """

        # Create a human object
        Human.create(id=1, name='John')

        # Delete the dog object
        rv = client.delete('/humans/1')
        assert rv.status_code == 204
        assert rv.data == b''

    def test_custom_route(self, client):
        """ Test custom routes using the resource set """

        # Create a human object
        Human.create(id=1, name='John')
        Dog.create(id=1, name='Johnny', owner='John')
        Dog.create(id=2, name='Mary', owner='John', age=3)
        Dog.create(id=3, name='Grady', owner='Jane', age=8)

        # Get the custom route
        rv = client.get('/humans/1/my_dogs')
        assert rv.status_code == 200
        assert rv.json['total'] == 2
        assert rv.json['dogs'][0] == {'age': 3, 'id': 2, 'name': 'Mary',
                                      'owner': 'John'}
