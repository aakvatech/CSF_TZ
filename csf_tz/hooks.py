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



# Override Document Class
override_doctype_class = {
	'Salary Slip': 'csf_tz.overrides.salary_slip.SalarySlip',
}

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
    "Sales Invoice": ["csf_tz/sales_invoice.js", "authotp/api/sales_invoice.js"],
    "Sales Order": "csf_tz/sales_order.js",
    "Delivery Note": "csf_tz/delivery_note.js",
    "Customer": ["csf_tz/customer.js","authotp/api/customer.js"],
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
    "Additional Salary": "csf_tz/additional_salary.js",
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
        "before_submit": [
            "csf_tz.authotp.api.sales_invoice.before_submit",
        ],
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
        "before_insert": "csf_tz.custom_api.batch_splitting",
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
        # Routine for every day 3:30am at night
        "30 3 * * *": [
            "csf_tz.custom_api.auto_close_dn",
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

jinja = {"methods": ["csf_tz.custom_api.generate_qrcode"]}

# Testing
# -------

# before_tests = "csf_tz.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
override_whitelisted_methods = {
    "frappe.desk.query_report.get_script": "csf_tz.csftz_hooks.query_report.get_script"
}
