"""

Usage:
    scripts/make-g-cloud-7-live.py <stage> <api_url> <api_token> <slug> [--dry-run]
"""
import sys
sys.path.insert(0, '.')

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import random
import re

from docopt import docopt
from dmapiclient import DataAPIClient
from dmutils.s3 import S3

DOCUMENT_KEYS = [
    'pricingDocumentURL'
]
FRAMEWORK_SLUG = arguments['<slug>']


def assert_equal(one, two):
    assert one == two, "{} != {}".format(one, two)


def find_suppliers_on_framework(client, framework_slug):
    return (
        supplier for supplier in client.find_framework_suppliers(FRAMEWORK_SLUG)['supplierFrameworks']
        if supplier['onFramework']
    )


def find_submitted_draft_services(client, supplier, framework_slug):
    return (
        draft_service for draft_service in
        client.find_draft_services(supplier['supplierId'], framework=framework_slug)['services']
        if draft_service['status'] == 'submitted' and not draft_service.get('serviceId')
    )


def make_draft_service_live(client, copy_document, draft_service, framework_slug, dry_run):
    print("  > Migrating draft {} - {}".format(draft_service['id'], draft_service['serviceName']))
    if dry_run:
        service_id = random.randint(1000, 10000)
        print("    > generating random test service ID: {}".format(service_id))
    else:
        services = client.publish_draft_service(draft_service['id'], 'make-inoket-1-live script')
        service_id = services['services']['id']
        print("    > draft service published - new service ID {}".format(service_id))

    document_updates = {}
    for document_key in DOCUMENT_KEYS:
        if document_key not in draft_service:
            print("    > Skipping {}".format(document_key))
        else:
            parsed_document = parse_document_url(draft_service[document_key], framework_slug)
            assert_equal(str(parsed_document['supplier_id']), str(draft_service['supplierId']))
            assert_equal(str(parsed_document['draft_id']), str(draft_service['id']))

            draft_document_path = get_draft_document_path(parsed_document, framework_slug)
            live_document_path = get_live_document_path(parsed_document, framework_slug, service_id)

            copy_document(draft_document_path, live_document_path)
            document_updates[document_key] = get_live_asset_url(live_document_path)

    if dry_run:
        print("    > not updating document URLs {}".format(document_updates))
    else:
        client.update_service(service_id, document_updates, 'Moving documents to live bucket')
        print("    > document URLs updated")


if __name__ == '__main__':
    arguments = docopt(__doc__)

    STAGE = arguments['<stage>']
    api_url = arguments['<api_url>']

    client = DataAPIClient(api_url, arguments['<api_token>'])
    DRY_RUN = arguments['--dry-run']

    suppliers = find_suppliers_on_framework(client, FRAMEWORK_SLUG)

    for supplier in suppliers:
        print("Migrating drafts for supplier {} - {}".format(supplier['supplierId'], supplier['supplierName']))
        draft_services = find_submitted_draft_services(client, supplier, FRAMEWORK_SLUG)

        for draft_service in draft_services:
            make_draft_service_live(client, copy_document, draft_service, FRAMEWORK_SLUG, DRY_RUN)