from __future__ import unicode_literals
import frappe
from frappe import _
from csf_tz import console
from frappe.utils import today, date_diff, flt


def validate(doc, method):
    loan_type = frappe.get_doc("Loan Type", doc.loan_type)
    base_salary = get_base_salary(doc.applicant, today())
    if loan_type.loan_factor and base_salary:
        if doc.loan_amount > loan_type.loan_factor * base_salary:
            frappe.throw(_("Loan Amount should not be grater then {0}".format(
                flt(loan_type.loan_factor * base_salary, 2))))
    if loan_type.ristrict_to_date:
        loan_last_date = doc.repayment_schedule[len(
            doc.repayment_schedule)-1].payment_date
        contract_end_date = frappe.get_value(
            "Employee", doc.applicant, "contract_end_date")
        diff = date_diff(contract_end_date, loan_last_date)
        console(diff)
        if diff < 0:
            frappe.throw(
                _("Loan Last Payment Date should not after {0}".format(contract_end_date)))


def get_base_salary(employee, on_date):
    if not employee or not on_date:
        return None
    base = frappe.db.sql("""
		select base from `tabSalary Structure Assignment`
		where employee=%(employee)s
		and docstatus = 1
		and %(on_date)s >= from_date order by from_date desc limit 1""", {
        'employee': employee,
        'on_date': on_date,
    })
    return base[0][0] if base else None
