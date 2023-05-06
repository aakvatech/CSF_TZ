import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields={
            "Student":[
                {
                    "fieldname": "bank",
                    "fieldtype": "Select",
                    "insert_after": "student_applicant",
                    "is_system_generated": 1,
                    "label": "Bank",
                    "options": "\n NMB Bank",
                    "translatable": 1
                },
            ],
            "Student Applicant":[
                {
                    "allow_on_submit": 1,
                    "fieldname": "student_applicant_fee",
                    "fieldtype": "Data",
                    "insert_after": "paid",
                    "is_system_generated": 1,
                    "label": "Student Applicant Fee",
                    "read_only": 1,
                    "translatable": 1
                },
                {
                    "allow_on_submit": 1,
                    "fieldname": "bank_reference",
                    "fieldtype": "Data",
                    "insert_after": "student_applicant_fee",
                    "is_system_generated": 1,
                    "label": "Bank Reference",
                    "read_only": 1,
                    "translatable": 1
                },
                {
                    "fieldname": "fee_structure",
                    "fieldtype": "Link",
                    "insert_after": "application_date",
                    "is_system_generated": 1,
                    "label": "Fee Structure",
                    "options": "Fee Structure",
                    "reqd": 1
                },
                {
                    "fieldname": "program_enrollment",
                    "fieldtype": "Link",
                    "insert_after": "fee_structure",
                    "is_system_generated": 1,
                    "label": "Program Enrollment",
                    "options": "Program Enrollment"
                },
            ],
            "Program Fee":[
                {
                    "fetch_from": "fee_structure.default_fee_category",
                    "fieldname": "default_fee_category",
                    "fieldtype": "Link",
                    "in_list_view": 1,
                    "insert_after": "due_date",
                    "is_system_generated": 1,
                    "label": "Default Fee Category",
                    "options": "Fee Category"
                },
            ],
            "Program":[
                {
                    "fieldname": "fees",
                    "fieldtype": "Section Break",
                    "insert_after": "courses",
                    "is_system_generated": 1,
                    "label": "Fees"
                },
            ],
            "Fees":[
                {
                    "allow_on_submit": 1,
                    "fieldname": "callback_token",
                    "fieldtype": "Data",
                    "insert_after": "healthcare_practitioner",
                    "is_system_generated": 1,
                    "label": "Callback Token",
                    "read_only": 1,
                    "translatable": 1
                },
                {
                    "allow_on_submit": 1,
                    "fieldname": "bank_reference",
                    "fieldtype": "Data",
                    "insert_after": "send_payment_request",
                    "is_system_generated": 1,
                    "label": "Bank Reference",
                    "read_only": 1,
                    "translatable": 1
                },
                {
                    "fetch_from": "company.abbr",
                    "fieldname": "abbr",
                    "fieldtype": "Data",
                    "insert_after": "company",
                    "is_system_generated": 1,
                    "label": "Abbr",
                    "read_only": 1,
                    "translatable": 1
                },
                {
                    "fieldname": "from_date",
                    "fieldtype": "Date",
                    "insert_after": "vehicle",
                    "is_system_generated": 1,
                    "label": "From Date"
                },
                {
                    "fieldname": "to_date",
                    "fieldtype": "Date",
                    "insert_after": "from_date",
                    "is_system_generated": 1,
                    "label": "To Date"
                },
            ],
            "Fee Structure":[
                {
                    "allow_on_submit": 1,
                    "fieldname": "default_fee_category",
                    "fieldtype": "Link",
                    "insert_after": "student_category",
                    "is_system_generated": 1,
                    "label": "Default Fee Category",
                    "options": "Fee Category"
                },
            ],
            "Campany":[
                    {
                "default": "0",
                "fieldname": "send_fee_details_to_bank",
                "fieldtype": "Check",
                "insert_after": "education_section",
                "label": "Send Fee details to Bank",
            },
            {
                "fieldname": "fee_bank_account",
                "fieldtype": "Link",
                "insert_after": "send_fee_details_to_bank",
                "label": "Fee Bank Account",
                "options": "Account"
            },
            {
                "fieldname": "student_applicant_fees_revenue_account",
                "fieldtype": "Link",
                "insert_after": "fee_bank_account",
                "label": "Student Applicant Fees Revenue Account",
                "options": "Account"
            },
            {
                "fieldname": "column_break_60",
                "fieldtype": "Column Break",
                "insert_after": "student_applicant_fees_revenue_account",
                "label": "",
            },
            {
                "depends_on": "send_fee_details_to_bank",
                "fieldname": "nmb_series",
                "fieldtype": "Data",
                "insert_after": "column_break_60",
                "label": "NMB Series",
                "translatable": 1
            },
            {
                "depends_on": "send_fee_details_to_bank",
                "fieldname": "nmb_username",
                "fieldtype": "Data",
                "insert_after": "nmb_series",
                "label": "NMB User Name",
                "translatable": 1
            },
            {
                "depends_on": "send_fee_details_to_bank",
                "fieldname": "nmb_password",
                "fieldtype": "Password",
                "insert_after": "nmb_username",
                "label": "NMB Password",
            },
            {
                "depends_on": "send_fee_details_to_bank",
                "fieldname": "nmb_url",
                "fieldtype": "Data",
                "insert_after": "nmb_password",
                "label": "NMb URL",
                "translatable": 1
            },
        ]           

    }
    create_custom_fields(fields, update=True)                