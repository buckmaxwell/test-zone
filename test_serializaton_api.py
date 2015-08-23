from flask import Flask, jsonify, request
import serializable_structured_node
import user as users
from user import User
import application_codes

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'meta':
            {
                'working': True,
                'message': 'The api is working properly'
            }
        }
        )


@app.route('/users/<id>', methods=['GET', 'PATCH', 'DELETE'])
@app.route('/users', defaults={'id': None}, methods=['POST', 'GET'])
def user(id):
    response = None
    if request.method == 'POST':
        response = User.create_resource(eval(request.data))
    elif request.method == 'PATCH':
        response = User.update_resource(eval(request.data), id)
    elif request.method == 'DELETE':
        response = User.set_resource_inactive(id)
    elif request.method == 'GET':
        response = User.get_resource_or_collection(request.args, id)
    return response

@app.route('/users/<id>/relationships/<related_collection_name>/<related_resource>', methods=['GET', 'DELETE'])
@app.route('/users/<id>/relationships/<related_collection_name>', defaults={'related_resource': None}, methods=['GET', 'DELETE'])
def user_relationships(id, related_collection_name, related_resource):
    response = None
    if request.method == 'GET':
        response = User.get_relationship(request.args, id, related_collection_name, related_resource)
    elif request.method == 'DELETE':
        response = User.delete_relationship(id, related_collection_name, related_resource)
    return response


@app.route('/users/<id>/<related_collection_name>/<related_resource>', methods=['GET', 'DELETE'])
@app.route('/users/<id>/<related_collection_name>', defaults={'related_resource': None}, methods=['GET', 'DELETE'])
def user_related_resources(id, related_collection_name, related_resource):
    response = None
    if request.method == 'GET':
        response = User.get_related_resources(request.args, id, related_collection_name, related_resource)
    if request.method == 'DELETE':
        response = User.set_related_resources_inactive(id, related_collection_name, related_resource)
    return response


@app.errorhandler(404)
def not_found(error):
    return application_codes.error_response([application_codes.RESOURCE_NOT_FOUND])

@app.errorhandler(405)
def method_not_allowed(error):
    return application_codes.error_response([application_codes.METHOD_NOT_ALLOWED])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10200, debug=True)