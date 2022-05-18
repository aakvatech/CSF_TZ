# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import flt


class EFDZReport(Document):
    def validate(self):
        if not self.efd_z_report_invoices:
            frappe.throw(_("No Sales Invoie Found in the table"))
        if flt(self.total_turnover, 2) != flt(self.total_turnover_ticked, 2):
            frappe.throw(_("Sales Invoice Amount is not equal to Money Entered"))
        if flt(self.net_amount, 2) != flt(self.total_excluding_vat_ticked, 2):
            frappe.throw(
                _("Total Excluding VAT is not equal to Total Excluding VAT (Ticked)")
            )
        if flt(self.total_vat, 2) != flt(self.total_vat_ticked, 2):
            frappe.throw(_("Total VAT is not equal to Total VAT (Ticked)"))
        if flt(self.total_turnover_ex_sr, 2) != flt(
            self.total_turnover_exempted__sp_relief_ticked, 2
        ):
            frappe.throw(
                _(
                    "Total Turnover Exempted / Sp. Relief is not equal to Total Turnover Exempted / Sp. Relief (Ticked)"
                )
            )
        if self.get_number_of_ticked() != self.receipts_issued:
            frappe.throw(
                _(
                    "The Number of Sales Invoice (Include is checked) in the table is not equal to Receipts Issued"
                )
            )

    def get_number_of_ticked(self):
        total_checked = 0
        for i in self.efd_z_report_invoices:
            if i.include:
                total_checked += 1
        return total_checked

    @frappe.whitelist()
    def get_sales_invoice(self):

        date = datetime.strptime(
            str(self.z_report_date_time), "%Y-%m-%d %H:%M:%S"
        ).date()
        time = datetime.strptime(
            str(self.z_report_date_time), "%Y-%m-%d %H:%M:%S"
        ).time()

        condition = (
            "docstatus = 1  and (efd_z_report = '' OR efd_z_report is null) and status !='Return' and posting_date <= '"
            + str(date)
            + "' and IF(IF(posting_date = '"
            + str(date)
            + "', IF(posting_time < '"
            + str(time)
            + "',1,'PostingTime'),'PostingDate') = 1 or IF(posting_date = '"
            + str(date)
            + "',IF(posting_time < '"
            + str(time)
            + "',1,'PostingTime'),'PostingDate') = 'PostingDate',1,0)"
        )

        condition += (
            " and ( electronic_fiscal_device = '" + self.electronic_fiscal_device + "'"
            "or electronic_fiscal_device is null or electronic_fiscal_device = '')"
        )

        query = """ select *
                        from `tabSales Invoice`
                        where {0}""".format(
            condition
        )

        sales_invoices = frappe.db.sql(query, as_dict=True)

        if not sales_invoices:
            frappe.throw("No Sales Invoice Fetch")

        for i in sales_invoices:
            if i.base_total_taxes_and_charges == 0:
                amt_ex__sr = i.base_total
            else:
                if i.base_net_total != i.base_total:
                    amt_ex__sr = i.base_grand_total - (
                        i.base_net_total + i.base_total_taxes_and_charges
                    )
                else:
                    amt_ex__sr = i.base_grand_total - (
                        (i.base_total_taxes_and_charges / 0.18)
                        + i.base_total_taxes_and_charges
                    )
            if amt_ex__sr < 0:
                amt_ex__sr = 0
            self.append(
                "efd_z_report_invoices",
                {
                    "invoice_number": i.name,
                    "invoice_date": i.posting_date,
                    "amt_excl_vat": flt((i.base_net_total + i.base_rounding_adjustment), 2),
                    "vat": flt(i.base_total_taxes_and_charges, 2),
                    "amt_ex__sr": amt_ex__sr,
                    "invoice_amount": flt(i.base_rounded_total, 2),
                    "invoice_currency": i.currency,
                },
            )
        return True

    def before_submit(self):
        to_remove = []
        for invoice in self.efd_z_report_invoices:
            if not invoice.include:
                to_remove.append(invoice)
            else:
                invoice_doc = frappe.get_doc("Sales Invoice", invoice.invoice_number)
                if invoice_doc.efd_z_report:
                    frappe.throw(
                        _(
                            "The Sales Invoice {0} is linked to EFD Z Report {1}".format(
                                invoice.invoice_number, invoice_doc.efd_z_report
                            )
                        )
                    )
                else:
                    invoice_doc.efd_z_report = self.name
                    invoice_doc.flags.ignore_permissions = True
                    invoice_doc.save()
        [self.remove(invoice) for invoice in to_remove]

    def on_cancel(self):
        for invoice in self.efd_z_report_invoices:
            if invoice.include:
                invoice_doc = frappe.get_doc("Sales Invoice", invoice.invoice_number)
                if invoice_doc.efd_z_report:
                    invoice_doc.efd_z_report = ""
                    invoice_doc.flags.ignore_permissions = True
                    invoice_doc.save()
