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
	{"doctype":"Custom Field", "filters": [["name", "in", (
		"Supplier-vrn",
		"Customer-vrn",
		"Company-vrn",
		"Company-p_o_box",
		"Company-city",
		"Company-street",
		"Company-block_number",
		"Company-plot_number",
		"Company-company_bank_details",
		"Company-section_break_12",
		"Journal Entry-to_date",
		"Journal Entry-from_date",
		"Payment Entry Reference-section_break_9",
		"Payment Entry Reference-posting_date",
		"Payment Entry Reference-end_date",
		"Sales Invoice-witholding_tax_certificate_number",
		"Purchase Invoice Item-withholding_tax_rate",
		"Sales Invoice Item-withholding_tax_rate",
		"Payment Entry Reference-start_date",
		"Sales Invoice-column_break_29",
		"Sales Invoice-tra_control_number",
		"Sales Invoice-statutory_details",
		"Sales Order-cost_center",
		"Sales Order-posting_date",
		"Purchase Order-posting_date",
		"Sales Invoice-electronic_fiscal_device",
		"Sales Invoice-efd_z_report",
		"POS Profile-column_break_1",
		"POS Profile-electronic_fiscal_device",
		"Item-witholding_tax_rate_on_purchase",
		"Company-max_records_in_dialog",
		"Stock Entry-repack_template",
		"Stock Entry-repack_qty",
		"Stock Entry-item_uom",
		"Account-item",
		"Purchase Invoice-expense_record",
		"Journal Entry-expense_record",
		"Sales Invoice Item-allow_over_sell",
		"Sales Invoice-delivery_status",
		"Sales Invoice Item-delivery_status",
		"Stock Entry-final_destination",
		"Stock Entry-transport_receipt_date",
		"Stock Entry-driver_name",
		"Stock Entry-transporter_name",
		"Stock Entry-column_break_69",
		"Stock Entry-vehicle_no",
		"Stock Entry-transport_receipt_no",
		"Stock Entry-driver",
		"Stock Entry-transporter",
		"Stock Entry-transporter_info",
		"Stock Entry-transporter_info",
		"Stock Entry-transporter_info",
		"Material Request Item-stock_reconciliation",
		"Stock Reconciliation Item-material_request",
		"Sales Invoice-price_reduction",
		"Delivery Note-form_sales_invoice",
		"Stock Entry-total_net_weight",
		"Stock Entry Detail-item_weight_details",
		"Stock Entry Detail-weight_per_unit",
		"Stock Entry Detail-total_weight",
		"Stock Entry Detail-column_break_32",
		"Stock Entry Detail-weight_uom",
		"Sales Invoice Item-allow_override_net_rate",
		"Company-default_withholding_payable_account",
		"Purchase Invoice Item-withholding_tax_entry",
		"Company-enabled_auto_create_delivery_notes",
		"Stock Reconciliation-sort_items",
		"Student-bank",
		"Fees-callback_token",
		"Company-nmb_series",
		"Company-nmb_password",
		"Company-nmb_username",
		"Company-withholding_section",
		"Company-auto_submit_for_purchase_withholding",
		"Company-column_break_55",
		"Company-default_withholding_receivable_account",
		"Company-auto_submit_for_sales_withholding",
		"Item-withholding_tax_rate_on_sales",
		"Sales Invoice Item-withholding_tax_entry",
		"Company-nmb_url",
		"Fees-bank_reference",
		"Fees-abbr",
		"Sales Invoice-enabled_auto_create_delivery_notes",
		"Company-education_section",
		"Company-send_fee_details_to_bank",
		"Company-column_break_60",
		"Company-auto_create_for_sales_withholding",
		"Company-auto_create_for_purchase_withholding",
		"Company-fee_bank_account",
		"Company-student_applicant_fees_revenue_account",
		"Student Applicant-fee_structure",
		"Student Applicant-student_applicant_fee",
		"Student Applicant-bank_reference",
		"Student Applicant-program_enrollment",
		"Company-bypass_material_request_validation",
		"Operation-image",
		"Employee-attachments",
		"Employee-files",
		"Fees-base_grand_total",
		"Fees-advance_paid",
		"Sales Invoice-default_item_discount",
	)]]},
	{"doctype":"Property Setter", "filters": [["name", "in", (
		"Sales Invoice-pos_profile-in_standard_filter",
		"Sales Invoice-posting_date-in_list_view",
		"Sales Invoice-is_pos-in_standard_filter",
		"Payment Reconciliation Payment-posting_date-in_list_view",
		"Payment Reconciliation Payment-posting_date-columns",
		"Payment Entry Reference-reference_doctype-in_list_view",
		"Payment Entry Reference-reference_name-columns",
		"Payment Entry Reference-reference_doctype-columns",
		"Payment Entry Reference-due_date-columns",
		"Payment Entry Reference-due_date-width",
		"Customer-tax_id-label",
		"Bank Reconciliation Detail-posting_date-in_list_view",
		"Bank Reconciliation Detail-posting_date-columns",
		"Bank Reconciliation Detail-payment_entry-columns",
		"Payment Entry-section_break_12-collapsible",
		"Payment Entry-payment_accounts_section-collapsible",
		"Stock Entry-from_warehouse-fetch_from",
		"Student Applicant-application_status-options",
		"Student Applicant-application_status-read_only",
		"Operation-image_field",
		"Document Attachment-attachment-in_list_view",
	)]]},
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/csf_tz/css/csf_tz.css"
# app_include_js = "/assets/csf_tz/js/csf_tz.js"
app_include_js = [
	"/assets/js/select_dialog.min.js",
	"/assets/js/to_console.min.js",
	"/assets/csf_tz/js/jobcards.min.js",
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
	"Payment Entry" : "csf_tz/payment_entry.js",
	"Sales Invoice" : "csf_tz/sales_invoice.js",
	"Sales Order" : "csf_tz/sales_order.js",
	"Delivery Note" : "csf_tz/delivery_note.js",
	"Customer" : "csf_tz/customer.js",
	"Supplier" : "csf_tz/supplier.js",
	"Stock Entry" : "csf_tz/stock_entry.js",
	"Account" : "csf_tz/account.js",
	"Asset" : "csf_tz/asset.js",
	"Warehouse" : "csf_tz/warehouse.js",
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
#	"Role": "home_page"
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
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Open Invoice Exchange Rate Revaluation": {
		"validate": "csf_tz.custom_api.getInvoiceExchangeRate"
	},
	"Sales Invoice": {
		"on_submit":[
			'csf_tz.custom_api.validate_net_rate',
			"csf_tz.custom_api.create_delivery_note",
			'csf_tz.custom_api.check_submit_delivery_note',
			'csf_tz.custom_api.make_withholding_tax_gl_entries_for_sales',
			],
		'validate': [
			'csf_tz.custom_api.check_validate_delivery_note',
			'csf_tz.custom_api.validate_items_remaining_qty',
			'csf_tz.custom_api.calculate_price_reduction',
			],
		'before_cancel': 'csf_tz.custom_api.check_cancel_delivery_note',
	},
	'Delivery Note': {
		'on_submit': 'csf_tz.custom_api.update_delivery_on_sales_invoice',
		'before_cancel': 'csf_tz.custom_api.update_delivery_on_sales_invoice',
  },
	"Account": {
		"on_update":"csf_tz.custom_api.create_indirect_expense_item",
		"after_insert":"csf_tz.custom_api.create_indirect_expense_item",
	},
	"Purchase Invoice": {
		"on_submit":"csf_tz.custom_api.make_withholding_tax_gl_entries_for_purchase",
	},
	"Fees": {
		"before_insert":"csf_tz.custom_api.set_fee_abbr",
		"after_insert":"csf_tz.bank_api.set_callback_token",
		"on_submit":"csf_tz.bank_api.invoice_submission",
		"before_cancel":"csf_tz.bank_api.cancel_invoice",
	},
	"Program Enrollment": {
		"onload":"csf_tz.csftz_hooks.program_enrollment.create_course_enrollments_override",
		"refresh":"csf_tz.csftz_hooks.program_enrollment.create_course_enrollments_override",
		"reload":"csf_tz.csftz_hooks.program_enrollment.create_course_enrollments_override",
		"before_submit":"csf_tz.csftz_hooks.program_enrollment.validate_submit_program_enrollment",
	},
	"*": {
		"validate"                      :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"onload"                        :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_insert"                 :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"after_insert"                  :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_naming"                 :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_change"                 :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_update_after_submit"    :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_validate"               :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_save"                   :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_update"                     :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"before_submit"                 :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"autoname"                      :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_cancel"                     :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_trash"                      :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_submit"                     :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_update_after_submit"        :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
		"on_change"                     :  ["csf_tz.csf_tz.doctype.visibility.visibility.run_visibility"],
	},
	"Stock Entry": {
		"validate": "csf_tz.custom_api.calculate_total_net_weight",
	},
	"Student Applicant": {
		"on_update_after_submit":"csf_tz.csftz_hooks.student_applicant.make_student_applicant_fees",
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"csf_tz.tasks.all"
	# ],
	"daily": [
		"csf_tz.custom_api.create_delivery_note_for_all_pending_sales_invoice",
		"csf_tz.csf_tz.doctype.visibility.visibility.trigger_daily_alerts",
		"csf_tz.csf_tz.doctype.vehicle_fine_record.vehicle_fine_record.check_fine_all_vehicles",
		"csf_tz.bank_api.reconciliation",
	],
	# "hourly": [
	# 	"csf_tz.tasks.hourly"
	# ],
	"weekly": [
		"csf_tz.custom_api.make_stock_reconciliation_for_all_pending_material_request"
	]
	# "monthly": [
	# 	"csf_tz.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "csf_tz.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "csf_tz.event.get_events"
# }

