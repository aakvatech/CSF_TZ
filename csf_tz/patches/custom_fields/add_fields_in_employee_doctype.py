import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields_to_delete = ["employee_country_code", "employee_country"]
    
    # Delete existing custom fields if they exist
    for field_name in fields_to_delete:
        custom_field = frappe.db.exists("Custom Field", {"fieldname": field_name, "dt": "Employee"})
        if custom_field:
            frappe.delete_doc("Custom Field", custom_field)

    # Define new custom fields
    fields = {
        "Employee": [
            {
                "fieldname": "bank_account_name",
                "fieldtype": "Data",
                "label": "Bank Account Name",
                "translatable": 1,
            },
            {
                "fieldname": "employee_country",
                "fieldtype": "Link",
                "options": "Country",
                "label": "Employee Country",
            },
            {
                "fieldname": "employee_country_code",
                "fieldtype": "Data",
                "fetch_from": "employee_country.code",
                "label": "Employee Country Code",
                "translatable": 1,
            },
            {
                "fieldname": "bank_country",
                "fieldtype": "Link",
                "options": "Country",
                "label": "Bank Country",
                "insert_after": "bank_code",
            },
            {
                "fieldname": "bank_country_code",
                "fieldtype": "Data",
                "fetch_from": "bank_country.code",
                "label": "Bank Country Code",
                "read_only": 1,
                "translatable": 1,
            },
            {
                "fieldname": "beneficiary_bank_bic",
                "fieldtype": "Data",
                "label": "Beneficiary Bank BIC",
                "translatable": 1,
            },
        ]
    }

    # Create the new custom fields
    create_custom_fields(fields, update=True)
