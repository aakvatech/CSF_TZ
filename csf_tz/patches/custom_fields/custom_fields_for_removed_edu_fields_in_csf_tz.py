import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields = {
        "Account": [
            {
                "fieldname": "item",
                "fieldtype": "Link",
                "insert_after": "include_in_gross",
                "label": "Expense Item",
                "options": "Item"
            },
        ],
        'Address':[
            {
                'fieldname': 'tax_category',
                'fieldtype': 'Link',
                'insert_after': 'fax',
                'label': 'Tax Category',
                'options': 'Tax Category'
            },
            {
                'default': '0',
                'fieldname': 'is_your_company_address',
                'fieldtype': 'Check',
                'insert_after': 'linked_with',
                'label': 'Is Your Company Address',
            }
        ],
        'BOM':[
            {
                'fieldname': 'warehouses',
                'fieldtype': 'Section Break',
                'insert_after': 'image',
                'label': 'Warehouses',
            },
            {
                'fieldname': 'source_warehouse',
                'fieldtype': 'Link',
                'insert_after': 'warehouses',
                'label': 'Source Warehouse',
                'options': 'Warehouse'
            },
            {
                'fieldname': 'fg_warehouse',
                'fieldtype': 'Link',
                'insert_after': 'source_warehouse',
                'label': 'Target Warehouse',
                'options': 'Warehouse'
            },
            {
                'fieldname': 'column_break_15',
                'fieldtype': 'Column Break',
                'insert_after': 'fg_warehouse',
                'label': "",
            },
            {
                'fieldname': 'wip_warehouse',
                'fieldtype': 'Link',
                'insert_after': 'column_break_15',
                'label': 'Work-in-Progress Warehouse',
                'options': 'Warehouse'
            },
            {
                'fieldname': 'scrap_warehouse',
                'fieldtype': 'Link',
                'insert_after': 'wip_warehouse',
                'label': 'Scrap Warehouse',
                'options': 'Warehouse'
            }
        ],
        "Company":[
            {
                "fieldname": "default_item_tax_template",
                "fieldtype": "Link",
                "insert_after": "default_in_transit_warehouse",
                "label": "Default Item Tax Template",
                "options": "Item Tax Template"
            },
            {
                "default": "0",
                "fieldname": "max_records_in_dialog",
                "fieldtype": "Int",
                "insert_after": "sales_monthly_history",
                "label": "Max records in Dialog",
            },
            {
                "fieldname": "withholding_section",
                "fieldtype": "Section Break",
                "insert_after": "default_expense_claim_payable_account",
                "label": "Withholding",
            },
            {
                "fieldname": "default_withholding_payable_account",
                "fieldtype": "Link",
                "insert_after": "withholding_section",
                "label": "Default Withholding Payable Account",
                "options": "Account"
            },
            {
                "fieldname": "auto_create_for_purchase_withholding",
                "fieldtype": "Check",
                "insert_after": "default_withholding_payable_account",
                "label": "Auto Create For Purchase Withholding",
            },
            {
                "default": "0",
                "depends_on": "auto_create_for_purchase_withholding",
                "fieldname": "auto_submit_for_purchase_withholding",
                "fieldtype": "Check",
                "insert_after": "auto_create_for_purchase_withholding",
                "label": "Auto Submit For Purchase Withholding",
            },
            {
                "fieldname": "column_break_55",
                "fieldtype": "Column Break",
                "insert_after": "auto_submit_for_purchase_withholding",
                "label": "",
            },
            {
                "fieldname": "default_withholding_receivable_account",
                "fieldtype": "Link",
                "insert_after": "column_break_55",
                "label": "Default Withholding Receivable Account",
                "options": "Account"
            },
            {
                "fieldname": "auto_create_for_sales_withholding",
                "fieldtype": "Check",
                "insert_after": "default_withholding_receivable_account",
                "label": "Auto Create For Sales Withholding",
            },
            {
                "default": "0",
                "depends_on": "auto_create_for_sales_withholding",
                "fieldname": "auto_submit_for_sales_withholding",
                "fieldtype": "Check",
                "insert_after": "auto_create_for_sales_withholding",
                "label": "Auto Submit For Sales Withholding",
            },
            {
                "fieldname": "education_section",
                "fieldtype": "Section Break",
                "insert_after": "auto_submit_for_sales_withholding",
                "label": "Education",
            },
            {
                "fieldname": "bypass_material_request_validation",
                "fieldtype": "Check",
                "insert_after": "stock_adjustment_account",
                "label": "Bypass Material Request validation on Stock Entry",
            },
            {
                "default": "1",
                "description": "For Sales Invoices",
                "fieldname": "enabled_auto_create_delivery_notes",
                "fieldtype": "Check",
                "insert_after": "column_break_32",
                "label": "Enabled Auto Create Delivery Notes",
            },
            {
                "fieldname": "vrn",
                "fieldtype": "Data",
                "insert_after": "website",
                "label": "VRN",
                "translatable": 1
            },
            {
                "fieldname": "tin",
                "fieldtype": "Data",
                "insert_after": "vrn",
                "label": "TIN",
                "translatable": 1
            },
            {
                "fieldname": "p_o_box",
                "fieldtype": "Data",
                "insert_after": "tin",
                "label": "P O Box",
                "translatable": 1
            },
            {
                "fieldname": "city",
                "fieldtype": "Data",
                "insert_after": "p_o_box",
                "label": "City",
                "translatable": 1
            },
            {
                "fieldname": "plot_number",
                "fieldtype": "Data",
                "insert_after": "city",
                "label": "Plot Number",
                "translatable": 1
            },
            {
                "fieldname": "block_number",
                "fieldtype": "Data",
                "insert_after": "plot_number",
                "label": "Block Number",
                "translatable": 1
            },
            {
                "fieldname": "street",
                "fieldtype": "Data",
                "insert_after": "block_number",
                "label": "Street",
                "translatable": 1
            },
            {
                "fieldname": "section_break_12",
                "fieldtype": "Section Break",
                "insert_after": "company_description",
                "label": "",
            },
            {
                "fieldname": "company_bank_details",
                "fieldtype": "Text",
                "insert_after": "section_break_12",
                "label": "Company Bank Details",
                "translatable": 1
            }
        ],
        "Contact":[
            {
                "fieldname": "is_billing_contact",
                "fieldtype": "Check",
                "insert_after": "is_primary_contact",
                "label": "Is Billing Contact",
            },
        ],
        "Custom DocPerm":[
            {
                "fieldname": "dependent",
                "fieldtype": "Check",
                "insert_after": "parent",
                "label": "Dependent",
            },
        ],
        "Custom Field":[
            {
                "fetch_from": "",
                "fieldname": "module_def",
                "fieldtype": "Link",
                "insert_after": "",
                "label": "Module Def",
                "options": "Module Def"
            },
        ],
        "Customer":[
            {
                "bold": 1,
                "description": "Value Added Tax Registration Number (VAT RN = VRN)",
                "fieldname": "vrn",
                "fieldtype": "Data",
                "insert_after": "tax_id",
                "label": "VRN",
                "translatable": 1
            },
        ],
        "Delivery Note":[
            {
                "fieldname": "form_sales_invoice",
                "fieldtype": "Link",
                "insert_after": "patient_name",
                "label": "Form Sales Invoice",
                "options": "Sales Invoice",
                "read_only": 1
            },
        ],
        "Employee":[
           {
                "fieldname": "old_employee_id",
                "fieldtype": "Data",
                "insert_after": "image",
                "label": "Old Employee ID",
                "translatable": 1
            },
            {
                "fieldname": "heslb_f4_index_number",
                "fieldtype": "Data",
                "insert_after": "national_identity",
                "label": "HESLB F4 Index Number",
                "precision": "",
                "translatable": 1
            },
            {
                "fieldname": "employee_salary_component_limits",
                "fieldtype": "Section Break",
                "insert_after": "heslb_f4_index_number",
                "label": "Employee Salary Component Limits",
            },
            {
                "fieldname": "employee_salary_component_limit",
                "fieldtype": "Table",
                "insert_after": "employee_salary_component_limits",
                "label": "Employee Salary Component Limit",
                "options": "Employee Salary Component Limit"
            },
        ],
        "Item":[
            {
                "fieldname": "witholding_tax_rate_on_purchase",
                "fieldtype": "Float",
                "insert_after": "stock_uom",
                "label": "Withholding Tax Rate on Purchase",
            },
            {
                "fieldname": "withholding_tax_rate_on_sales",
                "fieldtype": "Float",
                "insert_after": "witholding_tax_rate_on_purchase",
                "label": "Withholding Tax Rate on Sales",
            },
            {
                "fieldname": "excisable_item",
                "fieldtype": "Check",
                "insert_after": "is_stock_item",
                "label": "Excisable Item",
            },
            {
                "fetch_from": "",
                "fieldname": "default_tax_template",
                "fieldtype": "Link",
                "insert_after": "item_tax_section_break",
                "label": "Default Tax Template",
                "options": "Item Tax Template"
            },
        ],
        "Journal Entry":[
            {
                "fieldname": "expense_record",
                "fieldtype": "Link",
                "label": "Expense Record",
                "options": "Expense Record",
                "read_only": 1
            },
            {
                "allow_on_submit": 1,
                "fieldname": "import_file",
                "fieldtype": "Link",
                "insert_after": "clearance_date",
                "label": "Import File",
                "options": "Import File"
            },
            {
                "fieldname": "from_date",
                "fieldtype": "Date",
                "insert_after": "auto_repeat",
                "label": "From Date",
            },
            {
                "fieldname": "to_date",
                "fieldtype": "Date",
                "insert_after": "from_date",
                "label": "To Date",
            },
            {
                "owner": "Administrator",
                "label": "Referance DocType",
                "fieldname": "referance_doctype",
                "insert_after": "payment_order",
                "fieldtype": "Link",
                "options": "DocType",
                "module_def": "CSF TZ"
            },
            {
                "owner": "Administrator",
                "label": "Referance DocName",
                "fieldname": "referance_docname",
                "insert_after": "referance_doctype",
                "fieldtype": "Dynamic Link",
                "options": "referance_doctype",
                "module_def": "CSF TZ"
            },
        ],
        "Landed Cost Voucher":[
            {
                "fieldname": "import_file",
                "fieldtype": "Link",
                "insert_after": "sec_break1",
                "label": "Import File",
                "options": "Import File"
            },
        ],
        "Material Request Item":[
            {
                "allow_on_submit": 1,
                "fieldname": "stock_reconciliation",
                "fieldtype": "Link",
                "insert_after": "lead_time_date",
                "label": "Stock Reconciliation",
                "options": "Stock Reconciliation",
                "read_only": 1
            },
        ],
        "Operation":[
            {
                "fieldname": "image",
                "fieldtype": "Attach Image",
                "hidden": 1,
                "insert_after": "description",
                "label": "Image",
            },
        ],
        "POS Profile":[
            {
                "fieldname": "electronic_fiscal_device",
                "fieldtype": "Link",
                "insert_after": "is_not_vfd_invoice",
                "label": "Electronic Fiscal Device",
                "options": "Electronic Fiscal Device",
                "reqd": 1
            },
            {
                "fieldname": "column_break_1",
                "fieldtype": "Column Break",
                "insert_after": "disabled",
                "label": "",
            },
        ],
        "Payment Entry Reference":[
            {
                "fieldname": "section_break_9",
                "fieldtype": "Section Break",
                "insert_after": "exchange_rate",
                "label": "",
            },
            {
                "columns": 1,
                "fetch_from": "reference_name.posting_date",
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "in_list_view": 1,
                "insert_after": "section_break_9",
                "label": "Posting Date",
            },
            {
                "fetch_from": "reference_name.from_date",
                "fieldname": "start_date",
                "fieldtype": "Date",
                "insert_after": "posting_date",
                "label": "Start Date",
            },
            {
                "fetch_from": "reference_name.to_date",
                "fieldname": "end_date",
                "fieldtype": "Date",
                "insert_after": "start_date",
                "label": "End Date",
            },
        ],
        "Print Settings":[
            {
                "default": "1",
                "fieldname": "compact_item_print",
                "fieldtype": "Check",
                "insert_after": "with_letterhead",
                "label": "Compact Item Print",
            },
            {
                "default": "0",
                "fieldname": "print_taxes_with_zero_amount",
                "fieldtype": "Check",
                "insert_after": "allow_print_for_cancelled",
                "label": "Print taxes with zero amount",
            },
        ],
        "Property Setter":[
            {
                "fetch_from": "",
                "fieldname": "module_def",
                "fieldtype": "Link",
                "insert_after": "",
                "label": "Module Def",
                "options": "Module Def"
            },
        ],
        "Purchase Invoice":[
            {
                "fieldname": "expense_record",
                "fieldtype": "Link",
                "insert_after": "amended_from",
                "label": "Expense Record",
                "options": "Expense Record",
                "read_only": 1
            },
            {
                "fieldname": "reference",
                "fieldtype": "Section Break",
                "insert_after": "language",
                "label": "Reference",
            },
            {
                "allow_on_submit": 1,
                "fieldname": "import_file",
                "fieldtype": "Link",
                "insert_after": "reference",
                "label": "Import File",
                "options": "Import File"
            },
        ],
        "Purchase Invoice Item":[
            {
                "allow_on_submit": 1,
                "fetch_from": "item_code.witholding_tax_rate_on_purchase",
                "fetch_if_empty": 1,
                "fieldname": "withholding_tax_rate",
                "fieldtype": "Float",
                "insert_after": "item_tax_template",
                "label": "Withholding Tax Rate",
            },
            {
                "allow_on_submit": 1,
                "fieldname": "withholding_tax_entry",
                "fieldtype": "Data",
                "insert_after": "withholding_tax_rate",
                "label": "Withholding Tax Entry",
                "translatable": 1
            },
        ],
        "Purchase Order":[
            {
                "default": "Today",
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "hidden": 1,
                "insert_after": "transaction_date",
                "label": "Posting Date",
            },
        ],
        "Sales Invoice":[
            {
                "allow_on_submit": 1,
                "fieldname": "delivery_status",
                "fieldtype": "Select",
                "in_standard_filter": 1,
                "insert_after": "pos_total_qty",
                "label": "Delivery Status",
                "options": "\nNot Delivered\nPart Delivered\nDelivered\nOver Delivered",
                "read_only": 1,
                "translatable": 1
            },
            {
                "allow_on_submit": 1,
                "depends_on": "eval: !in_list(frappe.user_roles, \"Healthcare Receptionist\")",
                "fieldname": "previous_invoice_number",
                "fieldtype": "Data",
                "insert_after": "is_return",
                "label": "Previous Invoice Number",
                "translatable": 1
            },
            {
                "depends_on": "eval: !in_list(frappe.user_roles, \"Healthcare Receptionist\")",
                "fieldname": "statutory_details",
                "fieldtype": "Section Break",
                "insert_after": "po_date",
                "label": "Statutory Details",
            },
            {
                "allow_on_submit": 1,
                "fieldname": "tra_control_number",
                "fieldtype": "Data",
                "insert_after": "statutory_details",
                "label": "TRA Control Number",
                "translatable": 1
            },
            {
                "allow_on_submit": 1,
                "fieldname": "witholding_tax_certificate_number",
                "fieldtype": "Data",
                "insert_after": "tra_control_number",
                "label": "Witholding Tax Certificate Number",
                "translatable": 1
            },
            {
                "fieldname": "column_break_29",
                "fieldtype": "Column Break",
                "insert_after": "witholding_tax_certificate_number",
                "label": "",
            },
            {
                "allow_on_submit": 1,
                "fetch_from": "pos_profile.electronic_fiscal_device",
                "fetch_if_empty": 1,
                "fieldname": "electronic_fiscal_device",
                "fieldtype": "Link",
                "insert_after": "column_break_29",
                "label": "Electronic Fiscal Device",
                "options": "Electronic Fiscal Device"
            },
            {
                "allow_on_submit": 1,
                "fieldname": "efd_z_report",
                "fieldtype": "Link",
                "insert_after": "electronic_fiscal_device",
                "label": "EFD Z Report",
                "options": "EFD Z Report"
            },
            {
                "depends_on": "eval: !in_list(frappe.user_roles, \"Healthcare Receptionist\")",
                "fieldname": "default_item_discount",
                "fieldtype": "Percent",
                "insert_after": "update_stock",
                "label": "Default Item Discount",
            },
            {
                "fetch_from": "company.default_item_tax_template",
                "fetch_if_empty": 1,
                "fieldname": "default_item_tax_template",
                "fieldtype": "Link",
                "insert_after": "default_item_discount",
                "label": "Default Item Tax Template",
                "options": "Item Tax Template"
            },
            {
                "fieldname": "section_break_80",
                "fieldtype": "Section Break",
                "insert_after": "default_item_tax_template",
                "label": "",
            },
            {
                "fieldname": "price_reduction",
                "fieldtype": "Currency",
                "insert_after": "base_net_total",
                "label": "Total Price Reduction Amount",
                "read_only": 1
            },
            {
                "allow_on_submit": 1,
                "fieldname": "excise_duty_applicable",
                "fieldtype": "Check",
                "insert_after": "col_break23",
                "label": "Excise Duty Applicable",
            },
            {
                "default": "1",
                "fetch_from": "",
                "fieldname": "enabled_auto_create_delivery_notes",
                "fieldtype": "Check",
                "insert_after": "delivery_status",
                "label": "Enabled Auto Create Delivery Notes",
            },
        ],
        "Sales Invoice Item":[
            {
                "allow_on_submit": 1,
                "fieldname": "is_ignored_in_pending_qty",
                "fieldtype": "Check",
                "insert_after": "item_code",
                "label": "Is Ignored In Pending Qty",
                "permlevel": 2,
                "precision": ""
            },
            {
                "default": "0",
                "fieldname": "allow_over_sell",
                "fieldtype": "Check",
                "insert_after": "customer_item_code",
                "label": "Allow Over Sell",
            },
            {
                "fetch_from": "item_code.withholding_tax_rate_on_sales",
                "fieldname": "withholding_tax_rate",
                "fieldtype": "Percent",
                "insert_after": "item_tax_template",
                "label": "Withholding Tax Rate",
            },
            {
                "allow_on_submit": 1,
                "fieldname": "withholding_tax_entry",
                "fieldtype": "Data",
                "ignore_user_permissions": 1,
                "insert_after": "withholding_tax_rate",
                "label": "Withholding Tax Entry",
                "read_only": 1,
                "translatable": 1
            },
            {
                "fieldname": "allow_override_net_rate",
                "fieldtype": "Check",
                "insert_after": "net_rate",
                "label": "Allow Override Net Rate",
                "permlevel": 1
            },
            {
                "allow_on_submit": 1,
                "fieldname": "delivery_status",
                "fieldtype": "Select",
                "insert_after": "sales_order",
                "label": "Delivery Status",
                "options": "\nNot Delivered\nPart Delivered\nDelivered\nOver Delivered",
                "read_only": 1,
                "translatable": 1
            },
        ],
        "Sales Order":[
            {
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "hidden": 1,
                "insert_after": "transaction_date",
                "label": "Posting Date",
            },
            {
                "fieldname": "default_item_discount",
                "fieldtype": "Percent",
                "insert_after": "scan_barcode",
                "label": "Default Item Discount",
            },
        ],
        "Stock Entry":[
            {
                "depends_on": "eval:doc.purpose==\"Repack\"",
                "fieldname": "repack_template",
                "fieldtype": "Link",
                "insert_after": "purchase_receipt_no",
                "label": "Repack Template",
                "options": "Repack Template"
            },
            {
                "depends_on": "eval:doc.purpose==\"Repack\"",
                "fetch_from": "repack_template.item_uom",
                "fieldname": "item_uom",
                "fieldtype": "Data",
                "insert_after": "repack_template",
                "label": "Item UOM",
                "read_only": 1,
                "translatable": 1
            },
            {
                "depends_on": "eval:doc.purpose==\"Repack\"",
                "fieldname": "repack_qty",
                "fieldtype": "Float",
                "insert_after": "item_uom",
                "label": "Repack Qty",
            },
            {
                "depends_on": "eval: doc.stock_entry_type == \"Send to Warehouse\"",
                "fieldname": "final_destination",
                "fieldtype": "Select",
                "insert_after": "target_address_display",
                "label": "Final Destination",
                "options": "",
                "translatable": 1
            },
            {
                "fieldname": "total_net_weight",
                "fieldtype": "Float",
                "insert_after": "section_break_19",
                "label": "Total Net Weight",
                "read_only": 1
            },
            {
                "fieldname": "transporter_info",
                "fieldtype": "Section Break",
                "insert_after": "letter_head",
                "label": "Transporter Info",
            },
            {
                "fieldname": "transporter",
                "fieldtype": "Link",
                "insert_after": "transporter_info",
                "label": "Transporter",
                "options": "Supplier"
            },
            {
                "fieldname": "driver",
                "fieldtype": "Link",
                "insert_after": "transporter",
                "label": "Driver",
                "options": "Driver"
            },
            {
                "fieldname": "transport_receipt_no",
                "fieldtype": "Data",
                "insert_after": "driver",
                "label": "Transport Receipt No",
                "translatable": 1
            },
            {
                "fieldname": "vehicle_no",
                "fieldtype": "Data",
                "insert_after": "transport_receipt_no",
                "label": "Vehicle No",
                "translatable": 1
            },
            {
                "fieldname": "column_break_69",
                "fieldtype": "Column Break",
                "insert_after": "vehicle_no",
                "label": "",
            },
            {
                "fieldname": "transporter_name",
                "fieldtype": "Data",
                "insert_after": "column_break_69",
                "label": "Transporter Name",
                "translatable": 1
            },
            {
                "fetch_from": "driver.full_name",
                "fieldname": "driver_name",
                "fieldtype": "Data",
                "insert_after": "transporter_name",
                "label": "Driver Name",
                "translatable": 1
            },
            {
                "fieldname": "transport_receipt_date",
                "fieldtype": "Date",
                "insert_after": "driver_name",
                "label": "Transport Receipt Date",
            },
        ],
        "Stock Entry Detail":[
            {
                "fieldname": "item_weight_details",
                "fieldtype": "Section Break",
                "insert_after": "sample_quantity",
                "label": "Item Weight Details",
            },
            {
                "fetch_from": "item_code.weight_per_unit",
                "fieldname": "weight_per_unit",
                "fieldtype": "Float",
                "insert_after": "item_weight_details",
                "label": "Weight Per Unit",
                "read_only": 1
            },
            {
                "fieldname": "total_weight",
                "fieldtype": "Float",
                "insert_after": "weight_per_unit",
                "label": "Total Weight",
                "read_only": 1
            },
            {
                "fieldname": "column_break_32",
                "fieldtype": "Column Break",
                "insert_after": "total_weight",
                "label": "",
            },
            {
                "fetch_from": "item_code.weight_uom",
                "fieldname": "weight_uom",
                "fieldtype": "Link",
                "insert_after": "column_break_32",
                "label": "Weight UOM",
                "options": "UOM",
                "read_only": 1
            },
        ],
        "Stock Reconciliation":[
            {
                "depends_on": "eval:doc.docstatus == 0",
                "fieldname": "sort_items",
                "fieldtype": "Button",
                "insert_after": "items",
                "label": "Sort Items",
            },
        ],
        "Stock Reconciliation Item":[
            {
                "fieldname": "material_request",
                "fieldtype": "Link",
                "insert_after": "amount",
                "label": "Material Request",
                "options": "Material Request",
                "read_only": 1
            },
        ],
        "Supplier":[
            {
                "bold": 1,
                "fieldname": "vrn",
                "fieldtype": "Data",
                "insert_after": "tax_id",
                "label": "VRN",
                "translatable": 1
            },
        ],
        "Vehicle":[
            {
                "module_def": "CSF TZ",
                "label": "Acquisition Odometer",
                "fieldname": "csf_tz_acquisition_odometer",
                "insert_after": "acquisition_date",
                "fieldtype": "Int",
            },
            {
                "owner": "Administrator",
                "module_def": "CSF TZ",
                "label": "Manufacturing Year",
                "fieldname": "csf_tz_year",
                "insert_after": "model",
                "fieldtype": "Int",
            },
            {
                "module_def": "CSF TZ",
                "label": "Engine Number",
                "fieldname": "csf_tz_engine_number",
                "insert_after": "chassis_no",
                "fieldtype": "Data",
            },
        ],
        "Vehicle Fine Record":[
            {
                "allow_on_submit": 1,
                "fieldname": "fully_paid",
                "fieldtype": "Check",
                "in_list_view": 1,
                "insert_after": "offence",
                "label": "FULLY PAID",
            },
        ],
        "Vehicle Log":[
            {
                "fieldname": "column_break_11",
                "fieldtype": "Column Break",
                "insert_after": "odometer",
                "label": "",
            },
            {
                "fieldname": "trip_destination",
                "fieldtype": "Data",
                "in_list_view": 1,
                "in_standard_filter": 1,
                "insert_after": "column_break_11",
                "label": "Trip Destination",
                "reqd": 1
            },
            {
                "fieldname": "destination_description",
                "fieldtype": "Data",
                "insert_after": "trip_destination",
                "label": "Destination Description",
                "translatable": 1
            },
        ],
        "Vehicle Service":[
            {
                "fieldname": "spare_name",
                "fieldtype": "Data",
                "in_list_view": 1,
                "label": "Spare Name",
            },
            {
                "fieldname": "quantity",
                "fieldtype": "Float",
                "in_list_view": 1,
                "insert_after": "spare_name",
                "label": "Quantity",
                "precision": "2"
            },
            {
                "allow_on_submit": 1,
                "fieldname": "invoice",
                "fieldtype": "Link",
                "in_list_view": 1,
                "insert_after": "type",
                "label": "Invoice",
                "options": "Purchase Invoice"
            }
        ]
    }
    create_custom_fields(fields, update=True)