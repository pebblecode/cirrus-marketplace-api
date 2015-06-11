from flask import Blueprint, request

from ..authentication import requires_authentication

main = Blueprint('main', __name__)

main.before_request(requires_authentication)


@main.after_request
def add_cache_control(response):
    if request.method in ['GET', 'HEAD']:
        response.cache_control.max_age = 24 * 60 * 60
    return response


from .views import suppliers, services, users, drafts
from . import errors
