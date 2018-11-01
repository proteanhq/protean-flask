"""Module to test View functionality and features"""

import pytest

from protean.core.repository import repo_factory
from tests.support.sample_app import app


class TestCustomMethodView:
    """Class to test CustomMethodView methods"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_dispatch_request(self):
        """Test Dispatch request flow for different HTTP methods"""


class TestGenericAPIResource:
    """Class to test GenericAPIResource functionality and methods"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_init(self):
        """Test initialization of GenericResource object"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_get(self):
        """Test `get` method of GenericResource"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_index(self):
        """Test `index` method of GenericResource"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_create(self):
        """Test `create` method of GenericResource"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_update(self):
        """Test `update` method of GenericResource"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_show(self):
        """Test `show` method of GenericResource"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_delete(self):
        """Test `delete` method of GenericResource"""


class TestShowAPIResource:
    """Class to test ShowAPIResource functionality and methods"""

    def test_show(self):
        """ Test that the show API returns an entity"""
        # Create a dog object
        repo_factory.DogSchema.create(id=1, name='Johnny', owner='John')

        # Fetch this dog by ID
        client = app.test_client()
        rv = client.get('/dogs/1')
        assert rv.status_code == 200

        expected_resp = {
            'dog': {'age': 5, 'id': 1, 'name': 'Johnny', 'owner': 'John'}
        }
        assert rv.json == expected_resp

        # Test search by invalid id
        client = app.test_client()
        rv = client.get('/dogs/2')
        assert rv.status_code == 404
