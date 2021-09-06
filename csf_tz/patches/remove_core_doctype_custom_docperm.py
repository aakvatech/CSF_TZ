from __future__ import unicode_literals
import frappe


def execute():
    frappe.db.sql(
        "DELETE FROM `tabCustom DocPerm` WHERE name != 'a' AND parent in ('DocType', 'Patch Log', 'Module Def', 'Transaction Log')"
    )
