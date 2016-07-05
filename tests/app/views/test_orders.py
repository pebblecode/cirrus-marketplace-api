from ..helpers import BaseApplicationTest
from flask import json, jsonify, request, current_app
from nose.tools import assert_equal, assert_in, assert_false
from app.models import Supplier, Service, Order
from app import db, create_app
import mock


@mock.patch('app.main.views.orders.send_email')
class TestPostOrder(BaseApplicationTest):
    endpoint = '/orders'
    method = 'post'

    def setup(self):
        super(TestPostOrder, self).setup()

    def _call_valid(self):
            self.setup_dummy_suppliers(2)
            sid = '10000000001'
            self.setup_dummy_service(service_id=sid)
            db.session.commit()
            return self.client.post(
                self.endpoint,
                data=json.dumps({
                    'service_id': sid,
                    'po_number': "1821",
                    'email': 'test@example.com',
                    'amount_in_pennies': 12812112
                    }),
                content_type='application/json'
                )

    def test_validation_error_causes_bad_request(self, email):
        with self.app.app_context():
            response = self.client.post(
                    self.endpoint,
                    data=json.dumps({
                        'service_id': -20
                        }),
                    content_type='application/json')
            assert_equal(400, response.status_code)
            data = json.loads(response.get_data())
            errors = data['error']
            service_id_error = ""
            field_missing_errors = []
            for e in errors:
                if 'service_id' in e:
                    service_id_error = e
                else:
                    field_missing_errors.append(e)
            assert_in(u'-20', service_id_error)
            for e in field_missing_errors:
                assert_in(u'required', e)

    def test_can_post_a_valid_order(self, email):
        with self.app.app_context():
            response = self._call_valid()
            assert_equal(response.status_code, 201)

    def test_sends_no_email_after_invalid_order(self, email):
        with self.app.app_context():
            self.client.post(
                    self.endpoint,
                    data='',
                    content_type='application/json'
                    )
            assert_false(email.called)

    def test_sends_two_emails(self, email):
        with self.app.app_context():
            response = self._call_valid()
            assert_equal(response.status_code, 201)
            assert(True, email.called)
            assert_equal(2, len(email.call_args_list))

            def subject(**kwargs):
                sub = kwargs.get('subject')
                return sub

            subjects = str.join(
                    "",
                    reduce(
                        lambda x, y: subject(**x[1]) + subject(**y[1]),
                        email.call_args_list))
            assert_in('received', subjects.lower())
            assert_in('sent', subjects.lower())
