import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def execute():
    properties = [
            {
                "doctype": "Supplier",
                "field_name": "tax_id",
                "property": "label",
                "property_type": "Data",
                "value": "TIN"
            },
            {
                "doctype": "Supplier",
                "property": "read_only_onload",
                "property_type": "Check",
                "value": ""
            },
            {
                "doctype": "Supplier",
                "field_name": "tax_id",
                "property": "bold",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Journal Entry Account",
                "field_name": "accounting_dimensions_section",
                "property": "collapsible",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Sales Invoice",
                "property": "search_fields",
                "property_type": "Data",
                "value": "posting_date, due_date, customer, base_grand_total, outstanding_amount"
            },
            {
                "doctype": "Sales Invoice Item",
                "field_name": "cost_center",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Sales Invoice Item",
                "field_name": "item_code",
                "property": "columns",
                "property_type": "Int",
                "value": "3"
            },
            {
                "doctype": "Sales Invoice Item",
                "field_name": "qty",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doctype": "Sales Invoice Item",
                "field_name": "warehouse",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Sales Invoice Item",
                "field_name": "batch_no",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Sales Invoice Item",
                "field_name": "cost_center",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doctype": "Vehicle Log",
                "field_name": "license_plate",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Vehicle Log",
                "field_name": "employee",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": "license_plate.driver"
            },
            {
                "doctype": "Vehicle Service",
                "field_name": "service_item",
                "property": "options",
                "property_type": "Text",
                "value": "NOT SELECTED\nBrake Oil\nBrake Pad\nClutch Plate\nEngine Oil\nOil Change\nWheels"
            },
            {
                "doctype": "Vehicle Service",
                "field_name": "service_item",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Vehicle Service",
                "field_name": "type",
                "property": "options",
                "property_type": "Text",
                "value": "Repair\nInspection\nService\nChange"
            },
            {
                "doctype": "Vehicle Service",
                "field_name": "frequency",
                "property": "options",
                "property_type": "Text",
                "value": "NOT SELECTED\nMileage\nMonthly\nQuarterly\nHalf Yearly\nYearly"
            },
            {
                "doctype": "Vehicle Service",
                "field_name": "frequency",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Vehicle Log",
                "property": "quick_entry",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Vehicle Log",
                "field_name": "employee",
                "property": "fetch_if_empty",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Account",
                "property": "search_fields",
                "property_type": "Data",
                "value": "account_number, root_type, account_type"
            },
            {
                "doctype": "Vehicle Log",
                "field_name": "date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Vehicle Log",
                "field_name": "date",
                "property": "default",
                "property_type": "Text",
                "value": "Today"
            },
            {
                "doctype": "Vehicle Log",
                "field_name": "odometer",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Purchase Invoice Item",
                "field_name": "cost_center",
                "property": "default",
                "property_type": "Text",
                "value": ""
            },
            {
                "doctype": "Journal Entry",
                "field_name": "accounts",
                "property": "allow_bulk_edit",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Journal Entry",
                "field_name": "total_debit",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Journal Entry",
                "field_name": "total_amount",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Report",
                "field_name": "javascript",
                "property": "depends_on",
                "property_type": "Text",
                "value": ""
            },
            {
                "doctype": "Journal Entry Account",
                "field_name": "reference_name",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Journal Entry Account",
                "field_name": "account",
                "property": "width",
                "property_type": "Data",
                "value": ""
            },
            {
                "doctype": "Sales Invoice Item",
                "field_name": "item_tax_template",
                "property": "fetch_if_empty",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Sales Invoice Item",
                "field_name": "item_tax_template",
                "property": "default",
                "property_type": "Text",
                "value": ""
            },
            {
                "doctype": "Sales Invoice",
                "field_name": "letter_head",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": "company.default_letter_head"
            },
            {
                "doctype": "Sales Invoice",
                "field_name": "letter_head",
                "property": "fetch_if_empty",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Purchase Order",
                "field_name": "letter_head",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": ""
            },
            {
                "doctype": "Item Price",
                "field_name": "brand",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Item Price",
                "field_name": "price_list",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Delivery Note",
                "field_name": "items",
                "property": "allow_bulk_edit",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Item Price",
                "field_name": "valid_from",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Payment Entry",
                "field_name": "letter_head",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": "company.default_letter_head"
            },
            {
                "doctype": "Piecework Type",
                "property": "search_fields",
                "property_type": "Data",
                "value": "task_name"
            },
            {
                "doctype": "Document Attachment",
                "field_name": "attachment",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Operation",
                "property": "image_field",
                "property_type": "Data",
                "value": "image"
            },
            {
                "doctype": "Payment Entry",
                "field_name": "payment_accounts_section",
                "property": "collapsible",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Payment Entry",
                "field_name": "section_break_12",
                "property": "collapsible",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Bank Reconciliation Detail",
                "field_name": "payment_entry",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doctype": "Bank Reconciliation Detail",
                "field_name": "posting_date",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doctype": "Bank Reconciliation Detail",
                "field_name": "posting_date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Customer",
                "field_name": "tax_id",
                "property": "label",
                "property_type": "Data",
                "value": "TIN"
            },
            {
                "doctype": "Payment Entry Reference",
                "field_name": "due_date",
                "property": "width",
                "property_type": "Data",
                "value": "23"
            },
            {
                "doctype": "Payment Entry Reference",
                "field_name": "due_date",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doctype": "Payment Entry Reference",
                "field_name": "reference_doctype",
                "property": "columns",
                "property_type": "Int",
                "value": "0"
            },
            {
                "doctype": "Payment Entry Reference",
                "field_name": "reference_name",
                "property": "columns",
                "property_type": "Int",
                "value": "3"
            },
            {
                "doctype": "Payment Entry Reference",
                "field_name": "reference_doctype",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Payment Reconciliation Payment",
                "field_name": "posting_date",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doctype": "Payment Reconciliation Payment",
                "field_name": "posting_date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Sales Invoice",
                "field_name": "is_pos",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Sales Invoice",
                "field_name": "posting_date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Sales Invoice",
                "field_name": "pos_profile",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Stock Entry",
                "field_name": "from_warehouse",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": "repack_template.default_warehouse"
            },
            {
                "doctype": "Payment Schedule",
                "field_name": "payment_amount",
                "property": "options",
                "property_type": "Small Text",
                "value": "Company:company:default_currency"
            },
            {
                "doctype": "Journal Entry Account",
                "field_name": "party",
                "property": "columns",
                "property_type": "Int",
                "value": "2"
            },
            {
                "doctype": "Journal Entry Account",
                "field_name": "party_type",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doctype": "Budget",
                "field_name": "budget_against",
                "property": "options",
                "property_type": "Text",
                "value": "\nCost Center\nProject\nDepartment\nVehicle\nHealthcare Practitioner\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit\nHealthcare Practitioner\nHealthcare Service Unit"
            },
            {
                "doctype": "Customer",
                "property": "search_fields",
                "property_type": "Data",
                "value": "customer_name,customer_group,territory, mobile_no"
            },
            {
                "doctype": "Energy Point Log",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Route History",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Notification Log",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Scheduled Job Log",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Healthcare Service Order",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Healthcare Insurance Claim",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Comment",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Workflow Action",
                "property": "track_changes",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Sales Invoice",
                "field_name": "loyalty_points_redemption",
                "property": "depends_on",
                "property_type": "Data",
                "value": "eval: !in_list(frappe.user_roles, \"Healthcare Receptionist\")"
            },
            {
                "doctype": "Sales Invoice Item",
                "field_name": "discount_percentage",
                "property": "precision",
                "property_type": "Select",
                "value": "6",
            },
            {
                "doctype": "Purchase Invoice Item",
                "field_name": "discount_percentage",
                "property": "precision",
                "property_type": "Select",
                "value": "6",
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