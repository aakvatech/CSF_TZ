# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "csf_tz"
app_title = "CSF TZ"
app_publisher = "Aakvatech"
app_description = "Country Specific Functionality Tanzania"
app_icon = "octicon octicon-bookmark"
app_color = "green"
app_email = "info@aakvatech.com"
app_license = "GNU General Public License (v3)"

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Account-item",
                    "Address-is_your_company_address",
                    "Address-tax_category",
                    "BOM-column_break_15",
                    "BOM-fg_warehouse",
                    "BOM-scrap_warehouse",
                    "BOM-source_warehouse",
                    "BOM-warehouses",
                    "BOM-wip_warehouse",
                    "Company-auto_create_for_purchase_withholding",
                    "Company-auto_create_for_sales_withholding",
                    "Company-auto_submit_for_purchase_withholding",
                    "Company-auto_submit_for_sales_withholding",
                    "Company-block_number",
                    "Company-bypass_material_request_validation",
                    "Company-city",
                    "Company-column_break_55",
                    "Company-column_break_60",
                    "Company-company_bank_details",
                    "Company-default_item_tax_template",
                    "Company-default_withholding_payable_account",
                    "Company-default_withholding_receivable_account",
                    "Company-education_section",
                    "Company-enabled_auto_create_delivery_notes",
                    "Company-fee_bank_account",
                    "Company-max_records_in_dialog",
                    "Company-nmb_password",
                    "Company-nmb_series",
                    "Company-nmb_url",
                    "Company-nmb_username",
                    "Company-p_o_box",
                    "Company-plot_number",
                    "Company-section_break_12",
                    "Company-send_fee_details_to_bank",
                    "Company-street",
                    "Company-student_applicant_fees_revenue_account",
                    "Company-tin",
                    "Company-vrn",
                    "Company-withholding_section",
                    "Contact-is_billing_contact",
                    "Custom DocPerm-dependent",
                    "Customer-vrn",
                    "Delivery Note-form_sales_invoice",
                    "Employee-old_employee_id",
                    "Fee Structure-default_fee_category",
                    "Fees-abbr",
                    "Fees-bank_reference",
                    "Fees-callback_token",
                    "Fees-from_date",
                    "Fees-to_date",
                    "Item-default_tax_template",
                    "Item-excisable_item",
                    "Item-withholding_tax_rate_on_sales",
                    "Item-witholding_tax_rate_on_purchase",
                    "Journal Entry-expense_record",
                    "Journal Entry-from_date",
                    "Journal Entry-import_file",
                    "Journal Entry-to_date",
                    "Landed Cost Voucher-import_file",
                    "Material Request Item-stock_reconciliation",
                    "Operation-image",
                    "Payment Entry Reference-end_date",
                    "Payment Entry Reference-posting_date",
                    "Payment Entry Reference-section_break_9",
                    "Payment Entry Reference-start_date",
                    "POS Profile-column_break_1",
                    "POS Profile-electronic_fiscal_device",
                    "Print Settings-compact_item_print",
                    "Print Settings-print_taxes_with_zero_amount",
                    "Program Fee-default_fee_category",
                    "Program-fees",
                    "Program-program_fee",
                    "Purchase Invoice Item-withholding_tax_entry",
                    "Purchase Invoice Item-withholding_tax_rate",
                    "Purchase Invoice-expense_record",
                    "Purchase Invoice-import_file",
                    "Purchase Invoice-reference",
                    "Purchase Order-posting_date",
                    "Sales Invoice Item-allow_over_sell",
                    "Sales Invoice Item-allow_override_net_rate",
                    "Sales Invoice Item-delivery_status",
                    "Sales Invoice Item-withholding_tax_entry",
                    "Sales Invoice Item-withholding_tax_rate",
                    "Sales Invoice Payment-payment_reference",
                    "Sales Invoice-column_break_29",
                    "Sales Invoice-default_item_discount",
                    "Sales Invoice-default_item_tax_template",
                    "Sales Invoice-delivery_status",
                    "Sales Invoice-efd_z_report",
                    "Sales Invoice-electronic_fiscal_device",
                    "Sales Invoice-enabled_auto_create_delivery_notes",
                    "Sales Invoice-excise_duty_applicable",
                    "Sales Invoice-previous_invoice_number",
                    "Sales Invoice-price_reduction",
                    "Sales Invoice-section_break_80",
                    "Sales Invoice-statutory_details",
                    "Sales Invoice-tra_control_number",
                    "Sales Invoice-witholding_tax_certificate_number",
                    "Sales Order-cost_center",
                    "Sales Order-default_item_discount",
                    "Sales Order-posting_date",
                    "Stock Entry Detail-column_break_32",
                    "Stock Entry Detail-item_weight_details",
                    "Stock Entry Detail-total_weight",
                    "Stock Entry Detail-weight_per_unit",
                    "Stock Entry Detail-weight_uom",
                    "Stock Entry-column_break_69",
                    "Stock Entry-driver_name",
                    "Stock Entry-driver",
                    "Stock Entry-final_destination",
                    "Stock Entry-item_uom",
                    "Stock Entry-repack_qty",
                    "Stock Entry-repack_template",
                    "Stock Entry-total_net_weight",
                    "Stock Entry-transport_receipt_date",
                    "Stock Entry-transport_receipt_no",
                    "Stock Entry-transporter_info",
                    "Stock Entry-transporter_name",
                    "Stock Entry-transporter",
                    "Stock Entry-vehicle_no",
                    "Stock Reconciliation Item-material_request",
                    "Stock Reconciliation-sort_items",
                    "Student Applicant-bank_reference",
                    "Student Applicant-fee_structure",
                    "Student Applicant-program_enrollment",
                    "Student Applicant-student_applicant_fee",
                    "Student-bank",
                    "Supplier-vrn",
                    "Vehicle Fine Record-fully_paid",
                    "Vehicle Log-column_break_11",
                    "Vehicle Log-destination_description",
                    "Vehicle Log-trip_destination",
                    "Vehicle Service-invoice",
                    "Vehicle Service-quantity",
                    "Vehicle Service-spare_name",
                    "Fees-base_grand_total",
                    "Fees-advance_paid",
                    "Employee-employee_salary_component_limits",
                    "Employee-employee_salary_component_limit",
                    "Employee-heslb_f4_index_number",
                    "Sales Invoice Item-is_ignored_in_pending_qty",
                ),
            ]
        ],
    },
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                (
                    "Account-search_fields",
                    "Bank Reconciliation Detail-payment_entry-columns",
                    "Bank Reconciliation Detail-posting_date-columns",
                    "Bank Reconciliation Detail-posting_date-in_list_view",
                    "Budget-budget_against-options",
                    "Comment-main-track_changes",
                    "Customer-main-search_fields",
                    "Customer-tax_id-label",
                    "Delivery Note-items-allow_bulk_edit",
                    "Document Attachment-attachment-in_list_view",
                    "Energy Point Log-main-track_changes",
                    "Healthcare Insurance Claim-main-track_changes",
                    "Healthcare Service Order-main-track_changes",
                    "Item Price-brand-in_list_view",
                    "Item Price-price_list-in_list_view",
                    "Item Price-valid_from-in_list_view",
                    "Journal Entry Account-account-width",
                    "Journal Entry Account-accounting_dimensions_section-collapsible",
                    "Journal Entry Account-party_type-columns",
                    "Journal Entry Account-party-columns",
                    "Journal Entry Account-reference_name-in_list_view",
                    "Journal Entry-accounts-allow_bulk_edit",
                    "Journal Entry-total_amount-in_list_view",
                    "Journal Entry-total_debit-in_list_view",
                    "Notification Log-main-track_changes",
                    "Operation-image_field",
                    "Payment Entry Reference-due_date-columns",
                    "Payment Entry Reference-due_date-width",
                    "Payment Entry Reference-reference_doctype-columns",
                    "Payment Entry Reference-reference_doctype-in_list_view",
                    "Payment Entry Reference-reference_name-columns",
                    "Payment Entry-letter_head-fetch_from",
                    "Payment Entry-payment_accounts_section-collapsible",
                    "Payment Entry-section_break_12-collapsible",
                    "Payment Reconciliation Payment-posting_date-columns",
                    "Payment Reconciliation Payment-posting_date-in_list_view",
                    "Payment Schedule-payment_amount-options",
                    "Piecework Type-search_fields",
                    "Purchase Invoice Item-cost_center-default",
                    "Purchase Order-letter_head-fetch_from",
                    "Report-javascript-depends_on",
                    "Route History-main-track_changes",
                    "Sales Invoice Item-batch_no-in_list_view",
                    "Sales Invoice Item-cost_center-columns",
                    "Sales Invoice Item-cost_center-in_list_view",
                    "Sales Invoice Item-item_code-columns",
                    "Sales Invoice Item-item_tax_template-default",
                    "Sales Invoice Item-item_tax_template-fetch_if_empty",
                    "Sales Invoice Item-qty-columns",
                    "Sales Invoice Item-warehouse-in_list_view",
                    "Sales Invoice-is_pos-in_standard_filter",
                    "Sales Invoice-letter_head-fetch_from",
                    "Sales Invoice-letter_head-fetch_if_empty",
                    "Sales Invoice-loyalty_points_redemption-depends_on",
                    "Sales Invoice-pos_profile-in_standard_filter",
                    "Sales Invoice-posting_date-in_list_view",
                    "Sales Invoice-search_fields",
                    "Scheduled Job Log-main-track_changes",
                    "Stock Entry-from_warehouse-fetch_from",
                    "Student Applicant-application_status-options",
                    "Student Applicant-application_status-read_only",
                    "Supplier-read_only_onload",
                    "Supplier-tax_id-bold",
                    "Supplier-tax_id-label",
                    "Vehicle Log-date-default",
                    "Vehicle Log-date-in_list_view",
                    "Vehicle Log-employee-fetch_from",
                    "Vehicle Log-employee-fetch_if_empty",
                    "Vehicle Log-license_plate-in_standard_filter",
                    "Vehicle Log-odometer-in_list_view",
                    "Vehicle Log-quick_entry",
                    "Vehicle Service-frequency-in_list_view",
                    "Vehicle Service-frequency-options",
                    "Vehicle Service-service_item-in_list_view",
                    "Vehicle Service-service_item-options",
                    "Vehicle Service-type-options",
                    "Workflow Action-main-track_changes",
                ),
            ]
        ],
    },
]

