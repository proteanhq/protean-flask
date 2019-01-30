"""Module to test Serializer functionality"""

import marshmallow as ma
import pytest
from protean.core.exceptions import ConfigurationError

from protean_flask.core.serializers import EntitySerializer

from ..support.sample_app.entities import Dog


class DogSerializer(EntitySerializer):
    """ Serializer for the Dog Entity """
    class Meta:
        entity = Dog


class TestEntitySerializer:
    """Tests for EntitySerializer class"""

    def test_init(self):
        """Test initialization of EntitySerializer derived class"""
        s = DogSerializer()
        assert s is not None

        # Check that the entity gets serialized correctly
        s_result = s.dump(Dog(id=1, name='Johnny', owner='John'))
        expected_data = {'age': 5, 'id': 1, 'name': 'Johnny', 'owner': 'John'}
        assert s_result.data == expected_data

    def test_abstraction(self):
        """Test that EntitySerializer class itself cannot be initialized"""

        with pytest.raises(ConfigurationError):
            EntitySerializer()

    def test_include_fields(self):
        """ Test the include fields option of the serializer"""

        class DogSerializer2(EntitySerializer):
            """ Serializer for the Dog Entity """
            class Meta:
                entity = Dog
                fields = ('id', 'age')

        s = DogSerializer2()
        assert s is not None

        # Check that the entity gets serialized correctly
        s_result = s.dump(Dog(id=1, name='Johnny', owner='John'))
        expected_data = {'age': 5, 'id': 1}
        assert s_result.data == expected_data

    def test_exclude_fields(self):
        """ Test the exclude fields option of the serializer"""

        class DogSerializer2(EntitySerializer):
            """ Serializer for the Dog Entity """
            class Meta:
                entity = Dog
                exclude = ('id', 'age')

        s = DogSerializer2()
        assert s is not None

        # Check that the entity gets serialized correctly
        s_result = s.dump(Dog(id=1, name='Johnny', owner='John'))
        expected_data = {'name': 'Johnny', 'owner': 'John'}
        assert s_result.data == expected_data

    def test_method_fields(self):
        """ Test the method field type of the serializer"""

        class DogSerializer2(EntitySerializer):
            """ Serializer for the Dog Entity """
            old = ma.fields.Method('get_old')

            def get_old(self, obj):
                """ Check if the dog is old or young """
                if obj.age > 5:
                    return True
                else:
                    return False

            class Meta:
                entity = Dog

        s = DogSerializer2()
        assert s is not None

        # Check that the entity gets serialized correctly
        s_result = s.dump(Dog(id=1, name='Johnny', owner='John'))
        expected_data = {
            'name': 'Johnny',
            'owner': 'John',
            'age': 5,
            'id': 1,
            'old': False
        }
        assert s_result.data == expected_data
