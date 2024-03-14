# -*- coding: utf-8 -*-
# Copyright (c) 2020, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json
import requests
from frappe.utils import get_host_name, flt
from time import sleep
import binascii
import os
from urllib.parse import quote, urlparse, urlunparse
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from frappe.utils.background_jobs import enqueue
from datetime import datetime
from frappe.utils.password import get_decrypted_password
from csf_tz.csf_tz.doctype.csf_api_response_log.csf_api_response_log import add_log


class ToObject(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)


def set_callback_token(doc, method):
    send_fee_details_to_bank = (
        frappe.get_value("Company", doc.company, "send_fee_details_to_bank") or 0
    )
    if not send_fee_details_to_bank:
        return
    doc.callback_token = binascii.hexlify(os.urandom(14)).decode()
    series = frappe.get_value("Company", doc.company, "nmb_series") or ""
    if not series:
        frappe.throw(_("Please set NMB User Series in Company {0}".format(doc.company)))
    reference = str(series) + "F" + str(doc.name)
    if not doc.abbr:
        doc.abbr = frappe.get_value("Company", doc.company, "abbr") or ""
    doc.bank_reference = reference.replace("-", "").replace("FEE" + doc.abbr, "")
    if method == "invoice_submission":
        doc.save()
        frappe.db.commit()


def get_nmb_token(company):
    url = frappe.get_value("Company", company, "nmb_url")
    if not url:
        frappe.throw(_("Please set NMB URL in Company {0}".format(company)))
    url = url + str("auth")
    username = frappe.get_value("Company", company, "nmb_username")
    if not username:
        frappe.throw(_("Please set NMB User Name in Company {0}".format(company)))
    password = get_decrypted_password("Company", company, "nmb_password")
    if not password:
        frappe.throw(_("Please set NMB Password in Company {0}".format(company)))
    data = {
        "username": username,
        "password": password,
    }
    for i in range(3):
        try:
            r = requests.post(url, data=json.dumps(data), timeout=5)
            r.raise_for_status()
            frappe.logger().debug({"get_nmb_token webhook_success": r.text})
            if json.loads(r.text):
                add_log(
                    request_type="NMB token",
                    request_url=url,
                    request_header="no header",
                    request_body=json.dumps(data),
                    response_data=json.loads(r.text),
                )
            if json.loads(r.text)["status"] == 1:
                return json.loads(r.text)["token"]
            else:
                frappe.throw(json.loads(r.text))
        except Exception as e:
            frappe.logger().debug({"get_nmb_token webhook_error": e, "try": i + 1})
            sleep(3 * i + 1)
            if i != 2:
                continue
            else:
                raise e


def send_nmb(method, data, company):
    url = frappe.get_value("Company", company, "nmb_url")
    if not url:
        frappe.throw(_("Please set NMB URL in Company {0}".format(company)))
    data["token"] = get_nmb_token(company)
    url = url + str(method)
    for i in range(3):
        try:
            r = requests.post(url, data=json.dumps(data), timeout=5)
            r.raise_for_status()
            frappe.logger().debug({"send_nmb webhook_success": r.text})
            if json.loads(r.text):
                add_log(
                    request_type="NMB " + method,
                    request_url=url,
                    request_header="no header",
                    request_body=json.dumps(data),
                    response_data=json.loads(r.text),
                )
            if json.loads(r.text)["status"] == 1:
                frappe.msgprint(
                    "Response from bank:<br><hr>" + json.loads(r.text)["description"]
                )
                return json.loads(r.text)
            else:
                print(json.loads(r.text)["description"])
                if json.loads(r.text)["description"] == "Duplicate Invoice Number":
                    return json.loads(r.text)
                frappe.msgprint(
                    "Error detected at bank:<br><hr>"
                    + json.loads(r.text)["description"]
                )
                frappe.throw(json.loads(r.text))
        except Exception as e:
            frappe.logger().debug({"send_nmb webhook_error": e, "try": i + 1})
            sleep(3 * i + 1)
            if i != 2:
                continue
            else:
                raise e