# Override Document Class
# override_doctype_class = {
# 	'Salary Slip': 'csf_tz.overrides.csftz_SalarySlip'
# }

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/csf_tz/css/csf_tz.css"
# app_include_js = "/assets/csf_tz/js/csf_tz.js"
app_include_js = [
    "/assets/js/select_dialog.min.js",
    "/assets/js/to_console.min.js",
    "/assets/js/jobcards.min.js",
    "/assets/csf_tz/node_modules/vuetify/dist/vuetify.js",
]

app_include_css = "/assets/csf_tz/css/theme.css"
web_include_css = "/assets/csf_tz/css/theme.css"
# include js, css files in header of web template
# web_include_css = "/assets/csf_tz/css/csf_tz.css"
# web_include_js = "/assets/csf_tz/js/csf_tz.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Payment Entry": "csf_tz/payment_entry.js",
    "Sales Invoice": "csf_tz/sales_invoice.js",
    "Sales Order": "csf_tz/sales_order.js",
    "Delivery Note": "csf_tz/delivery_note.js",
    "Customer": "csf_tz/customer.js",
    "Supplier": "csf_tz/supplier.js",
    "Stock Entry": "csf_tz/stock_entry.js",
    "Account": "csf_tz/account.js",
    "Warehouse": "csf_tz/warehouse.js",
    "Company": "csf_tz/company.js",
    "Stock Reconciliation": "csf_tz/stock_reconciliation.js",
    "Fees": "csf_tz/fees.js",
    "Program Enrollment Tool": "csf_tz/program_enrollment_tool.js",
    "Purchase Invoice": "csf_tz/purchase_invoice.js",
    "Quotation": "csf_tz/quotation.js",
    "Purchase Receipt": "csf_tz/purchase_receipt.js",
    "Purchase Order": "csf_tz/purchase_order.js",
    "Student Applicant": "csf_tz/student_applicant.js",
    "Bank Reconciliation": "csf_tz/bank_reconciliation.js",
    "Program Enrollment": "csf_tz/program_enrollment.js",
    "Payroll Entry": "csf_tz/payroll_entry.js",
    "Salary Slip": "csf_tz/salary_slip.js",
    "Landed Cost Voucher": "csf_tz/landed_cost_voucher.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "csf_tz.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "csf_tz.install.before_install"
