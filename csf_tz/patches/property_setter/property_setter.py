import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def execute():
    properties = [
            {
                "doc_type": "Supplier",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "tax_id",
                "property": "label",
                "property_type": "Data",
                "value": "TIN"
            },
            {
                "doc_type": "Supplier",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "read_only_onload",
                "property_type": "Check",
                "value": ""
            },
            {
                "doc_type": "Supplier",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "tax_id",
                "property": "bold",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Journal Entry Account",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "accounting_dimensions_section",
                "property": "collapsible",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Sales Invoice",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "search_fields",
                "property_type": "Data",
                "value": "posting_date, due_date, customer, base_grand_total, outstanding_amount"
            },
            {
                "doc_type": "Sales Invoice Item",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "cost_center",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Sales Invoice Item",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "item_code",
                "property": "columns",
                "property_type": "Int",
                "value": "3"
            },
            {
                "doc_type": "Sales Invoice Item",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "qty",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doc_type": "Sales Invoice Item",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "warehouse",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Sales Invoice Item",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "batch_no",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Sales Invoice Item",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "cost_center",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doc_type": "Vehicle Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "license_plate",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Vehicle Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "employee",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": "license_plate.driver"
            },
            {
                "doc_type": "Vehicle Service",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "service_item",
                "property": "options",
                "property_type": "Text",
                "value": "NOT SELECTED\nBrake Oil\nBrake Pad\nClutch Plate\nEngine Oil\nOil Change\nWheels"
            },
            {
                "doc_type": "Vehicle Service",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "service_item",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Vehicle Service",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "type",
                "property": "options",
                "property_type": "Text",
                "value": "Repair\nInspection\nService\nChange"
            },
            {
                "doc_type": "Vehicle Service",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "frequency",
                "property": "options",
                "property_type": "Text",
                "value": "NOT SELECTED\nMileage\nMonthly\nQuarterly\nHalf Yearly\nYearly"
            },
            {
                "doc_type": "Vehicle Service",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "frequency",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Vehicle Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "quick_entry",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Vehicle Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "employee",
                "property": "fetch_if_empty",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Account",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "search_fields",
                "property_type": "Data",
                "value": "account_number, root_type, account_type"
            },
            {
                "doc_type": "Vehicle Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Vehicle Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "date",
                "property": "default",
                "property_type": "Text",
                "value": "Today"
            },
            {
                "doc_type": "Vehicle Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "odometer",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Purchase Invoice Item",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "cost_center",
                "property": "default",
                "property_type": "Text",
                "value": ""
            },
            {
                "doc_type": "Journal Entry",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "accounts",
                "property": "allow_bulk_edit",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Journal Entry",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "total_debit",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Journal Entry",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "total_amount",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Report",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "javascript",
                "property": "depends_on",
                "property_type": "Text",
                "value": ""
            },
            {
                "doc_type": "Journal Entry Account",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "reference_name",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Journal Entry Account",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "account",
                "property": "width",
                "property_type": "Data",
                "value": ""
            },
            {
                "doc_type": "Sales Invoice Item",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "item_tax_template",
                "property": "fetch_if_empty",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Sales Invoice Item",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "item_tax_template",
                "property": "default",
                "property_type": "Text",
                "value": ""
            },
            {
                "doc_type": "Sales Invoice",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "letter_head",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": "company.default_letter_head"
            },
            {
                "doc_type": "Sales Invoice",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "letter_head",
                "property": "fetch_if_empty",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Purchase Order",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "letter_head",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": ""
            },
            {
                "doc_type": "Item Price",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "brand",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Item Price",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "price_list",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Delivery Note",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "items",
                "property": "allow_bulk_edit",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Item Price",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "valid_from",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Payment Entry",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "letter_head",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": "company.default_letter_head"
            },
            {
                "doc_type": "Piecework Type",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "search_fields",
                "property_type": "Data",
                "value": "task_name"
            },
            {
                "doc_type": "Document Attachment",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "attachment",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Operation",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "image_field",
                "property_type": "Data",
                "value": "image"
            },
            {
                "doc_type": "Payment Entry",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "payment_accounts_section",
                "property": "collapsible",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Payment Entry",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "section_break_12",
                "property": "collapsible",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Bank Reconciliation Detail",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "payment_entry",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doc_type": "Bank Reconciliation Detail",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "posting_date",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doc_type": "Bank Reconciliation Detail",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "posting_date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Customer",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "tax_id",
                "property": "label",
                "property_type": "Data",
                "value": "TIN"
            },
            {
                "doc_type": "Payment Entry Reference",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "due_date",
                "property": "width",
                "property_type": "Data",
                "value": "23"
            },
            {
                "doc_type": "Payment Entry Reference",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "due_date",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doc_type": "Payment Entry Reference",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "reference_doctype",
                "property": "columns",
                "property_type": "Int",
                "value": "0"
            },
            {
                "doc_type": "Payment Entry Reference",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "reference_name",
                "property": "columns",
                "property_type": "Int",
                "value": "3"
            },
            {
                "doc_type": "Payment Entry Reference",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "reference_doctype",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Payment Reconciliation Payment",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "posting_date",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doc_type": "Payment Reconciliation Payment",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "posting_date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Sales Invoice",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "is_pos",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Sales Invoice",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "posting_date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Sales Invoice",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "pos_profile",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Stock Entry",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "from_warehouse",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": "repack_template.default_warehouse"
            },
            {
                "doc_type": "Student Applicant",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "application_status",
                "property": "options",
                "property_type": "Text",
                "value": "Applied\nApproved\nRejected\nAdmitted\nAwaiting Registration Fees"
            },
            {
                "doc_type": "Student Applicant",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "application_status",
                "property": "read_only",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doc_type": "Payment Schedule",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "payment_amount",
                "property": "options",
                "property_type": "Small Text",
                "value": "Company:company:default_currency"
            },
            {
                "doc_type": "Journal Entry Account",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "party",
                "property": "columns",
                "property_type": "Int",
                "value": "2"
            },
            {
                "doc_type": "Journal Entry Account",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "party_type",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doc_type": "Budget",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "budget_against",
                "property": "options",
                "property_type": "Text",
                "value": "\nCost Center\nProject\nDepartment\nVehicle\nHealthcare Practitioner\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit"
            },
            {
                "doc_type": "Customer",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "search_fields",
                "property_type": "Data",
                "value": "customer_name,customer_group,territory, mobile_no"
            },
            {
                "doc_type": "Energy Point Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Route History",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Notification Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Scheduled Job Log",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Healthcare Service Order",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Healthcare Insurance Claim",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Comment",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Workflow Action",
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doc_type": "Sales Invoice",
                "doctype": "Property Setter",
                "doctype_or_field": "DocField",
                "field_name": "loyalty_points_redemption",
                "property": "depends_on",
                "property_type": "Data",
                "value": "eval: !in_list(frappe.user_roles, \"Healthcare Receptionist\")"
            },
            {
                "doctype_or_field": "DocField",
                "doc_type": "Sales Invoice Item",
                "field_name": "discount_percentage",
                "property": "precision",
                "property_type": "Select",
                "value": "6",
                "doctype": "Property Setter"
            },
            {
                "doctype_or_field": "DocField",
                "doc_type": "Purchase Invoice Item",
                "field_name": "discount_percentage",
                "property": "precision",
                "property_type": "Select",
                "value": "6",
                "doctype": "Property Setter"
            }
    ]
    for property in properties:
        make_property_setter(
            property.get("doctype"),
            property.get("fieldname"),
            property.get("property"),
            property.get("value"),
            property.get("property_type"),
            for_doctype=False,
            validate_fields_for_doctype=False
    )

frappe.db.commit()          