@frappe.whitelist()
def invoice_submission(doc=None, method=None, fees_name=None):
    send_fee_details_to_bank = (
        frappe.get_value("Company", doc.company, "send_fee_details_to_bank") or 0
    )
    if not send_fee_details_to_bank:
        return
    if not doc and fees_name:
        doc = frappe.get_doc("Fees", fees_name)
    if not doc.callback_token:
        frappe.msgprint(
            _(
                "This fee is not set with a token to be sent to the Bank. Generating the token..."
            ),
            alert=True,
        )
        set_callback_token(doc, "invoice_submission")
    series = frappe.get_value("Company", doc.company, "nmb_series") or ""
    abbr = frappe.get_value("Company", doc.company, "abbr") or ""
    if not series:
        frappe.throw(_("Please set NMB User Series in Company {0}".format(doc.company)))
    data = {
        "reference": doc.bank_reference,
        "student_name": doc.student_name,
        "student_id": doc.student,
        "amount": doc.grand_total,
        "type": "Fees Invoice",
        "code": 10,
        "allow_partial": "FALSE",
        "callback_url": "https://"
        + get_host_name()
        + "/api/method/csf_tz.bank_api.receive_callback?token="
        + doc.callback_token,
    }
    send_nmb("invoice_submission", data, doc.company)


@frappe.whitelist(allow_guest=True)
def receive_callback(*args, **kwargs):
    r = frappe.request
    url = url_fix(r.url.replace("+", " "))
    # http_method = r.method
    body = r.get_data()
    # headers = r.headers
    message = {}
    if body:
        data = body.decode("utf-8")
        msgs = ToObject(data)
        atr_list = list(msgs.__dict__)
        for atr in atr_list:
            if getattr(msgs, atr):
                message[atr] = getattr(msgs, atr)
    else:
        frappe.throw("This has no body!")
    parsed_url = urlparse(url)
    message["fees_token"] = parsed_url[4][6:]
    message["doctype"] = "NMB Callback"
    nmb_doc = frappe.get_doc(message)

    if nmb_doc.insert(ignore_permissions=True):
        frappe.response["status"] = 1
        frappe.response["description"] = "success"
    else:
        frappe.response["description"] = "insert failed"
        frappe.response["http_status_code"] = 409

    enqueue(
        method=make_payment_entry,
        queue="short",
        timeout=10000,
        is_async=True,
        kwargs=nmb_doc,
    )


