"""Module to test View functionality and features"""

import pytest


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


class TestGenericProtectedAPIResource:
    """Class to test GenericAPIResource functionality and methods"""

    @pytest.mark.skip(reason="To Be Implemented")
    def test_method_decoration(self):
        """Test that methods in GenericProtectedResource are decorated for authentication"""
