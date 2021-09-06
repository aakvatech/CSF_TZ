# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class CSFAPIResponseLog(Document):
    pass


def add_log(
    request_type,
    request_url,
    request_header=None,
    request_body=None,
    response_data=None,
    status_code=None,
):
    doc = frappe.new_doc("CSF API Response Log")
    doc.request_type = str(request_type)
    doc.request_url = str(request_url)
    doc.request_header = str(request_header) or ""
    doc.request_body = str(request_body) or ""
    doc.response_data = str(response_data) or ""
    doc.user_id = frappe.session.user
    doc.status_code = status_code or ""
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return doc.name
