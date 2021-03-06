from flask import jsonify

from . import main
from ..models import ValidationError


@main.app_errorhandler(ValidationError)
def validatation_error(e):
    return jsonify(error=e.message), 400


def generic_error_handler(e):
    # TODO: log the error
    headers = []
    error = e.description
    if e.code == 401:
        headers = [('WWW-Authenticate', 'Bearer')]
    elif e.code == 500:
        error = "Internal error"

    return jsonify(error=error),  e.code, headers


for code in range(400, 599):
    main.app_errorhandler(code)(generic_error_handler)
