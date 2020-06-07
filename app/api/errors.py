from flask import jsonify
from app.exceptions import ValidationError
from . import api

def bad_request(message):
    """Responde em forma de json o erro not found"""
    print("Teste")
    response = jsonify({'error':'bad request' , 'message' : message})
    response.status_code = 400

def unauthorized(message):
    print("Teste1")
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    print("Teste2")
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

def not_found(message):
    response = jsonify({'error': 'not found', 'message': message})
    response.status_code = 404
    return response


@api.errorhandler(404)
def validation_error(e):
    return not_found("Country not found")


 
