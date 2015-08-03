from flask import render_template, jsonify, current_app
from .. import main

from dmutils.email import send_email, MandrillException


@main.route('/send-email', methods=["POST"])
def send_invite_user():

    url = None
    email_address = None
    name = None
    supplier_name = None
    supplier_id = None

    email_body = render_template(
        "emails/invite_user_email.html",
        url=url,
        user=name,
        supplier=supplier_name)

    try:
        send_email(
            email_address,
            email_body,
            current_app.config['DM_MANDRILL_API_KEY'],
            current_app.config['INVITE_EMAIL_SUBJECT'],
            current_app.config['INVITE_EMAIL_FROM'],
            current_app.config['INVITE_EMAIL_NAME'],
            ["user-invite"]
        )
    except MandrillException as e:
        current_app.logger.error(
            "Invitation email failed to send error {} to {} suppluer {} supplier id {} ".format(
                e.message,
                email_address,
                supplier_name,
                supplier_id)
        )
        jsonify(message="Failed to send user invite reset"), 503

    return jsonify(message="Success"), 200
