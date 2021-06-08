# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class AVFixture(Document):
    def create_fixture():
        #frappe.msgprint("validate")
        for identified_app in frappe.get_installed_apps():
            for hook in frappe.get_hooks("fixtures", app_name=identified_app):
                filters = None
                if isinstance(hook, dict):
                    custom_doctype = hook.get("doctype")
                    filters = hook.get("filters")
                    for filter in filters:
                        for identified_filter in list(filter[2]):
                            required_doctype = identified_filter.split("-")[0]
                            
                            doc=frappe.new_doc("AV Fixture")
                            doc.custom_doctype = custom_doctype
                            doc.identified_filter = identified_filter
                            doc.identified_app = identified_app
                            doc.required_doctype = required_doctype
                            doc.insert()
    create_fixture()

