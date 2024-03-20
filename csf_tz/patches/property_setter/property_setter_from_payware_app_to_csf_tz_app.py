import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def execute():
    properties = [
        {
            "doc_type": "Additional Salary",
            "field_name": "overwrite_salary_structure_amount",
            "property": "default",
            "property_type": "Text",
            "value": 0,
            "for_doctype": False,
        },
        {
            "doc_type": "Attendance",
            "field_name": "leave_type",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Attendance",
            "field_name": "status",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Attendance",
            "field_name": "",
            "property": "track_changes",
            "property_type": "Check",
            "value": 1,
            "for_doctype": True,
        },
        {
            "doc_type": "Employee",
            "field_name": "company",
            "property": "in_list_view",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Employee",
            "field_name": "image",
            "property": "hidden",
            "property_type": "Check",
            "value": 0,
            "for_doctype": False,
        },
        {
            "doc_type": "Employee",
            "field_name": "",
            "property": "track_changes",
            "property_type": "Check",
            "value": 1,
            "for_doctype": True,
        },
        {
            "doc_type": "Loan",
            "field_name": "applicant_name",
            "property": "in_list_view",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Loan",
            "field_name": "applicant_name",
            "property": "in_standard_filter",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Loan",
            "field_name": "loan_amount",
            "property": "in_list_view",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Loan",
            "field_name": "status",
            "property": "in_list_view",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Loan",
            "field_name": "",
            "property": "search_fields",
            "property_type": "Data",
            "value": "posting_date, applicant_name",
            "for_doctype": True,
        },
        {
            "doc_type": "Payroll Entry",
            "field_name": "company",
            "property": "in_standard_filter",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Payroll Entry",
            "field_name": "end_date",
            "property": "in_list_view",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Payroll Entry",
            "field_name": "posting_date",
            "property": "in_list_view",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Salary Structure Assignment",
            "field_name": "base",
            "property": "in_list_view",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,

        },
        {
            "doc_type": "Salary Structure Assignment",
            "field_name": "company",
            "property": "in_standard_filter",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Salary Structure",
            "field_name": "deductions",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        },
        {
            "doc_type": "Salary Structure",
            "field_name": "earnings",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": 1,
            "for_doctype": False,
        }
    ]

    for property in properties:
        make_property_setter(
            property.get("doc_type"),
            property.get("field_name"),
            property.get("property"),
            property.get("value"),
            property.get("property_type"),
            for_doctype=property.get("for_doctype"),
            validate_fields_for_doctype=False,
        )

    frappe.db.commit()
