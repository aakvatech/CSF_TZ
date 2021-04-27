# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class PieceworkSingle(Document):
    def before_submit(self):
        create_additional_salaries(self)

    def before_cancel(self):
        validate_additional_salary(self)


def create_additional_salaries(doc):
    for row in doc.employees:
        if row.employee and row.amount:
            as_doc = frappe.new_doc("Additional Salary")
            as_doc.employee = row.employee
            as_doc.salary_component = "Piecework"
            as_doc.amount = row.amount
            as_doc.payroll_date = doc.date
            as_doc.company = doc.company
            as_doc.overwrite_salary_structure_amount = 0
            as_doc.insert(ignore_permissions=True)
            row.additional_salary = as_doc.name
            as_doc.submit()
            frappe.msgprint(
                _("Additional Salary {0} created for employee {1}").format(
                    as_doc.name, row.employee
                ),
                alert=True,
            )


def validate_additional_salary(doc):
    for row in doc.employees:
        status = frappe.get_value(
            "Additional Salary", row.additional_salary, "docstatus"
        )
        if status == 1:
            frappe.throw(
                _(
                    "Pieceworks cannot be cancelled once the Payroll Entry / Additional Salary {0} is submited"
                ).format(row.additional_salary)
            )
