import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    fieds = {
        "Employee": [
            {
                "fieldname": "attachments",
                "label": "Attachments",
                "fieldtype": "Section Break",
                "insert_after": "health_details",
            },
            {
                "fieldname": "files",
                "label": "",
                "fieldtype": "Table",
                "insert_after": "attachments",
                "options": "Document Attachment",
            },
            {
                "depends_on": "eval:doc.salary_mode == 'Bank'",
                "fieldname": "bank_code",
                "label": "Bank Code",
                "fieldtype": "Data",
                "insert_after": "bank_ac_no",
                "translatable": 1,
            },
            {
                "fieldname": "overtime_components",
                "label": "Overtime Components",
                "fieldtype": "Section Break",
                "insert_after": "bank_code",
            },
            {
                "fieldname": "employee_ot_component",
                "label": "Employee OT Component",
                "fieldtype": "Table",
                "insert_after": "overtime_components",
                "options": "Employee OT Component",
            },
            {
                "fieldname": "statutory_details",
                "label": "Statutory Details",
                "fieldtype": "Section Break",
                "insert_after": "grade",
            },
            {
                "fieldname": "pension_fund",
                "label": "Pension Fund",
                "fieldtype": "Select",
                "insert_after": "statutory_details",
                "options": "\nNSSF\nPPF",
                "translatable": 1,
            },
            {
                "fieldname": "pension_fund_number",
                "label": "Pension Fund Number",
                "fieldtype": "Data",
                "insert_after": "pension_fund",
                "translatable": 1,
            },
            {
                "fieldname": "wcf_number",
                "label": "WCF Number",
                "fieldtype": "Data",
                "insert_after": "pension_fund_number",
                "translatable": 1,
            },
            {
                "fieldname": "statutory_details_cb",
                "label": "",
                "fieldtype": "Column Break",
                "insert_after": "wcf_number",
            },
            {
                "fieldname": "tin_number",
                "label": "TIN Number",
                "fieldtype": "Data",
                "insert_after": "statutory_details_cb",
                "translatable": 1,
            },
            {
                "fieldname": "national_identity",
                "label": "National Identity",
                "fieldtype": "Data",
                "insert_after": "tin_number",
                "translatable": 1,
            },
        ],
        "Salary Component": [
            {
                "fieldname": "payware_specifics",
                "label": "Payware Specifics",
                "fieldtype": "Section Break",
                "insert_after": "disabled",
            },
            {
                "fieldname": "create_cash_journal",
                "label": "Create Cash Journal",
                "fieldtype": "Check",
                "insert_after": "payware_specifics",
                "depends_on": "eval:doc.type=='Deduction' ",
            },
            {
                "fieldname": "payware_specifics_cb",
                "label": "",
                "fieldtype": "Column Break",
                "insert_after": "create_cash_journal",
            },
            {
                "fieldname": "based_on_hourly_rate",
                "label": "Based on Hourly Rate",
                "fieldtype": "Check",
                "insert_after": "payware_specifics_cb",
                "depends_on": "eval:doc.type=='Earning' ",
            },
            {
                "fieldname": "hourly_rate",
                "label": "Hourly Rate",
                "fieldtype": "Percent",
                "insert_after": "based_on_hourly_rate",
                "depends_on": "based_on_hourly_rate",
                "description": "Enter percentage % e.g. for 1.5 times enter 150%",
            },
        ],
        "Salary Slip": [
            {
                "fieldname": "overtime_components",
                "label": "Overtime Components",
                "fieldtype": "Section Break",
                "insert_after": "base_hour_rate",
            },
            {
                "fieldname": "salary_slip_ot_component",
                "label": "Salary Slip OT Component",
                "fieldtype": "Table",
                "insert_after": "overtime_components",
                "options": "Salary Slip OT Component",
            },
        ],
    }

    create_custom_fields(fieds, update=True)

