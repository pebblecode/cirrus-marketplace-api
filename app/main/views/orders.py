from .. import main
from ...utils import get_json_from_request
from ...validation import get_validator
from ...models import Order, Supplier, Service, ContactInformation
from ... import db
from flask import abort, current_app, jsonify
from sqlalchemy.exc import IntegrityError, DataError
from inoket.email import send_email
from collections import namedtuple
from jinja2 import Template
from datetime import date

EmailInfo = namedtuple(
        'EmailInfo', ['from_address', 'from_name', 'subject', 'body_text', 'body_html', 'tags'])


@main.route('/orders', methods=['POST'])
def create_order():
    body = get_json_from_request()
    (is_valid, errors) = validate_order_request(body)
    if not is_valid:
        error_messages = [error_message(e) for e in errors]
        abort(400, error_messages)

    order = Order.from_json(body)

    try:
        db.session.add(order)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        log_message = "Database Error: {0}".format(e)
        current_app.logger.error(log_message)
        return jsonify(message=log_message), 400

    try:
        (contact, supplier, service) = db.session\
                .query(ContactInformation, Supplier, Service)\
                .filter(ContactInformation.supplier_id == Supplier.supplier_id)\
                .filter(Service.supplier_id == Supplier.supplier_id)\
                .filter(Service.service_id == order.service_id)\
                .filter(ContactInformation.email is not None)\
                .one()
    except Exception as e:
        log_message = "Failed to look up supplier for service id: {0}, Error: {1}".format(order.service_id, e)
        current_app.logger.error(log_message)
        return jsonify(log_message), 400

    order_email_info ={
            'purchase_order_number': order.purchase_order_number,
            'amount_in_pennies': order.amount_in_pennies
            }
    buyer_email_info = {
            'email': body.get('email'),
            'name': body.get('name', '')
            }
    supplier_email_info = {
            'name': supplier.name,
            'email': contact.email,
            'phone_number': contact.phone_number,
            }
    service_email_info = {
            'name': service.data.get('serviceName', ''),
            'id': service.service_id
            }

    send_emails(order_email_info, buyer_email_info, supplier_email_info, service_email_info)

    response_body = {
            'id': order.id,
            'order_state': order.order_state
            }

    return jsonify(response_body), 201


def validate_order_request(body):
    validator = get_validator('orders-create')
    errors = [e for e in validator.iter_errors(body)]
    if len(errors) > 0:
        return False, errors
    return True, []


def error_message(validation_error):
    if validation_error.path:
        return str.join(":", (validation_error.path[0], validation_error.message))
    else:
        return validation_error.message


def send_emails(order, buyer, supplier, service):
    today = date.today().strftime("%d/%m/%Y")
    def send(buyer_or_supplier, to):
        info = get_email_info(
                buyer_or_supplier,
                order,
                buyer,
                supplier,
                service,
                today)
        try:
            send_email(from_address=info.from_address, to_addresses=[to], subject=info.subject, body_text=info.body_text, from_email_name=info.from_name, tags=info.tags, body_html=info.body_html)
            # send_email(info.from_address, to, info.subject, info.body_text)
        except Exception as e:
            current_app.logger.error(
                    "Sending email to [{0}] for order_id: [{1}]. Details: {2}"
                    .format(buyer_or_supplier.upper(), order.id, e))

    send("buyer", buyer.get('email'))
    send("supplier", supplier.get('email'))


def get_email_info(buyer_or_supplier, order, buyer, supplier, service, today_date):
    if buyer_or_supplier == 'buyer':
        html_body = format_buyer_html_body(buyer, supplier, service, order, today_date)
        text_body = format_buyer_text_body(buyer, supplier, service, order, today_date)
        subject = "Purchase Order No: {0} Sent".format(order.get('purchase_order_number'))
        info = EmailInfo(
                from_address=current_app.config.get('ORDER_BUYER_FROM_EMAIL'),
                from_name=current_app.config.get('ORDER_BUYER_FROM_NAME'),
                subject=subject,
                body_text=text_body,
                body_html=html_body,
                tags=["buyer", "buyer_orders", "orders"]
                )
        return info
    else:
        return EmailInfo(
                from_address=current_app.config.get('ORDER_SUPPLIER_FROM_EMAIL'),
                from_name=current_app.config.get('ORDER_SUPPLIER_FROM_NAME'),
                subject="Purchase Order Received",
                body_text="A request to buy a service has been received.",
                body_html='',
                tags=["supplier", "supplier_orders", "orders"]
                )

def format_buyer_text_body(*args):
    return "Your order has been sent."

def format_buyer_html_body(buyer, supplier, service, order, today_date):
    template = Template(current_app.config['email_templates']['buyer_order_received'])
    return template.render(
            buyer=buyer,
            supplier=supplier,
            service=service,
            purchase_order_number=order.get('purchase_order_number'),
            amount=str(order.get('amount_in_pennies') / 100.0),
            date=today_date)
