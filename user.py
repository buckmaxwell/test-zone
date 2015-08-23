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


    '''
    events = RelationshipFrom('Event', 'CREATED_BY')
    venues = RelationshipFrom('Venue', 'CREATED_BY')
    companies = RelationshipFrom('Company', 'CREATED_BY')
    artists = RelationshipFrom('Company', 'CREATED_BY')
    '''


def create(request_json):
    response = dict()
    status_code = http_error_codes.INTERNAL_SERVER_ERROR
    new_user, location = None, None
    try:
        data = request_json['data']

        if data['type'] != 'users':
            raise WrongTypeError('type should be users when attempting to create a user resource')

        attributes = data.get('attributes')
        if attributes:
            new_user = User(
                email=attributes.get('email'),
                signup_method=attributes.get('signup_method'))
            new_user.save()

        relationships = data.get('relationships')
        if relationships:
            friends = relationships.get('friends')
            if friends:
                friends = friends['data']
                for friend in friends:
                    the_type = friend['type']
                    if the_type != 'users':
                        raise WrongTypeError('type should be users when attempting to create a friend resource')
                    the_id = friend['id']
                    new_users_friend = User.nodes.get(id=the_id)
                    new_user.friends.connect(new_users_friend)
                    new_user.save()

        response['data'] = new_user.get_resource_object()
        response['links'] = {'self': new_user.get_self_link()}
        status_code = http_error_codes.CREATED
        location = new_user.get_self_link()

    except UniqueProperty:
        response = {'error': application_codes.UNIQUE_KEY_VIOLATION[0]}
        status_code = http_error_codes.BAD_REQUEST
        try:
            new_user.delete()
        except:
            pass

    except WrongTypeError as e:
        response = {'error': application_codes.WRONG_TYPE_VIOLATION[0], 'message': str(e)}
        status_code = http_error_codes.BAD_REQUEST
        try:
            new_user.delete()
        except:
            pass

    except KeyError as e:
        response = {'error': application_codes.BAD_FORMAT_VIOLATION[0], 'message': str(e)}
        status_code = http_error_codes.BAD_REQUEST
        try:
            new_user.delete()
        except:
            pass

    r = make_response(jsonify(response))
    r.headers['Content-Type'] = "application/vnd.api+json; charset=utf-8"
    if location and new_user:
        r.headers['Location'] = location

    r.status_code = status_code

    return r


def update(request_json):
    return None


def delete(request_json):
    return None
        
















