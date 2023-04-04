import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    def execute():
        fields={
        "Customer": [
            {
                "fieldname": "default_authotp_method",
                "fieldtype": "Link",
                "insert_after": "is_authotp_applied",
                "label": "Default AuthOTP Method",
                "name": "Customer-default_authotp_method",
                "options": "OTP Register"
            },
            {
                "fieldname": "is_authotp_applied",
                "fieldtype": "Check",
                "insert_after": "customer_group",
                "label": "Is AuthOTP Applied",
                "name": "Customer-is_authotp_applied",
            },
            {
                "fieldname": "authotp_validated",
                "fieldtype": "Check",
                "insert_after": "column_break_sn02w",
                "label": "AuthOTP Validated",
                "name": "Sales Invoice-authotp_validated"
            },
        ],
        "Sales Invoice":[
            {
                "fieldname": "column_break_sn02w",
                "fieldtype": "Column Break",
                "insert_after": "authotp_method",
                "name": "Sales Invoice-column_break_sn02w"
            },
            {
                "fieldname": "authotp_method",
                "fieldtype": "Link",
                "insert_after": "authotp_method",
                "name": "Sales Invoice-authotp_method",
                "options": "OTP Register",
                "label": "AuthOTP Method"
            },
            {
                "fieldname": "authotp",
                "fieldtype": "Section Break",
                "insert_after": "amended_from",
                "name": "Sales Invoice-authotp",
                "label": "AuthOTP"
            },
        ]
    }
create_custom_fields(fields, update=True)


