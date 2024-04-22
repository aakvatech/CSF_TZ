import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields = {
        "Salary Structure Assignment": [
            {
                "fetch_from": "employee.designation",
                "fieldname": "designation",
                "fieldtype": "data",
                "insert_after": "employee",
                "label": "Designation",
                "read_only": 1
            },
            {
                
                "fetch_from": "employee.department",
                "fieldname": "department",
                "fieldtype": "data",
                "insert_after": "designation",
                "label": "Department",
                "read_only": 1
            },
            {
                "fetch_from": "employee.grade",
                "fieldname": "grade",
                "fieldtype": "data",
                "insert_after": "department",
                "label": "Grade",
                "read_only": 1
            }
        ]
    }