# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AVFixture(Document):
    def validate():
        frappe.msgprint("validate")
        for identified_app in frappe.get_installed_apps():
            for hook in frappe.get_hooks("fixtures", app_name=identified_app):
                filters = None
                if isinstance(hook, dict):
                    custom_doctype = hook.get("doctype")
                    filters = hook.get("filters")
                    for filter in filters:
                        for identified_filter in list(filter[2]):
                            required_doctype = identified_filter.split("-")[0]

                        frappe.db.new_doc({
                            "doctype": "Av Fixture",
                            "custom_doctype": custom_doctype,
                            "identified_filter": identified_filter,
                            "identified_app": identified_app,
                            "required_doctype": required_doctype
                            }).insert()
    validate()                    
                        
"""
av_fixture = frappe.new_doc("AV Fixture")

av_fixture.identified_app=identified_app
av_fixture.custom_doctype=custom_doctype
av_fixture.identified_filter=identified_filter
av_fixture.required_doctype=required_doctype
frappe.db.commit()
av_fixture.insert()
    """

    #create_fixture()
    
#if not frappe.db.exist("AV Fixture", doc.name):
#return 