# after_install = "csf_tz.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "csf_tz.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Open Invoice Exchange Rate Revaluation": {
        "validate": "csf_tz.custom_api.getInvoiceExchangeRate"
    },
    "Sales Invoice": {
        "on_submit": [
            "csf_tz.custom_api.validate_net_rate",
            "csf_tz.custom_api.create_delivery_note",
            "csf_tz.custom_api.check_submit_delivery_note",
            "csf_tz.custom_api.make_withholding_tax_gl_entries_for_sales",
        ],
        "validate": [
            "csf_tz.custom_api.check_validate_delivery_note",
            "csf_tz.custom_api.validate_items_remaining_qty",
            "csf_tz.custom_api.calculate_price_reduction",
        ],
        "before_cancel": "csf_tz.custom_api.check_cancel_delivery_note",
    },
    "Delivery Note": {
        "on_submit": "csf_tz.custom_api.update_delivery_on_sales_invoice",
        "before_cancel": "csf_tz.custom_api.update_delivery_on_sales_invoice",
    },
    "Account": {
        "on_update": "csf_tz.custom_api.create_indirect_expense_item",
        "after_insert": "csf_tz.custom_api.create_indirect_expense_item",
    },
    "Purchase Invoice": {
        "on_submit": "csf_tz.custom_api.make_withholding_tax_gl_entries_for_purchase",
    },
    "Fees": {
        "before_insert": "csf_tz.custom_api.set_fee_abbr",
        "after_insert": "csf_tz.bank_api.set_callback_token",
        "on_submit": "csf_tz.bank_api.invoice_submission",
        "before_cancel": "csf_tz.custom_api.on_cancel_fees",
    },
    "Program Enrollment": {
        "onload": "csf_tz.csftz_hooks.program_enrollment.create_course_enrollments_override",
        "refresh": "csf_tz.csftz_hooks.program_enrollment.create_course_enrollments_override",
        "reload": "csf_tz.csftz_hooks.program_enrollment.create_course_enrollments_override",
        "before_submit": "csf_tz.csftz_hooks.program_enrollment.validate_submit_program_enrollment",
    },
    "*": {
        "validate": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "onload": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "before_insert": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "after_insert": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "before_naming": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "before_change": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "before_update_after_submit": [
            "csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"
        ],
        "before_validate": [
            "csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"
        ],
        "before_save": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "on_update": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "before_submit": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "autoname": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "on_cancel": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "on_trash": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "on_submit": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
        "on_update_after_submit": [
            "csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"
        ],
        "on_change": ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
    },
    "Stock Entry": {
        "validate": "csf_tz.custom_api.calculate_total_net_weight",
    },
    "Student Applicant": {
        "on_update_after_submit": "csf_tz.csftz_hooks.student_applicant.make_student_applicant_fees",
    },
    "Custom DocPerm": {
        "validate": "csf_tz.csftz_hooks.custom_docperm.grant_dependant_access",
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    # "all": [
    # 	"csf_tz.tasks.all"
    # ],
    "cron": {
        "0 */6 * * *": [
            "csf_tz.csf_tz.doctype.parking_bill.parking_bill.check_bills_all_vehicles",
            "csf_tz.csf_tz.doctype.vehicle_fine_record.vehicle_fine_record.check_fine_all_vehicles",
        ],
        "*/15 * * * *": [
            "csf_tz.csftz_hooks.items_revaluation.process_incorrect_balance_qty"
        ],
        # Routine for every day 3:30 am at night
        "30 3 * * *": [
            "csf_tz.custom_api.auto_closing_delivery_note",
        ],
    },
    "daily": [
        "csf_tz.custom_api.create_delivery_note_for_all_pending_sales_invoice",
        "csf_tz.csf_tz.doctype.visibility.visibility.trigger_daily_alerts",
        "csf_tz.bank_api.reconciliation",
    ],
    # "hourly": [
    # 	"csf_tz.tasks.hourly"
    # ],
    "weekly": [
        "csf_tz.custom_api.make_stock_reconciliation_for_all_pending_material_request"
    ],
    "monthly": [
        # "csf_tz.tasks.monthly",
        "csf_tz.csf_tz.doctype.tz_insurance_cover_note.tz_insurance_cover_note.update_covernote_docs"
    ],
}

jenv = {"methods": ["generate_qrcode:csf_tz.custom_api.generate_qrcode"]}

# Testing
# -------

# before_tests = "csf_tz.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
override_whitelisted_methods = {
    "frappe.desk.query_report.get_script": "csf_tz.csftz_hooks.query_report.get_script"
}
