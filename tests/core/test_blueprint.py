"""Module to test View functionality and features"""

from protean.core.repository import repo
from tests.support.sample_app import app


class TestBlueprint:
    """Class to test Blueprint functionality of flask with this package"""

    @classmethod
    def setup_class(cls):
        """ Setup for this test case"""

        # Create the test client
        cls.client = app.test_client()

    @classmethod
    def teardown_class(cls):
        """ Teardown for this test case"""

        # Delete all dog objects
        repo.DogSchema.delete_all()
        repo.HumanSchema.delete_all()

    def test_show(self):
        """ Test retrieving an entity using blueprint ShowAPIResource"""

        # Create a dog object
        repo.DogSchema.create(id=5, name='Johnny', owner='John')

        # Fetch this dog by ID
        rv = self.client.get('/blueprint/dogs/5')
        assert rv.status_code == 200

        expected_resp = {
            'dog': {'age': 5, 'id': 5, 'name': 'Johnny', 'owner': 'John'}
        }
        assert rv.json == expected_resp

        # Test search by invalid id
        rv = self.client.get('/blueprint/dogs/6')
        assert rv.status_code == 404

        # Delete the dog now
        repo.DogSchema.delete(5)

    def test_set_show(self):
        """ Test retrieving an entity using the blueprint resource set"""
        # Create a human object
        repo.HumanSchema.create(id=1, name='John')

        # Fetch this human by ID
        rv = self.client.get('/blueprint/humans/1')
        assert rv.status_code == 200
        expected_resp = {
            'human': {'contact': None, 'id': 1, 'name': 'John'}
        }
        assert rv.json == expected_resp

        # Delete the human now
        repo.HumanSchema.delete(1)

    def test_custom_route(self):
        """ Test custom routes using the blueprint resource set """

        # Create a human object
        repo.HumanSchema.create(id=1, name='John')
        repo.DogSchema.create(id=5, name='Johnny', owner='John')

        # Get the custom route
        rv = self.client.get('/humans/1/my_dogs')
        assert rv.status_code == 200
        assert rv.json['total'] == 1
        assert rv.json['dogs'][0] == {'age': 5, 'id': 5, 'name': 'Johnny', 'owner': 'John'}
