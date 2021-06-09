# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class AVFixture(Document):
    pass


def create_fixture():
    #frappe.db.sql("DELETE FROM `tabAuFix` WHERE name != 'a1' ")
    frappe.db.commit()
    for app_name in frappe.get_installed_apps():
        for fixture_doc in frappe.get_hooks("fixtures", app_name=app_name):
            filters = None
            if isinstance(fixture_doc, dict):
                custom_doctype = fixture_doc.get("doctype")
                filters = fixture_doc.get("filters")
                for filter in filters:
                    for identified_filter in list(filter[2]):
                        required_doctype = identified_filter.split("-")[0]

                        doc = frappe.new_doc("AV Fixture")
                        doc.custom_doctype = custom_doctype
                        doc.identified_filter = identified_filter
                        doc.identified_app = app_name
                        doc.required_doctype = required_doctype
                        doc.insert()


create_fixture()
