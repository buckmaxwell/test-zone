from http_error_codes import (OK, CREATED, BAD_REQUEST, UNAUTHORIZED, FORBIDDEN, NOT_FOUND,
                              CONFLICT, INTERNAL_SERVER_ERROR, NOT_ALLOWED)
from flask import jsonify, make_response

BAD_FORMAT_VIOLATION = '4000', 'there is a problem with the request format', BAD_REQUEST
UNIQUE_KEY_VIOLATION = '4001', 'a uniqueness constraint is violated by the request', BAD_REQUEST
WRONG_TYPE_VIOLATION = '4002', 'the type key does not match the resource requested', BAD_REQUEST
PARAMETER_NOT_SUPPORTED_VIOLATION = '4003', 'a query parameter you tried to use is not supported for this endpoint', BAD_REQUEST

RESOURCE_NOT_FOUND = '4040', 'the requested resource was not found on the server', NOT_FOUND

METHOD_NOT_ALLOWED = '4050', 'the http method you tried is not a legal operation on this resource', NOT_ALLOWED


def error_response(array_of_application_code_tuples):
    errors = list()
    for app_code_tuple in array_of_application_code_tuples:
        error = dict()
        error['status'] = app_code_tuple[2]
        error['code'] = app_code_tuple[0]
        error['title'] = app_code_tuple[1]
        errors.append(error)

    r = make_response(jsonify({'errors': errors}))
    r.status_code = app_code_tuple[2]
    r.headers['Content-Type'] = "application/vnd.api+json; charset=utf-8"

    return r