def make_payment_entry(method="callback", **kwargs):
    for key, value in kwargs.items():
        nmb_doc = value
        doc_info = get_fee_info(nmb_doc.reference)
        accounts = get_fees_default_accounts(doc_info["company"])

        nmb_amount = flt(nmb_doc.amount)
        frappe.flags.ignore_account_permission = True
        if doc_info["doctype"] == "Fees":
            if method == "callback":
                frappe.set_user("Administrator")
            fees_name = doc_info["name"]
            bank_reference, receivable_account = frappe.get_value(
                "Fees", fees_name, ["bank_reference", "receivable_account"]
            )
            if bank_reference == nmb_doc.reference:
                payment_entry = get_payment_entry(
                    "Fees",
                    fees_name,
                    party_amount=nmb_amount,
                    bank_amount=nmb_amount,
                    party_type="Student",
                    payment_type="Receive",
                )
                payment_entry.update(
                    {
                        "payment_date": nmb_doc.timestamp,
                        "posting_date": nmb_doc.timestamp,
                        "reference_no": nmb_doc.reference,
                        "reference_date": nmb_doc.timestamp,
                        "remarks": "Payment Entry against {0} {1} via NMB Bank Payment {2}".format(
                            "Fees", fees_name, nmb_doc.reference
                        ),
                        "paid_from": receivable_account,
                        "party_account": receivable_account,
                    }
                )
                payment_entry.flags.ignore_permissions = True
                # payment_entry.references = []
                # payment_entry.set_missing_values()
                payment_entry.save()
                payment_entry.submit()
            return nmb_doc

        elif doc_info["doctype"] == "Student Applicant Fees":
            doc = frappe.get_doc("Student Applicant Fees", doc_info["name"])
            if not doc.callback_token == nmb_doc.fees_token:
                return
            # Below remarked after introducing VFD in AV solutions
            # jl_rows = []
            # debit_row = dict(
            #     account=accounts["bank"],
            #     debit_in_account_currency=nmb_amount,
            #     account_currency=accounts["currency"],
            #     cost_center=doc.cost_center,
            # )
            # jl_rows.append(debit_row)

            # credit_row_1 = dict(
            #     account=accounts["income"],
            #     credit_in_account_currency=nmb_amount,
            #     account_currency=accounts["currency"],
            #     cost_center=doc.cost_center,
            # )
            # jl_rows.append(credit_row_1)

            # user_remark = (
            #     "Journal Entry against {0} {1} via NMB Bank Payment {2}".format(
            #         "Student Applicant Fees", doc_info["name"], nmb_doc.reference
            #     )
            # )
            # jv_doc = frappe.get_doc(
            #     dict(
            #         doctype="Journal Entry",
            #         posting_date=nmb_doc.timestamp,
            #         accounts=jl_rows,
            #         company=doc.company,
            #         multi_currency=0,
            #         user_remark=user_remark,
            #     )
            # )

            # jv_doc.flags.ignore_permissions = True
            # frappe.flags.ignore_account_permission = True
            # jv_doc.save()
            # jv_doc.submit()
            # jv_url = frappe.utils.get_url_to_form(jv_doc.doctype, jv_doc.name)
            # si_msgprint = "Journal Entry Created <a href='{0}'>{1}</a>".format(
            #     jv_url, jv_doc.name
            # )
            # frappe.msgprint(_(si_msgprint))
            frappe.db.set_value(
                "Student Applicant", doc.student, "application_status", "Approved"
            )
            return nmb_doc


@frappe.whitelist(allow_guest=True)
def receive_validate_reference(*args, **kwargs):
    r = frappe.request
    # uri = url_fix(r.url.replace("+"," "))
    # http_method = r.method
    body = r.get_data()
    # headers = r.headers
    message = {}
    if body:
        data = body.decode("utf-8")
        msgs = ToObject(data)
        atr_list = list(msgs.__dict__)
        for atr in atr_list:
            if getattr(msgs, atr):
                message[atr] = getattr(msgs, atr)
    else:
        frappe.throw("This has no body!")

    doc_info = get_fee_info(message["reference"])
    if doc_info["name"]:
        doc = frappe.get_doc(doc_info["doctype"], doc_info["name"])
        response = dict(
            status=1,
            reference=doc.bank_reference,
            student_name=doc.student_name,
            student_id=doc.student,
            amount=doc.grand_total,
            type="Fees Invoice",
            code=10,
            allow_partial="FALSE",
            callback_url="https://"
            + get_host_name()
            + "/api/method/csf_tz.bank_api.receive_callback?token="
            + doc.callback_token,
            token=message["token"],
        )
        return response
    else:
        frappe.response["status"] = 0
        frappe.response["description"] = "Not Exist"


def cancel_invoice(doc, method):
    send_fee_details_to_bank = (
        frappe.get_value("Company", doc.company, "send_fee_details_to_bank") or 0
    )
    if not send_fee_details_to_bank:
        return
    data = {
        "reference": str(doc.bank_reference),
    }
    message = send_nmb("invoice_cancel", data, doc.company)
    frappe.msgprint(str(message))


def reconciliation(doc=None, method=None):
    companys = frappe.get_all("Company")
    for company in companys:
        if not frappe.get_value("Company", company["name"], "nmb_username"):
            continue
        data = {"reconcile_date": datetime.today().strftime("%d-%m-%Y")}
        frappe.msgprint(str(data))
        message = send_nmb("reconcilliation", data, company["name"])
        if message["status"] == 1 and len(message["transactions"]) > 0:
            for i in message["transactions"]:
                if (
                    len(
                        frappe.get_all(
                            "NMB Callback",
                            filters=[
                                ["NMB Callback", "reference", "=", i.reference],
                                ["NMB Callback", "receipt", "=", i.receipt],
                            ],
                            fields=["name"],
                        )
                    )
                    == 1
                ):
                    doc_info = get_fee_info(message["reference"])
                    if doc_info["name"]:
                        message["fees_token"] = frappe.get_value(
                            doc_info["doctype"], doc_info["name"], "callback_token"
                        )
                        message["doctype"] = "NMB Callback"
                        nmb_doc = frappe.get_doc(message)
                        enqueue(
                            method=make_payment_entry,
                            queue="short",
                            timeout=10000,
                            is_async=True,
                            kwargs=nmb_doc,
                        )


