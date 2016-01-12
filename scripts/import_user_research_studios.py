#!/usr/bin/env python
"""
Import user research studios stored as json data in a file

Usage:
    import_user_research_studios.py <data_api_url> <data_api_token> <filename> [--user=<user>]
"""
import json

from docopt import docopt
from dmapiclient import DataAPIClient


def import_user_research_studios(data_api_client, user, studios):
    for studio in studios:
        studio = data_api_client.create_new_draft_service(
            framework_slug=studio['frameworkSlug'],
            lot=studio['lot'],
            supplier_id=studio['supplierId'],
            data=studio,
            user=user)

        data_api_client.complete_draft_service(
            draft_id=studio['services']['id'],
            user=user)

        service = data_api_client.publish_draft_service(
            draft_id=studio['services']['id'],
            user=user)

        print('{} -> id={}, draft_id={}'.format(
                service['services']['serviceName'],
                service['services']['id'],
                studio['services']['id']))


if __name__ == '__main__':
    arguments = docopt(__doc__)

    data_api_client = DataAPIClient(arguments['<data_api_url>'], arguments['<data_api_token>'])
    user = arguments.get('--user') if arguments.get('--user') else 'paul@paul.paul'

    with open(arguments['<filename>']) as data_file:
        data = json.load(data_file)

    import_user_research_studios(data_api_client, user, data['services'])
