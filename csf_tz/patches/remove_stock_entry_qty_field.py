from __future__ import unicode_literals
import frappe

def execute():
    if frappe.db.exists("Custom Field", "Stock Entry-qty"):
        frappe.delete_doc("Custom Field", "Stock Entry-qty", force=True)
    if 'qty' in frappe.db.get_table_columns("Stock Entry"):
        frappe.db.sql_ddl("alter table `tabStock Entry` drop column qty")