def get_fee_info(bank_reference):
    data = {"name": "", "doctype": ""}
    doc_list = frappe.get_all(
        "Fees",
        filters=[
            ["Fees", "bank_reference", "=", bank_reference],
            ["Fees", "docstatus", "=", 1],
        ],
        fields=["name", "company"],
    )
    if len(doc_list):
        data["name"] = doc_list[0]["name"]
        data["doctype"] = "Fees"
        data["company"] = doc_list[0]["company"]
        return data
    else:
        doc_list = frappe.get_all(
            "Student Applicant Fees",
            filters=[
                ["Student Applicant Fees", "bank_reference", "=", bank_reference],
                ["Student Applicant Fees", "docstatus", "=", 1],
            ],
            fields=["name", "company"],
        )
        if len(doc_list):
            data["name"] = doc_list[0]["name"]
            data["doctype"] = "Student Applicant Fees"
            data["company"] = doc_list[0]["company"]
        return data


def get_fees_default_accounts(company):
    data = {"bank": "", "income": "", "currency": ""}
    data["currency"] = frappe.get_value("Company", company, "default_currency") or ""
    data["bank"] = frappe.get_value("Company", company, "fee_bank_account") or ""
    if not data["bank"]:
        data["bank"] = (
            frappe.get_value("Company", company, "default_bank_account") or ""
        )
    data["income"] = (
        frappe.get_value("Company", company, "student_applicant_fees_revenue_account")
        or ""
    )
    if not data["income"]:
        data["bank"] = (
            frappe.get_value("Company", company, "default_income_account") or ""
        )
    if not data["bank"]:
        frappe.throw(_("Please set Fee Bank Account in Company {0}".format(company)))
    if not data["income"]:
        frappe.throw(
            _(
                "Please set Student Applicant Fees Revenue Account in Company {0}".format(
                    company
                )
            )
        )
    return data


@frappe.whitelist()
def make_payment_entry_from_call(docname):
    nmb_doc = frappe.get_doc("NMB Callback", docname)
    make_payment_entry(method="frontend", kwargs=nmb_doc)


@frappe.whitelist()
def url_fix(url: str, charset: str = "utf-8") -> str:
    """Fixes the URL by encoding the non-ASCII characters.

    Args:
        url (str): The URL to fix.
        charset (str, optional): The charset to use. Defaults to "utf-8".

    Examples:
        >>> url_fix("http://example.com/äöüß")
        'http://example.com/%C3%A4%C3%B6%C3%BC%C3%9F'

        >>> url_fix("http://example.com/漢字")
        'http://example.com/%E6%BC%A2%E5%AD%97'

        >>> url_fix("http://example.com/|pipe")
        'http://example.com/%7Cpipe'

        >>> url_fix("http://example.com/page#fragment with space")
        'http://example.com/page%23fragment%20with%20space'

        >>> url_fix("http://example.com/{curly})
        'http://example.com/%7Bcurly%7D'

        >>> url_fix("http://example.com/[square])
        'http://example.com/%5Bsquare%5D'

    """
    s = url.replace("\\", "/")

    if s.startswith("file://") and s[7:8].isalpha() and s[8:10] in (":/", "|/"):
        s = f"file:///{s[7:]}"

    url = urlparse(s)
    path = quote(url.path, safe="/%+$!*'(),")
    qs = quote(url.query, safe=":&%=+$!*'(),")
    anchor = quote(url.fragment, safe=":&%=+$!*'(),")
    return urlunparse((url.scheme, url.netloc, path, qs, "", anchor))

