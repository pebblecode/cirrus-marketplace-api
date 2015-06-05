#!/usr/bin/env python

"""Import SSP export files into the API

Usage:
        import_suppliers.py <filename> <suppliers> <contacts>

Example:
    ./import_suppliers.py ~/myData/myData.json ~/suppliers.json ~/contacts.json
"""
from __future__ import print_function
import sys
import json
import requests
from datetime import datetime
import io
from docopt import docopt
import re

dummy_address = "10033618144"
dummy_company = "02851586"


def print_progress(counter, start_time):
    if counter % 100 == 0:
        time_delta = datetime.now() - start_time
        print("{} in {} ({}/s)".format(counter,
                                       time_delta,
                                       counter / time_delta.total_seconds()))


def client_string(raw):
    if raw:
        return raw.replace(',', ';')
    return ""


def do_import(filename, supplier_register, contact_register):
    print("Filename: {}".format(filename))

    counter = 0
    start_time = datetime.now()

    with open(filename) as data_file, io.open(supplier_register, 'w', encoding="utf-8") as suppliers, io.open(contact_register, 'w', encoding="utf-8") as contacts:
        json_from_file = json.load(data_file)

        # new output file
        # write headers

        suppliers.write(u'g-cloud-supplier,g-cloud-supplier-contact,name,company,ccs-sourcing-id,clients\n')
        contacts.write(u'g-cloud-supplier-contact,website,contact-name,email,phone-number,address\n')
        for supplier in json_from_file['suppliers']:

                # transform supplier
            suppliers.write(u"{},{},{},{},{},{}\n".format(
                supplier.get('supplierId'),
                supplier.get('supplierId'),
                supplier.get('name').replace(",", " "),
                dummy_company,
                supplier.get('supplierId', ""),
                client_string(supplier.get('clientsString'))
            ))

            contacts.write(u"{},{},{},{},{},{}\n".format(
                supplier.get('supplierId'),
                supplier.get('website', ""),
                supplier.get('contactName', "").replace(",", " "),
                supplier.get('contactEmail', "").replace(",", " "),
                supplier.get('contactPhone', "").replace(",", " "),
                dummy_address
            ))

            counter += 1
            print_progress(counter, start_time)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    do_import(
        filename=arguments['<filename>'],
        supplier_register=arguments['<suppliers>'],
        contact_register=arguments['<contacts>']
    )
