"""Module to test View functionality and features"""

import pytest
import json

from protean.core.repository import repo_factory
from tests.support.sample_app import app


class TestCustomMethodView:
    """Class to test CustomMethodView methods"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_dispatch_request(self):
        """Test Dispatch request flow for different HTTP methods"""


class TestGenericPIResource:
    """Class to test Generic API Respoirce functionality and methods"""

    @classmethod
    def setup_class(cls):
        """ Setup for this test case"""

        # Create the test client
        cls.client = app.test_client()

    def test_show(self):
        """ Test retrieving an entity using ShowAPIResource"""

        # Create a dog object
        repo_factory.DogSchema.create(id=1, name='Johnny', owner='John')

        # Fetch this dog by ID
        rv = self.client.get('/dogs/1')
        assert rv.status_code == 200

        expected_resp = {
            'dog': {'age': 5, 'id': 1, 'name': 'Johnny', 'owner': 'John'}
        }
        assert rv.json == expected_resp

        # Test search by invalid id
        rv = self.client.get('/dogs/2')
        assert rv.status_code == 404

        # Delete the dog now
        repo_factory.DogSchema.delete(1)

    def test_create(self):
        """ Test creating an entity using CreateAPIResource """

        # Create a dog object
        rv = self.client.post('/dogs',
                              data=json.dumps(
                                  dict(id=1, name='Johnny', owner='John')),
                              content_type='application/json')
        assert rv.status_code == 201

        expected_resp = {
            'dog': {'age': 5, 'id': 1, 'name': 'Johnny', 'owner': 'John'}
        }
        assert rv.json == expected_resp

        # Test value has been added to db
        dog = repo_factory.DogSchema.get(1)
        assert dog is not None
        assert dog.id == 1

        # Delete the dog now
        repo_factory.DogSchema.delete(1)

    def test_list(self):
        """ Test listing an entity using ListAPIResource """
        # Create a dog objects
        repo_factory.DogSchema.create(id=1, name='Johnny', owner='John')
        repo_factory.DogSchema.create(id=2, name='Mary', owner='John', age=3)
        repo_factory.DogSchema.create(id=3, name='Grady', owner='Jane', age=8)
        repo_factory.DogSchema.create(id=4, name='Brawny', owner='John', age=2)

        # Get the list of dogs
        rv = self.client.get('/dogs?order_by[]=age')
        assert rv.status_code == 200
        assert rv.json['total'] == 4
        assert rv.json['dogs'][0] == \
               {'age': 2, 'id': 4, 'name': 'Brawny', 'owner': 'John'}

        # Test with filters
        rv = self.client.get('/dogs?owner=Jane')
        assert rv.status_code == 200
        assert rv.json['total'] == 1
