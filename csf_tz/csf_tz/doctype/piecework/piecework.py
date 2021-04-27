# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from csf_tz.csf_tz.doctype.piecework_single.piecework_single import (
    validate_additional_salary,
)


class Piecework(Document):
    def before_submit(self):
        create_additional_salaries(self)

    def before_cancel(self):
        validate_additional_salary(self)

    def validate(self):
        self.total = self.quantity * frappe.db.get_value(
            "Piecework Type", self.task, "rate"
        )
        employees = []
        amount = self.total / len(self.employees)
        for row in self.employees:
            if row.employee not in employees:
                employees.append(row.employee)
                row.amount = amount
            else:
                frappe.throw(
                    "The employee '{0}' is this duplicate in the table in row {1}".format(
                        row.employee, row.idx
                    )
                )


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
