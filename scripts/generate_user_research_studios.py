#!/usr/bin/env python
"""
Create a number of user research studios.

Usage:
    generate_user_research_studios.py <num_studios> [--filename=<filename>]
"""
import sys
import json
import time

from docopt import docopt


def generate_user_research_studio(parameter):
    return {
        "labAccessibility": "Nanaimo bar there should plaid flannel back bacon for eavestroughs eats of all igloo on this mickey lacrosse stagette.",  # noqa
        "labAddressBuilding": "123 Fake Street",
        "labAddressPostcode": "C4N4D4",
        "labAddressTown": "Toronto",
        "labBabyChanging": False,
        "labCarPark": "The fishing have canned moose gasbar in goaltender Canuck freezie.",
        "labDesktopStreaming": "No",
        "labDeviceStreaming": "No",
        "labEyeTracking": "No",
        "labHosting": "Yes – included as standard",
        "labPriceMin": "100",
        "labPublicTransport": "The igloo have mickey garburator in goaltender loonie turfed out.",
        "labSize": "Canuck for lacrosse eats of all hoser on this two-four keener bacon",
        "labStreaming": "No",
        "labTechAssistance": "No",
        "labTimeMin": "4 hours",
        "labToilets": False,
        "labViewingArea": "Yes – included as standard",
        "labWaitingArea": "Yes – included as standard",
        "labWiFi": True,
        "serviceName": "Studio {}".format(parameter),
        "supplierId": 11111,
        "lot": "user-research-studios",
        "frameworkSlug": "digital-outcomes-and-specialists"
      }


def generate_user_research_studios(num_studios, output):
    # some error if number of labs is 0
    studios = {'services': []}
    timestamp = int(time.time())

    for i in range(num_studios):
        studios['services'].append(generate_user_research_studio(timestamp + i))

    json.dump(studios, output, indent=2, separators=(',', ': '))


if __name__ == '__main__':
    arguments = docopt(__doc__)

    num_studios = int(arguments['<num_studios>'])
    output = open(arguments.get('--filename'), 'w+') if arguments.get('--filename') else sys.stdout

    generate_user_research_studios(num_studios, output)
