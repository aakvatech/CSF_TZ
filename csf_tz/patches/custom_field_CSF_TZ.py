import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    def execute():
        fields={
        "Account": [
            {
                "fieldname": "item",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "include_in_gross",
                "label": "Expense Item",
                "modified": "2020-06-16 00:19:13.785448",
                "name": "Account-item",
                "options": "Item"
            },
        ],
        'Address':[
            {
                'fieldname': 'tax_category',
                'fieldtype': 'Link',
                'in_list_view': 0,
                'insert_after': 'fax',
                'label': 'Tax Category',
                'modified': '2018-12-28 22:29:21.828090',
                'name': 'Address-tax_category',
                'options': 'Tax Category'
            },
            {
                'default': '0',
                'fieldname': 'is_your_company_address',
                'fieldtype': 'Check',
                'in_list_view': 0,
                'insert_after': 'linked_with',
                'label': 'Is Your Company Address',
                'modified': '2020-10-14 17:41:40.878179',
                'name': 'Address-is_your_company_address'
            }
        ],
        'BOM':[
            {
                'fieldname': 'warehouses',
                'fieldtype': 'Section Break',
                'in_list_view': 0,
                'insert_after': 'image',
                'label': 'Warehouses',
                'modified': '2021-01-21 06:42:52.549662',
                'name': 'BOM-warehouses'
            },
            {
                'fieldname': 'source_warehouse',
                'fieldtype': 'Link',
                'in_list_view': 0,
                'insert_after': 'warehouses',
                'label': 'Source Warehouse',
                'modified': '2021-01-21 06:54:48.841522',
                'name': 'BOM-source_warehouse',
                'options': 'Warehouse'
            },
            {
                'fieldname': 'fg_warehouse',
                'fieldtype': 'Link',
                'in_list_view': 0,
                'insert_after': 'source_warehouse',
                'label': 'Target Warehouse',
                'modified': '2021-01-21 06:44:08.776914',
                'name': 'BOM-fg_warehouse',
                'options': 'Warehouse'
            },
            {
                'fieldname': 'column_break_15',
                'fieldtype': 'Column Break',
                'in_list_view': 0,
                'insert_after': 'fg_warehouse',
                'label': "",
                'modified': '2021-01-21 06:55:01.821947',
                'name': 'BOM-column_break_15'
            },
            {
                'fieldname': 'wip_warehouse',
                'fieldtype': 'Link',
                'in_list_view': 0,
                'insert_after': 'column_break_15',
                'label': 'Work-in-Progress Warehouse',
                'modified': '2021-01-21 06:42:52.960942',
                'name': 'BOM-wip_warehouse',
                'options': 'Warehouse'
            },
            {
                'fieldname': 'scrap_warehouse',
                'fieldtype': 'Link',
                'in_list_view': 0,
                'insert_after': 'wip_warehouse',
                'label': 'Scrap Warehouse',
                'modified': '2021-01-21 06:44:09.157050',
                'name': 'BOM-scrap_warehouse',
                'options': 'Warehouse'
            }
        ],
        "Company":[
            {
                "fieldname": "default_item_tax_template",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "default_in_transit_warehouse",
                "label": "Default Item Tax Template",
                "modified": "2021-03-31 08:45:00.684605",
                "name": "Company-default_item_tax_template",
                "options": "Item Tax Template"
            },
            {
                "default": "0",
                "fieldname": "max_records_in_dialog",
                "fieldtype": "Int",
                "in_list_view": 0,
                "insert_after": "sales_monthly_history",
                "label": "Max records in Dialog",
                "modified": "2020-05-07 08:55:04.364472",
                "name": "Company-max_records_in_dialog"
            },
            {
                "fieldname": "withholding_section",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "default_expense_claim_payable_account",
                "label": "Withholding",
                "modified": "2020-08-05 22:35:42.216333",
                "name": "Company-withholding_section"
            },
            {
                "fieldname": "default_withholding_payable_account",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "withholding_section",
                "label": "Default Withholding Payable Account",
                "modified": "2020-07-17 00:37:50.184521",
                "name": "Company-default_withholding_payable_account",
                "options": "Account"
            },
            {
                "fieldname": "auto_create_for_purchase_withholding",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "default_withholding_payable_account",
                "label": "Auto Create For Purchase Withholding",
                "modified": "2020-09-01 23:21:15.437803",
                "name": "Company-auto_create_for_purchase_withholding"
            },
            {
                "default": "0",
                "depends_on": "auto_create_for_purchase_withholding",
                "fieldname": "auto_submit_for_purchase_withholding",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "auto_create_for_purchase_withholding",
                "label": "Auto Submit For Purchase Withholding",
                "modified": "2020-08-05 22:48:17.854167",
                "name": "Company-auto_submit_for_purchase_withholding"
            },
            {
                "fieldname": "column_break_55",
                "fieldtype": "Column Break",
                "in_list_view": 0,
                "insert_after": "auto_submit_for_purchase_withholding",
                "label": "",
                "modified": "2020-08-05 22:48:18.181399",
                "name": "Company-column_break_55"
            },
            {
                "fieldname": "default_withholding_receivable_account",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "column_break_55",
                "label": "Default Withholding Receivable Account",
                "modified": "2020-08-05 22:48:18.477944",
                "name": "Company-default_withholding_receivable_account",
                "options": "Account"
            },
            {
                "fieldname": "auto_create_for_sales_withholding",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "default_withholding_receivable_account",
                "label": "Auto Create For Sales Withholding",
                "modified": "2020-09-01 23:21:15.814351",
                "name": "Company-auto_create_for_sales_withholding"
            },
            {
                "default": "0",
                "depends_on": "auto_create_for_sales_withholding",
                "fieldname": "auto_submit_for_sales_withholding",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "auto_create_for_sales_withholding",
                "label": "Auto Submit For Sales Withholding",
                "modified": "2020-08-05 22:48:18.789116",
                "name": "Company-auto_submit_for_sales_withholding"
            },
            {
                "fieldname": "education_section",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "auto_submit_for_sales_withholding",
                "label": "Education",
                "modified": "2020-08-18 15:46:30.057666",
                "name": "Company-education_section"
            },
            {
                "default": "0",
                "fieldname": "send_fee_details_to_bank",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "education_section",
                "label": "Send Fee details to Bank",
                "modified": "2020-08-18 15:46:30.517510",
                "name": "Company-send_fee_details_to_bank"
            },
            {
                "fieldname": "fee_bank_account",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "send_fee_details_to_bank",
                "label": "Fee Bank Account",
                "modified": "2020-09-01 01:35:36.035810",
                "name": "Company-fee_bank_account",
                "options": "Account"
            },
            {
                "fieldname": "student_applicant_fees_revenue_account",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "fee_bank_account",
                "label": "Student Applicant Fees Revenue Account",
                "modified": "2020-09-01 01:36:24.342359",
                "name": "Company-student_applicant_fees_revenue_account",
                "options": "Account"
            },
            {
                "fieldname": "column_break_60",
                "fieldtype": "Column Break",
                "in_list_view": 0,
                "insert_after": "student_applicant_fees_revenue_account",
                "label": "",
                "modified": "2020-08-18 15:47:26.978439",
                "name": "Company-column_break_60"
            },
            {
                "depends_on": "send_fee_details_to_bank",
                "fieldname": "nmb_series",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "column_break_60",
                "label": "NMB Series",
                "modified": "2020-08-10 16:10:54.189754",
                "name": "Company-nmb_series",
                "translatable": 1
            },
            {
                "depends_on": "send_fee_details_to_bank",
                "fieldname": "nmb_username",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "nmb_series",
                "label": "NMB User Name",
                "modified": "2020-07-28 03:54:27.672291",
                "name": "Company-nmb_username",
                "translatable": 1
            },
            {
                "depends_on": "send_fee_details_to_bank",
                "fieldname": "nmb_password",
                "fieldtype": "Password",
                "in_list_view": 0,
                "insert_after": "nmb_username",
                "label": "NMB Password",
                "modified": "2020-07-28 03:54:28.347794",
                "name": "Company-nmb_password"
            },
            {
                "depends_on": "send_fee_details_to_bank",
                "fieldname": "nmb_url",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "nmb_password",
                "label": "NMb URL",
                "modified": "2020-08-10 16:11:58.119081",
                "name": "Company-nmb_url",
                "translatable": 1
            },
            {
                "fieldname": "bypass_material_request_validation",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "stock_adjustment_account",
                "label": "Bypass Material Request validation on Stock Entry",
                "modified": "2020-09-10 16:46:34.320822",
                "name": "Company-bypass_material_request_validation"
            },
            {
                "default": "1",
                "description": "For Sales Invoices",
                "fieldname": "enabled_auto_create_delivery_notes",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "column_break_32",
                "label": "Enabled Auto Create Delivery Notes",
                "modified": "2020-07-17 22:30:49.037893",
                "name": "Company-enabled_auto_create_delivery_notes"
            },
            {
                "fieldname": "vrn",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "website",
                "label": "VRN",
                "modified": "2019-12-20 19:22:02.995304",
                "name": "Company-vrn",
                "translatable": 1
            },
            {
                "fieldname": "tin",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "vrn",
                "label": "TIN",
                "modified": "2019-12-20 19:22:10.324100",
                "name": "Company-tin",
                "translatable": 1
            },
            {
                "fieldname": "p_o_box",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "tin",
                "label": "P O Box",
                "modified": "2020-05-07 17:49:19.841962",
                "name": "Company-p_o_box",
                "translatable": 1
            },
            {
                "fieldname": "city",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "p_o_box",
                "label": "City",
                "modified": "2020-05-07 17:49:20.430328",
                "name": "Company-city",
                "translatable": 1
            },
            {
                "fieldname": "plot_number",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "city",
                "label": "Plot Number",
                "modified": "2020-05-07 13:58:31.627080",
                "name": "Company-plot_number",
                "translatable": 1
            },
            {
                "fieldname": "block_number",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "plot_number",
                "label": "Block Number",
                "modified": "2020-05-07 13:58:32.111317",
                "name": "Company-block_number",
                "translatable": 1
            },
            {
                "fieldname": "street",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "block_number",
                "label": "Street",
                "modified": "2020-05-07 13:58:32.664481",
                "name": "Company-street",
                "translatable": 1
            },
            {
                "fieldname": "section_break_12",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "company_description",
                "label": "",
                "modified": "2019-12-20 19:22:27.862997",
                "name": "Company-section_break_12"
            },
            {
                "fieldname": "company_bank_details",
                "fieldtype": "Text",
                "in_list_view": 0,
                "insert_after": "section_break_12",
                "label": "Company Bank Details",
                "modified": "2019-12-20 19:22:19.201911",
                "name": "Company-company_bank_details",
                "translatable": 1
            }
        ],
        "Contact":[
            {
                "fieldname": "is_billing_contact",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "is_primary_contact",
                "label": "Is Billing Contact",
                "modified": "2019-12-02 11:00:03.432994",
                "name": "Contact-is_billing_contact"
            },
        ],
        "Custom DocPerm":[
            {
                "fieldname": "dependent",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "parent",
                "label": "Dependent",
                "modified": "2021-03-19 23:25:35.897256",
                "name": "Custom DocPerm-dependent"
            },
        ],
        "Custom Field":[
            {
                "fetch_from": "",
                "fieldname": "module_def",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "",
                "label": "Module Def",
                "modified": "2020-08-13 18:32:53.375956",
                "name": "Custom Field-module_def",
                "options": "Module Def"
            },
        ],
        "Customer":[
            {
                "bold": 1,
                "description": "Value Added Tax Registration Number (VAT RN = VRN)",
                "fieldname": "vrn",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "tax_id",
                "label": "VRN",
                "modified": "2019-12-20 19:21:41.980276",
                "name": "Customer-vrn",
                "translatable": 1
            },
        ],
        "Delivery Note":[
            {
                "fieldname": "form_sales_invoice",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "patient_name",
                "label": "Form Sales Invoice",
                "modified": "2020-06-28 22:15:11.257297",
                "name": "Delivery Note-form_sales_invoice",
                "options": "Sales Invoice",
                "read_only": 1
            },
        ],
        "Employee":[
           {
                "fieldname": "old_employee_id",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "image",
                "label": "Old Employee ID",
                "modified": "2020-09-24 11:29:02.966955",
                "name": "Employee-old_employee_id",
                "translatable": 1
            },
            {
                "fieldname": "heslb_f4_index_number",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "national_identity",
                "label": "HESLB F4 Index Number",
                "modified": "2021-08-16 17:52:02.294599",
                "name": "Employee-heslb_f4_index_number",
                "precision": "",
                "translatable": 1
            },
            {
                "fieldname": "employee_salary_component_limits",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "heslb_f4_index_number",
                "label": "Employee Salary Component Limits",
                "modified": "2021-07-25 21:03:21.031697",
                "name": "Employee-employee_salary_component_limits"
            },
            {
                "fieldname": "employee_salary_component_limit",
                "fieldtype": "Table",
                "in_list_view": 0,
                "insert_after": "employee_salary_component_limits",
                "label": "Employee Salary Component Limit",
                "modified": "2021-07-25 21:03:21.895844",
                "name": "Employee-employee_salary_component_limit",
                "options": "Employee Salary Component Limit"
            },
        ],
        "Fee Structure":[
            {
                "allow_on_submit": 1,
                "fieldname": "default_fee_category",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "student_category",
                "label": "Default Fee Category",
                "modified": "2020-07-31 12:20:15.767419",
                "name": "Fee Structure-default_fee_category",
                "options": "Fee Category"
            },
        ],
        "Fees":[
            {
                "allow_on_submit": 1,
                "fieldname": "callback_token",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "healthcare_practitioner",
                "label": "Callback Token",
                "modified": "2020-08-10 17:17:36.137062",
                "name": "Fees-callback_token",
                "read_only": 1,
                "translatable": 1
            },
            {
                "fieldname": "from_date",
                "fieldtype": "Date",
                "in_list_view": 0,
                "insert_after": "vehicle",
                "label": "From Date",
                "modified": "2020-08-18 13:10:14.387470",
                "name": "Fees-from_date"
            },
            {
                "allow_on_submit": 1,
                "fieldname": "bank_reference",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "send_payment_request",
                "label": "Bank Reference",
                "modified": "2020-08-10 17:13:35.213803",
                "name": "Fees-bank_reference",
                "read_only": 1,
                "translatable": 1
            },
            {
                "fetch_from": "company.abbr",
                "fieldname": "abbr",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "company",
                "label": "Abbr",
                "modified": "2020-07-22 13:06:42.155142",
                "name": "Fees-abbr",
                "read_only": 1,
                "translatable": 1
            },
            {
                "fieldname": "to_date",
                "fieldtype": "Date",
                "in_list_view": 0,
                "insert_after": "from_date",
                "label": "To Date",
                "modified": "2020-08-18 13:10:14.889080",
                "name": "Fees-to_date"
            },
        ],
        "Item":[
            {
                "fieldname": "witholding_tax_rate_on_purchase",
                "fieldtype": "Float",
                "in_list_view": 0,
                "insert_after": "stock_uom",
                "label": "Withholding Tax Rate on Purchase",
                "modified": "2020-05-05 12:33:29.224597",
                "name": "Item-witholding_tax_rate_on_purchase"
            },
            {
                "fieldname": "withholding_tax_rate_on_sales",
                "fieldtype": "Float",
                "in_list_view": 0,
                "insert_after": "witholding_tax_rate_on_purchase",
                "label": "Withholding Tax Rate on Sales",
                "modified": "2020-08-06 01:17:58.305162",
                "name": "Item-withholding_tax_rate_on_sales"
            },
            {
                "fieldname": "excisable_item",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "is_stock_item",
                "label": "Excisable Item",
                "modified": "2021-03-06 07:27:57.882935",
                "name": "Item-excisable_item"
            },
            {
                "fetch_from": "",
                "fieldname": "default_tax_template",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "item_tax_section_break",
                "label": "Default Tax Template",
                "modified": "2021-03-10 12:04:59.499730",
                "name": "Item-default_tax_template",
                "options": "Item Tax Template"
            },
        ],
        "Journal Entry":[
            {
                "fieldname": "expense_record",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "naming_series",
                "label": "Expense Record",
                "modified": "2020-06-18 00:24:05.285565",
                "name": "Journal Entry-expense_record",
                "options": "Expense Record",
                "read_only": 1
            },
            {
                "allow_on_submit": 1,
                "fieldname": "import_file",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "clearance_date",
                "label": "Import File",
                "modified": "2021-01-20 13:50:31.424897",
                "name": "Journal Entry-import_file",
                "options": "Import File"
            },
            {
                "fieldname": "from_date",
                "fieldtype": "Date",
                "in_list_view": 0,
                "insert_after": "auto_repeat",
                "label": "From Date",
                "modified": "2019-12-20 19:22:47.765536",
                "name": "Journal Entry-from_date"
            },
            {
                "fieldname": "to_date",
                "fieldtype": "Date",
                "in_list_view": 0,
                "insert_after": "from_date",
                "label": "To Date",
                "modified": "2019-12-20 19:22:38.720845",
                "name": "Journal Entry-to_date"
            },
            {
                "name": "Journal Entry-referance_doctype",
                "owner": "Administrator",
                "modified": "2022-03-08 23:23:52.276124",
                "label": "Referance DocType",
                "fieldname": "referance_doctype",
                "insert_after": "payment_order",
                "fieldtype": "Link",
                "options": "DocType",
                "module_def": "CSF TZ"
            },
            {
                "name": "Journal Entry-referance_docname",
                "owner": "Administrator",
                "modified": "2022-03-08 23:24:03.811966",
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
                "in_list_view": 0,
                "insert_after": "sec_break1",
                "label": "Import File",
                "modified": "2021-01-20 20:26:59.420718",
                "name": "Landed Cost Voucher-import_file",
                "options": "Import File"
            },
        ],
        "Material Request Item":[
            {
                "allow_on_submit": 1,
                "fieldname": "stock_reconciliation",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "lead_time_date",
                "label": "Stock Reconciliation",
                "modified": "2020-06-24 22:47:46.584890",
                "name": "Material Request Item-stock_reconciliation",
                "options": "Stock Reconciliation",
                "read_only": 1
            },
        ],
        "Operation":[
            {
                "fieldname": "image",
                "fieldtype": "Attach Image",
                "hidden": 1,
                "in_list_view": 0,
                "insert_after": "description",
                "label": "Image",
                "modified": "2020-10-17 02:40:39.330498",
                "name": "Operation-image"
            },
        ],
        "POS Profile":[
            {
                "fieldname": "electronic_fiscal_device",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "is_not_vfd_invoice",
                "label": "Electronic Fiscal Device",
                "modified": "2020-03-05 19:37:44.325865",
                "name": "POS Profile-electronic_fiscal_device",
                "options": "Electronic Fiscal Device",
                "reqd": 1
            },
            {
                "fieldname": "column_break_1",
                "fieldtype": "Column Break",
                "in_list_view": 0,
                "insert_after": "disabled",
                "label": "",
                "modified": "2020-03-05 19:37:44.023203",
                "name": "POS Profile-column_break_1"
            },
        ],
        "Payment Entry Reference":[
            {
                "fieldname": "section_break_9",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "exchange_rate",
                "label": "",
                "modified": "2019-12-20 19:23:11.532502",
                "name": "Payment Entry Reference-section_break_9"
            },
            {
                "columns": 1,
                "fetch_from": "reference_name.posting_date",
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "in_list_view": 1,
                "insert_after": "section_break_9",
                "label": "Posting Date",
                "modified": "2019-12-20 19:23:23.225925",
                "name": "Payment Entry Reference-posting_date"
            },
            {
                "fetch_from": "reference_name.from_date",
                "fieldname": "start_date",
                "fieldtype": "Date",
                "in_list_view": 0,
                "insert_after": "posting_date",
                "label": "Start Date",
                "modified": "2019-12-20 19:23:57.230372",
                "name": "Payment Entry Reference-start_date"
            },
            {
                "fetch_from": "reference_name.to_date",
                "fieldname": "end_date",
                "fieldtype": "Date",
                "in_list_view": 0,
                "insert_after": "start_date",
                "label": "End Date",
                "modified": "2019-12-20 19:23:36.497233",
                "name": "Payment Entry Reference-end_date"
            },
        ],
        "Print Settings":[
            {
                "default": "1",
                "fieldname": "compact_item_print",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "with_letterhead",
                "label": "Compact Item Print",
                "modified": "2020-04-29 12:32:28.701703",
                "name": "Print Settings-compact_item_print"
            },
            {
                "default": "0",
                "fieldname": "print_taxes_with_zero_amount",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "allow_print_for_cancelled",
                "label": "Print taxes with zero amount",
                "modified": "2020-04-29 12:32:28.864970",
                "name": "Print Settings-print_taxes_with_zero_amount"
            },
        ],
        "Program":[
            {
                "fieldname": "fees",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "courses",
                "label": "Fees",
                "modified": "2020-07-31 09:39:52.330874",
                "name": "Program-fees"
            },
            {
                "fieldname": "program_fee",
                "fieldtype": "Table",
                "in_list_view": 0,
                "insert_after": "fees",
                "label": "Program Fee",
                "modified": "2020-07-31 09:39:52.739333",
                "name": "Program-program_fee",
                "options": "Program Fee"
            },
        ],
        "Program Fee":[
            {
                "fetch_from": "fee_structure.default_fee_category",
                "fieldname": "default_fee_category",
                "fieldtype": "Link",
                "in_list_view": 1,
                "insert_after": "due_date",
                "label": "Default Fee Category",
                "modified": "2020-07-31 12:32:27.126255",
                "name": "Program Fee-default_fee_category",
                "options": "Fee Category"
            },
        ],
        "Property Setter":[
            {
                "fetch_from": "",
                "fieldname": "module_def",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "",
                "label": "Module Def",
                "name": "Property Setter-module_def",
                "options": "Module Def"
            },
        ],
        "Purchase Invoice":[
            {
                "fieldname": "expense_record",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "amended_from",
                "label": "Expense Record",
                "modified": "2020-06-17 22:59:39.964707",
                "name": "Purchase Invoice-expense_record",
                "options": "Expense Record",
                "read_only": 1
            },
            {
                "fieldname": "reference",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "language",
                "label": "Reference",
                "modified": "2021-01-20 13:49:43.238770",
                "name": "Purchase Invoice-reference"
            },
            {
                "allow_on_submit": 1,
                "fieldname": "import_file",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "reference",
                "label": "Import File",
                "modified": "2021-01-20 13:49:43.767414",
                "name": "Purchase Invoice-import_file",
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
                "in_list_view": 0,
                "insert_after": "item_tax_template",
                "label": "Withholding Tax Rate",
                "modified": "2020-07-17 01:03:26.025362",
                "name": "Purchase Invoice Item-withholding_tax_rate"
            },
            {
                "allow_on_submit": 1,
                "fieldname": "withholding_tax_entry",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "withholding_tax_rate",
                "label": "Withholding Tax Entry",
                "modified": "2020-07-17 16:37:56.527525",
                "name": "Purchase Invoice Item-withholding_tax_entry",
                "translatable": 1
            },
        ],
        "Purchase Order":[
            {
                "default": "Today",
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "hidden": 1,
                "in_list_view": 0,
                "insert_after": "transaction_date",
                "label": "Posting Date",
                "modified": "2020-03-13 16:59:13.689530",
                "name": "Purchase Order-posting_date"
            },
        ],
        "Sales Invoice":[
            {
                "allow_on_submit": 1,
                "fieldname": "delivery_status",
                "fieldtype": "Select",
                "in_list_view": 0,
                "in_standard_filter": 1,
                "insert_after": "pos_total_qty",
                "label": "Delivery Status",
                "modified": "2020-06-19 18:16:07.249867",
                "name": "Sales Invoice-delivery_status",
                "options": "\nNot Delivered\nPart Delivered\nDelivered\nOver Delivered",
                "read_only": 1,
                "translatable": 1
            },
            {
                "allow_on_submit": 1,
                "depends_on": "eval: !in_list(frappe.user_roles, \"Healthcare Receptionist\")",
                "fieldname": "previous_invoice_number",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "is_return",
                "label": "Previous Invoice Number",
                "modified": "2020-08-05 14:33:05.352542",
                "name": "Sales Invoice-previous_invoice_number",
                "translatable": 1
            },
            {
                "depends_on": "eval: !in_list(frappe.user_roles, \"Healthcare Receptionist\")",
                "fieldname": "statutory_details",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "po_date",
                "label": "Statutory Details",
                "modified": "2019-12-20 19:25:08.716714",
                "name": "Sales Invoice-statutory_details"
            },
            {
                "allow_on_submit": 1,
                "fieldname": "tra_control_number",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "statutory_details",
                "label": "TRA Control Number",
                "modified": "2019-12-20 19:24:51.344893",
                "name": "Sales Invoice-tra_control_number",
                "translatable": 1
            },
            {
                "allow_on_submit": 1,
                "fieldname": "witholding_tax_certificate_number",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "tra_control_number",
                "label": "Witholding Tax Certificate Number",
                "modified": "2019-12-20 19:23:45.693752",
                "name": "Sales Invoice-witholding_tax_certificate_number",
                "translatable": 1
            },
            {
                "fieldname": "column_break_29",
                "fieldtype": "Column Break",
                "in_list_view": 0,
                "insert_after": "witholding_tax_certificate_number",
                "label": "",
                "modified": "2019-12-20 19:24:28.702495",
                "name": "Sales Invoice-column_break_29"
            },
            {
                "allow_on_submit": 1,
                "fetch_from": "pos_profile.electronic_fiscal_device",
                "fetch_if_empty": 1,
                "fieldname": "electronic_fiscal_device",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "column_break_29",
                "label": "Electronic Fiscal Device",
                "modified": "2020-03-05 16:05:01.332647",
                "name": "Sales Invoice-electronic_fiscal_device",
                "options": "Electronic Fiscal Device"
            },
            {
                "allow_on_submit": 1,
                "fieldname": "efd_z_report",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "electronic_fiscal_device",
                "label": "EFD Z Report",
                "modified": "2019-12-20 19:24:07.925266",
                "name": "Sales Invoice-efd_z_report",
                "options": "EFD Z Report"
            },
            {
                "depends_on": "eval: !in_list(frappe.user_roles, \"Healthcare Receptionist\")",
                "fieldname": "default_item_discount",
                "fieldtype": "Percent",
                "in_list_view": 0,
                "insert_after": "update_stock",
                "label": "Default Item Discount",
                "modified": "2021-01-09 19:30:39.855293",
                "name": "Sales Invoice-default_item_discount"
            },
            {
                "fetch_from": "company.default_item_tax_template",
                "fetch_if_empty": 1,
                "fieldname": "default_item_tax_template",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "default_item_discount",
                "label": "Default Item Tax Template",
                "modified": "2021-02-08 22:50:03.490542",
                "name": "Sales Invoice-default_item_tax_template",
                "options": "Item Tax Template"
            },
            {
                "fieldname": "section_break_80",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "default_item_tax_template",
                "label": "",
                "modified": "2021-02-08 22:50:04.586234",
                "name": "Sales Invoice-section_break_80"
            },
            {
                "fieldname": "price_reduction",
                "fieldtype": "Currency",
                "in_list_view": 0,
                "insert_after": "base_net_total",
                "label": "Total Price Reduction Amount",
                "modified": "2020-06-28 02:56:42.240626",
                "name": "Sales Invoice-price_reduction",
                "read_only": 1
            },
            {
                "allow_on_submit": 1,
                "fieldname": "excise_duty_applicable",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "col_break23",
                "label": "Excise Duty Applicable",
                "modified": "2021-03-06 07:42:46.718597",
                "name": "Sales Invoice-excise_duty_applicable"
            },
            {
                "default": "1",
                "fetch_from": "",
                "fieldname": "enabled_auto_create_delivery_notes",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "delivery_status",
                "label": "Enabled Auto Create Delivery Notes",
                "modified": "2020-08-13 18:32:53.375956",
                "name": "Sales Invoice-enabled_auto_create_delivery_notes"
            },
        ],
        "Sales Invoice Item":[
            {
                "allow_on_submit": 1,
                "fieldname": "is_ignored_in_pending_qty",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "item_code",
                "label": "Is Ignored In Pending Qty",
                "modified": "2021-09-23 23:33:08.695837",
                "name": "Sales Invoice Item-is_ignored_in_pending_qty",
                "permlevel": 2,
                "precision": ""
            },
            {
                "default": "0",
                "fieldname": "allow_over_sell",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "customer_item_code",
                "label": "Allow Over Sell",
                "modified": "2020-06-19 17:42:30.386345",
                "name": "Sales Invoice Item-allow_over_sell"
            },
            {
                "fetch_from": "item_code.withholding_tax_rate_on_sales",
                "fieldname": "withholding_tax_rate",
                "fieldtype": "Percent",
                "in_list_view": 0,
                "insert_after": "item_tax_template",
                "label": "Withholding Tax Rate",
                "modified": "2019-12-20 00:57:44.450609",
                "name": "Sales Invoice Item-withholding_tax_rate"
            },
            {
                "allow_on_submit": 1,
                "fieldname": "withholding_tax_entry",
                "fieldtype": "Data",
                "ignore_user_permissions": 1,
                "in_list_view": 0,
                "insert_after": "withholding_tax_rate",
                "label": "Withholding Tax Entry",
                "modified": "2020-08-06 01:34:59.329482",
                "name": "Sales Invoice Item-withholding_tax_entry",
                "read_only": 1,
                "translatable": 1
            },
            {
                "fieldname": "allow_override_net_rate",
                "fieldtype": "Check",
                "in_list_view": 0,
                "insert_after": "net_rate",
                "label": "Allow Override Net Rate",
                "modified": "2020-07-02 17:20:45.022013",
                "name": "Sales Invoice Item-allow_override_net_rate",
                "permlevel": 1
            },
            {
                "allow_on_submit": 1,
                "fieldname": "delivery_status",
                "fieldtype": "Select",
                "in_list_view": 0,
                "insert_after": "sales_order",
                "label": "Delivery Status",
                "modified": "2020-06-19 18:17:11.595366",
                "name": "Sales Invoice Item-delivery_status",
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
                "in_list_view": 0,
                "insert_after": "transaction_date",
                "label": "Posting Date",
                "modified": "2020-03-13 17:00:30.266085",
                "name": "Sales Order-posting_date"
            },
            {
                "fieldname": "default_item_discount",
                "fieldtype": "Percent",
                "in_list_view": 0,
                "insert_after": "scan_barcode",
                "label": "Default Item Discount",
                "modified": "2021-02-04 08:16:47.825862",
                "name": "Sales Order-default_item_discount"
            },
        ],
        "Stock Entry":[
            {
                "depends_on": "eval:doc.purpose==\"Repack\"",
                "fieldname": "repack_template",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "purchase_receipt_no",
                "label": "Repack Template",
                "modified": "2020-05-29 11:40:04.831550",
                "name": "Stock Entry-repack_template",
                "options": "Repack Template"
            },
            {
                "depends_on": "eval:doc.purpose==\"Repack\"",
                "fetch_from": "repack_template.item_uom",
                "fieldname": "item_uom",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "repack_template",
                "label": "Item UOM",
                "modified": "2020-05-29 12:22:24.669156",
                "name": "Stock Entry-item_uom",
                "read_only": 1,
                "translatable": 1
            },
            {
                "depends_on": "eval:doc.purpose==\"Repack\"",
                "fieldname": "repack_qty",
                "fieldtype": "Float",
                "in_list_view": 0,
                "insert_after": "item_uom",
                "label": "Repack Qty",
                "modified": "2020-05-29 11:40:05.783365",
                "name": "Stock Entry-repack_qty"
            },
            {
                "depends_on": "eval: doc.stock_entry_type == \"Send to Warehouse\"",
                "fieldname": "final_destination",
                "fieldtype": "Select",
                "in_list_view": 0,
                "insert_after": "target_address_display",
                "label": "Final Destination",
                "modified": "2020-06-29 18:07:10.893479",
                "name": "Stock Entry-final_destination",
                "options": "",
                "translatable": 1
            },
            {
                "fieldname": "total_net_weight",
                "fieldtype": "Float",
                "in_list_view": 0,
                "insert_after": "section_break_19",
                "label": "Total Net Weight",
                "modified": "2020-06-30 14:59:16.406735",
                "name": "Stock Entry-total_net_weight",
                "read_only": 1
            },
            {
                "fieldname": "transporter_info",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "letter_head",
                "label": "Transporter Info",
                "modified": "2020-06-23 16:43:00.237708",
                "name": "Stock Entry-transporter_info"
            },
            {
                "fieldname": "transporter",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "transporter_info",
                "label": "Transporter",
                "modified": "2020-06-23 16:43:00.755674",
                "name": "Stock Entry-transporter",
                "options": "Supplier"
            },
            {
                "fieldname": "driver",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "transporter",
                "label": "Driver",
                "modified": "2020-06-23 16:43:01.308481",
                "name": "Stock Entry-driver",
                "options": "Driver"
            },
            {
                "fieldname": "transport_receipt_no",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "driver",
                "label": "Transport Receipt No",
                "modified": "2020-06-23 16:43:01.837481",
                "name": "Stock Entry-transport_receipt_no",
                "translatable": 1
            },
            {
                "fieldname": "vehicle_no",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "transport_receipt_no",
                "label": "Vehicle No",
                "modified": "2020-06-23 16:43:02.364744",
                "name": "Stock Entry-vehicle_no",
                "translatable": 1
            },
            {
                "fieldname": "column_break_69",
                "fieldtype": "Column Break",
                "in_list_view": 0,
                "insert_after": "vehicle_no",
                "label": "",
                "modified": "2020-06-23 16:43:02.892782",
                "name": "Stock Entry-column_break_69"
            },
            {
                "fieldname": "transporter_name",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "column_break_69",
                "label": "Transporter Name",
                "modified": "2020-06-23 16:43:03.373538",
                "name": "Stock Entry-transporter_name",
                "translatable": 1
            },
            {
                "fetch_from": "driver.full_name",
                "fieldname": "driver_name",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "transporter_name",
                "label": "Driver Name",
                "modified": "2020-06-23 16:43:03.900970",
                "name": "Stock Entry-driver_name",
                "translatable": 1
            },
            {
                "fieldname": "transport_receipt_date",
                "fieldtype": "Date",
                "in_list_view": 0,
                "insert_after": "driver_name",
                "label": "Transport Receipt Date",
                "modified": "2020-06-23 16:43:04.427622",
                "name": "Stock Entry-transport_receipt_date"
            },
        ],
        "Stock Entry Detail":[
            {
                "fieldname": "item_weight_details",
                "fieldtype": "Section Break",
                "in_list_view": 0,
                "insert_after": "sample_quantity",
                "label": "Item Weight Details",
                "modified": "2020-06-30 15:34:01.228484",
                "name": "Stock Entry Detail-item_weight_details"
            },
            {
                "fetch_from": "item_code.weight_per_unit",
                "fieldname": "weight_per_unit",
                "fieldtype": "Float",
                "in_list_view": 0,
                "insert_after": "item_weight_details",
                "label": "Weight Per Unit",
                "modified": "2020-06-30 15:34:01.669365",
                "name": "Stock Entry Detail-weight_per_unit",
                "read_only": 1
            },
            {
                "fieldname": "total_weight",
                "fieldtype": "Float",
                "in_list_view": 0,
                "insert_after": "weight_per_unit",
                "label": "Total Weight",
                "modified": "2020-06-30 15:34:02.259714",
                "name": "Stock Entry Detail-total_weight",
                "read_only": 1
            },
            {
                "fieldname": "column_break_32",
                "fieldtype": "Column Break",
                "in_list_view": 0,
                "insert_after": "total_weight",
                "label": "",
                "modified": "2020-06-30 15:34:02.814827",
                "name": "Stock Entry Detail-column_break_32"
            },
            {
                "fetch_from": "item_code.weight_uom",
                "fieldname": "weight_uom",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "column_break_32",
                "label": "Weight UOM",
                "modified": "2020-06-30 15:34:03.282211",
                "name": "Stock Entry Detail-weight_uom",
                "options": "UOM",
                "read_only": 1
            },
        ],
        "Stock Reconciliation":[
            {
                "depends_on": "eval:doc.docstatus == 0",
                "fieldname": "sort_items",
                "fieldtype": "Button",
                "in_list_view": 0,
                "insert_after": "items",
                "label": "Sort Items",
                "modified": "2020-07-17 23:53:18.064909",
                "name": "Stock Reconciliation-sort_items"
            },
        ],
        "Stock Reconciliation Item":[
            {
                "fieldname": "material_request",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "amount",
                "label": "Material Request",
                "modified": "2020-06-24 22:55:04.777565",
                "name": "Stock Reconciliation Item-material_request",
                "options": "Material Request",
                "read_only": 1
            },
        ],
        "Student":[
            {
                "fieldname": "bank",
                "fieldtype": "Select",
                "in_list_view": 0,
                "insert_after": "student_applicant",
                "label": "Bank",
                "modified": "2020-07-21 02:47:58.927966",
                "name": "Student-bank",
                "options": "\n NMB Bank",
                "translatable": 1
            },
        ],
        "Student Applicant":[
            {
                "allow_on_submit": 1,
                "fieldname": "student_applicant_fee",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "paid",
                "label": "Student Applicant Fee",
                "modified": "2020-09-08 18:39:21.143298",
                "name": "Student Applicant-student_applicant_fee",
                "read_only": 1,
                "translatable": 1
            },
            {
                "allow_on_submit": 1,
                "fieldname": "bank_reference",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "student_applicant_fee",
                "label": "Bank Reference",
                "modified": "2020-09-08 18:39:21.460847",
                "name": "Student Applicant-bank_reference",
                "read_only": 1,
                "translatable": 1
            },
            {
                "fieldname": "fee_structure",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "application_date",
                "label": "Fee Structure",
                "modified": "2020-09-08 18:38:13.430256",
                "name": "Student Applicant-fee_structure",
                "options": "Fee Structure",
                "reqd": 1
            },
            {
                "fieldname": "program_enrollment",
                "fieldtype": "Link",
                "in_list_view": 0,
                "insert_after": "fee_structure",
                "label": "Program Enrollment",
                "modified": "2020-09-08 21:42:34.633789",
                "name": "Student Applicant-program_enrollment",
                "options": "Program Enrollment"
            },
        ],
        "Supplier":[
            {
                "bold": 1,
                "fieldname": "vrn",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "tax_id",
                "label": "VRN",
                "modified": "2019-01-04 10:14:48.458823",
                "name": "Supplier-vrn",
                "translatable": 1
            },
        ],
        "Vehicle":[
            {
                "name": "Vehicle-csf_tz_acquisition_odometer",
                "modified_by": "Administrator",
                "module_def": "CSF TZ",
                "label": "Acquisition Odometer",
                "fieldname": "csf_tz_acquisition_odometer",
                "insert_after": "acquisition_date",
                "fieldtype": "Int",
            },
            {
                "name": "Vehicle-csf_tz_year",
                "owner": "Administrator",
                "modified": "2022-07-09 03:26:47.982299",
                "modified_by": "Administrator",
                "module_def": "CSF TZ",
                "label": "Manufacturing Year",
                "fieldname": "csf_tz_year",
                "insert_after": "model",
                "fieldtype": "Int",
            },
            {
                "name": "Vehicle-csf_tz_engine_number",
                "modified": "2022-07-09 11:27:38.710494",
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
                "modified": "2020-12-10 10:50:48.832611",
                "name": "Vehicle Fine Record-fully_paid"
            },
        ],
        "Vehicle Log":[
            {
                "fieldname": "column_break_11",
                "fieldtype": "Column Break",
                "in_list_view": 0,
                "insert_after": "odometer",
                "label": "",
                "modified": "2020-08-20 16:46:46.909608",
                "name": "Vehicle Log-column_break_11"
            },
            {
                "fieldname": "trip_destination",
                "fieldtype": "Data",
                "in_list_view": 1,
                "in_standard_filter": 1,
                "insert_after": "column_break_11",
                "label": "Trip Destination",
                "modified": "2020-08-20 16:46:47.646836",
                "name": "Vehicle Log-trip_destination",
                "reqd": 1
            },
            {
                "fieldname": "destination_description",
                "fieldtype": "Data",
                "in_list_view": 0,
                "insert_after": "trip_destination",
                "label": "Destination Description",
                "modified": "2020-08-20 16:46:48.115791",
                "name": "Vehicle Log-destination_description",
                "translatable": 1
            },
        ],
        "Vehicle Service":[
            {
                "fieldname": "spare_name",
                "fieldtype": "Data",
                "in_list_view": 1,
                "label": "Spare Name",
                "modified": "2020-09-03 21:04:45.705267",
                "name": "Vehicle Service-spare_name"
            },
            {
                "fieldname": "quantity",
                "fieldtype": "Float",
                "in_list_view": 1,
                "insert_after": "spare_name",
                "label": "Quantity",
                "modified": "2020-09-03 21:04:45.981769",
                "name": "Vehicle Service-quantity",
                "precision": "2"
            },
            {
                "allow_on_submit": 1,
                "fieldname": "invoice",
                "fieldtype": "Link",
                "in_list_view": 1,
                "insert_after": "type",
                "label": "Invoice",
                "modified": "2020-09-03 21:04:46.285638",
                "name": "Vehicle Service-invoice",
                "options": "Purchase Invoice"
            }
        ]
    }
create_custom_fields(fields, update=True)


