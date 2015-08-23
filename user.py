from neomodel import (Property, StructuredNode, StringProperty, DateProperty, AliasProperty,
                      DateTimeProperty, RelationshipFrom, RelationshipTo, BooleanProperty, Relationship, UniqueProperty,
                      DoesNotExist, ZeroOrOne)
from datetime import datetime
from serializable_structured_node import SerializableStructuredNode
from flask import jsonify, make_response
import application_codes
from errors import WrongTypeError
import http_error_codes


class User(SerializableStructuredNode):
    """This is the User entity. Added password"""

    __index__ = 'User'

    # INFO
    version = (1, 0, 0)

    # ATTRIBUTES
    type = 'users'
    id = AliasProperty(to='email')
    email = StringProperty(unique_index=True, required=True)
    signup_method = StringProperty(required=True)
    
    # RELATIONSHIPS
    friends = Relationship('User', 'HAS_FRIEND')
    mom = RelationshipTo('User', 'HAS_MOM', cardinality=ZeroOrOne)

















