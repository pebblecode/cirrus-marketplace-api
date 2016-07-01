from .. import main
from ...utils import get_json_from_request
from ...validation import get_validator
from ...models import Order, Supplier, Service, ContactInformation
from ... import db
from flask import abort, current_app, jsonify
from sqlalchemy.exc import IntegrityError, DataError
from cirrus.email import send_email
from collections import namedtuple

EmailInfo = namedtuple(
        'EmailInfo', ['from_address', 'from_name', 'subject', 'body', 'tags'])


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
        contact = db.session\
                .query(ContactInformation)\
                .join(Supplier, Service)\
                .filter(Service.service_id == order.service_id)\
                .filter(ContactInformation.email is not None)\
                .first()
    except Exception as e:
        log_message = "Failed to look up supplier for service id: {0}, Error: {1}".format(order.service_id, e)
        current_app.logger.error(log_message)
        return jsonify(log_message), 400

    send_emails(order, body.get('email'), contact.email)

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


def send_emails(order, buyer_email, supplier_email):
    def send(buyer_or_supplier, to):
        info = get_email_info(buyer_or_supplier)
        try:
            send_email(
                    [to],
                    info.body,
                    info.subject,
                    info.from_address,
                    info.from_name,
                    info.tags)
        except Exception as e:
            current_app.logger.error(
                    "Sending email to [{0}] for order_id: [{1}]. Details: {2}"
                    .format(buyer_or_supplier.upper(), order.id, e))

    send("buyer", buyer_email)
    send("supplier", supplier_email)


def get_email_info(buyer_or_supplier):
    if buyer_or_supplier == 'buyer':
        return EmailInfo(
                from_address=current_app.config.get('ORDER_BUYER_FROM_EMAIL'),
                from_name=current_app.config.get('ORDER_BUYER_FROM_NAME'),
                subject="Purchase Order Sent",
                body="Your order has been sent.",
                tags=["buyer", "buyer_orders", "orders"])
    else:
        return EmailInfo(
                from_address=current_app.config.get('ORDER_SUPPLIER_FROM_EMAIL'),
                from_name=current_app.config.get('ORDER_SUPPLIER_FROM_NAME'),
                subject="Purchase Order Received",
                body="A request to buy a service has been received.",
                tags=["supplier", "supplier_orders", "orders"]
        )
