from flask import jsonify, abort, request, current_app
from datetime import datetime
from ...models import AuditEvent
from sqlalchemy import asc, Date, cast
from sqlalchemy.exc import IntegrityError
from ...utils import pagination_links
from .. import main
from ... import db
from dmutils.audit import AuditTypes
from ...validation import is_valid_date
from ...service_utils import validate_and_return_updater_request


@main.route('/audit-events', methods=['GET'])
def list_audits():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(400, "Invalid page argument")

    audits = AuditEvent.query.order_by(
        asc(AuditEvent.created_at)
    )

    audit_date = request.args.get('audit-date', None)
    if audit_date:
        if is_valid_date(audit_date):
            audits = audits.filter(
                cast(AuditEvent.created_at, Date) == audit_date
            )
        else:
            abort(400, 'invalid audit date supplied')

    if request.args.get('audit-type'):
        if AuditTypes.is_valid_audit_type(request.args.get('audit-type')):
            audits = audits.filter(
                AuditEvent.type == request.args.get('audit-type')
            )
        else:
            abort(400, "Invalid audit type")

    audits = audits.paginate(
        page=page,
        per_page=current_app.config['DM_API_SERVICES_PAGE_SIZE'],
    )

    return jsonify(
        auditEvents=[audit.serialize() for audit in audits.items],
        links=pagination_links(
            audits,
            '.list_audits',
            request.args
        )
    )


@main.route('/audit-events/<string:audit_id>/acknowledge', methods=['POST'])
def acknowledge_audit(audit_id):
    try:
        audit_id = int(audit_id)
    except ValueError:
        abort(400, "Invalid audit id argument")

    updater_json = validate_and_return_updater_request()

    audit_event = AuditEvent.query.filter(
        AuditEvent.id == audit_id
    ).first()

    if audit_event is None:
        abort(404, "No audit event with this id")

    audit_event.acknowledged = True
    audit_event.acknowledged_at = datetime.now()
    audit_event.acknowledged_by = updater_json['updated_by']

    try:
        db.session.add(audit_event)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        abort(400, e.orig)

    return jsonify(auditEvents=audit_event.serialize()), 200
