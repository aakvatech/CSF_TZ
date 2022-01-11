from __future__ import unicode_literals
from erpnext.setup.utils import get_exchange_rate
import frappe
from frappe import _
import frappe.permissions
import frappe.share
import traceback
import pyqrcode
import io
import base64
from frappe.utils import flt, cint, getdate, get_datetime, nowdate, nowtime
from frappe.model.mapper import get_mapped_doc
from frappe.desk.form.linked_with import get_linked_docs, get_linked_doctypes
from erpnext.stock.utils import get_stock_balance, get_latest_stock_qty
from erpnext.stock.doctype.batch.batch import get_batch_qty
from erpnext.accounts.utils import get_account_currency
import csf_tz
from csf_tz import console


@frappe.whitelist()
def generate_qrcode(qrcode_data):
    c = pyqrcode.create(qrcode_data)
    s = io.BytesIO()
    c.png(s, scale=3)
    encoded = "data:image/png;base64," + base64.b64encode(s.getvalue()).decode("ASCII")
    return encoded


@frappe.whitelist()
def app_error_log(title, error):
    frappe.log(traceback.format_exc())


@frappe.whitelist()
def getInvoiceExchangeRate(date, currency):
    try:
        exchange_rate = get_exchange_rate(
            currency, frappe.defaults.get_global_default("currency"), str(date)
        )
        return exchange_rate

    except Exception as e:
        error_log = app_error_log(frappe.session.user, str(e))


@frappe.whitelist()
def getInvoice(currency, name):
    try:
        doc = frappe.get_doc("Open Invoice Exchange Rate Revaluation", name)
        # company_currency = frappe.get_value("Company",doc.company,"default_currency")
        sinv_details = frappe.get_all(
            "Sales Invoice",
            filters=[
                ["Sales Invoice", "currency", "=", str(currency)],
                ["Sales Invoice", "party_account_currency", "!=", str(currency)],
                ["Sales Invoice", "company", "=", doc.company],
                ["Sales Invoice", "status", "in", ["Unpaid", "Overdue"]],
            ],
            fields=[
                "name",
                "grand_total",
                "conversion_rate",
                "currency",
                "party_account_currency",
                "customer",
            ],
        )
        pinv_details = frappe.get_all(
            "Purchase Invoice",
            filters=[
                ["Purchase Invoice", "currency", "=", str(currency)],
                ["Purchase Invoice", "party_account_currency", "!=", str(currency)],
                ["Purchase Invoice", "company", "=", doc.company],
                ["Purchase Invoice", "status", "in", ["Unpaid", "Overdue"]],
            ],
            fields=[
                "name",
                "grand_total",
                "conversion_rate",
                "currency",
                "party_account_currency",
                "supplier",
            ],
        )
        doc.inv_err_detail = []
        doc.save()
        if sinv_details:
            count = 1
            for sinv in sinv_details:
                if not flt(sinv.conversion_rate) == flt(
                    doc.exchange_rate_to_company_currency
                ):
                    addChildItem(
                        name,
                        sinv.name,
                        "Sales Invoice",
                        sinv.conversion_rate,
                        sinv.currency,
                        sinv.grand_total,
                        doc.exchange_rate_to_company_currency,
                        count,
                    )
                    count += 1
        if pinv_details:
            for pinv in pinv_details:
                if not flt(pinv.conversion_rate) == flt(
                    doc.exchange_rate_to_company_currency
                ):
                    addChildItem(
                        name,
                        pinv.name,
                        "Purchase Invoice",
                        pinv.conversion_rate,
                        pinv.currency,
                        pinv.grand_total,
                        doc.exchange_rate_to_company_currency,
                        count,
                    )
                    count += 1
        return sinv_details

    except Exception as e:
        app_error_log(frappe.session.user, str(e))


def addChildItem(
    name,
    inv_no,
    invoice_type,
    invoice_exchange_rate,
    invoice_currency,
    invoice_amount,
    current_exchange,
    idx,
):
    gain_loss = (flt(invoice_amount) * flt(invoice_exchange_rate)) - (
        flt(invoice_amount) * flt(current_exchange)
    )
    child_doc = frappe.get_doc(
        dict(
            doctype="Inv ERR Detail",
            parent=name,
            parenttype="Open Invoice Exchange Rate Revaluation",
            parentfield="inv_err_detail",
            invoice_number=inv_no,
            invoice_type=invoice_type,
            invoice_exchange_rate=invoice_exchange_rate,
            invoice_currency=invoice_currency,
            invoice_gain_or_loss=gain_loss,
            invoice_amount=invoice_amount,
            idx=idx,
        )
    ).insert()


@frappe.whitelist()
def print_out(message, alert=False, add_traceback=False, to_error_log=False):
    if not message:
        return

    def out(mssg):
        if message:
            frappe.errprint(str(mssg))
            if to_error_log:
                frappe.log_error(str(mssg))
            if add_traceback:
                if len(frappe.utils.get_traceback()) > 20:
                    frappe.errprint(frappe.utils.get_traceback())
            if alert:
                frappe.msgprint(str(mssg))

    def check_msg(msg):
        if isinstance(msg, str):
            msg = str(msg)

        elif isinstance(msg, int):
            msg = str(msg)

        elif isinstance(msg, float):
            msg = str(msg)

        elif isinstance(msg, dict):
            msg = frappe._dict(msg)

        elif isinstance(msg, list):
            for item in msg:
                check_msg(item)
            msg = ""

        elif isinstance(msg, object):
            msg = str(msg.__dict__)

        else:
            msg = str(msg)
        out(msg)

    check_msg(message)


def get_stock_ledger_entries(item_code):
    if get_version() == 12:
        conditions = " and item_code = '%s'" % item_code
    else:
        conditions = " and is_cancelled = 0 and item_code = '%s'" % item_code
    return frappe.db.sql(
        """
        select item_code, batch_no, warehouse, sum(actual_qty) as actual_qty
        from `tabStock Ledger Entry`
        where docstatus = 1 %s
        group by batch_no, item_code, warehouse
        having sum(actual_qty) > 0
        order by item_code, warehouse"""
        % conditions,
        as_dict=1,
    )


def get_version():
    branch_name = get_app_branch("erpnext")
    if "12" in branch_name:
        return 12
    elif "13" in branch_name:
        return 13
    else:
        return 13


def get_app_branch(app):
    """Returns branch of an app"""
    import subprocess

    try:
        branch = subprocess.check_output(
            "cd ../apps/{0} && git rev-parse --abbrev-ref HEAD".format(app), shell=True
        )
        branch = branch.decode("utf-8")
        branch = branch.strip()
        return branch
    except Exception:
        return ""


@frappe.whitelist()
def get_item_info(item_code):
    sle = get_stock_ledger_entries(item_code)
    iwb_map = {}
    float_precision = cint(frappe.db.get_default("float_precision")) or 3

    for d in sle:
        iwb_map.setdefault(d.item_code, {}).setdefault(d.warehouse, {}).setdefault(
            d.batch_no, frappe._dict({"bal_qty": 0.0})
        )
        qty_dict = iwb_map[d.item_code][d.warehouse][d.batch_no]

        expiry_date_unicode = frappe.db.get_value("Batch", d.batch_no, "expiry_date")

        if expiry_date_unicode:
            qty_dict.expires_on = expiry_date_unicode
            exp_date = frappe.utils.data.getdate(expiry_date_unicode)
            qty_dict.expires_on = exp_date
            expires_in_days = (exp_date - frappe.utils.datetime.date.today()).days
            if expires_in_days > 0:
                qty_dict.expiry_status = expires_in_days
            else:
                qty_dict.expiry_status = 0

        qty_dict.actual_qty = flt(qty_dict.actual_qty, float_precision) + flt(
            d.actual_qty, float_precision
        )

    iwd_list = []
    for key1, value1 in iwb_map.items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                lin_dict = {"item_code": key1, "warehouse": key2, "batch_no": key3}
                lin_dict.update(value3)
                iwd_list.append(lin_dict)
    return iwd_list


@frappe.whitelist()
def get_item_prices(item_code, currency, customer=None, company=None):
    item_code = "'{0}'".format(item_code)
    currency = "'{0}'".format(currency)
    unique_records = int(frappe.db.get_value("CSF TZ Settings", None, "unique_records"))
    prices_list = []
    unique_price_list = []
    max_records = frappe.db.get_value("Company", company, "max_records_in_dialog") or 20
    if customer:
        conditions = " and SI.customer = '%s'" % customer
    else:
        conditions = ""

    query = """ SELECT SI.name, SI.posting_date, SI.customer, SIT.item_code, SIT.qty, SIT.rate
            FROM `tabSales Invoice` AS SI 
            INNER JOIN `tabSales Invoice Item` AS SIT ON SIT.parent = SI.name
            WHERE 
                SIT.item_code = {0} 
                AND SIT.parent = SI.name
                AND SI.docstatus=%s 
                AND SI.currency = {2}
                AND SI.is_return != 1
                AND SI.company = '{3}'
                {1}
            ORDER by SI.posting_date DESC""".format(
        item_code, conditions, currency, company
    ) % (
        1
    )

    items = frappe.db.sql(query, as_dict=True)
    for item in items:
        item_dict = {
            "name": item.item_code,
            "item_code": item.item_code,
            "price": item.rate,
            "date": item.posting_date,
            "invoice": item.name,
            "customer": item.customer,
            "qty": item.qty,
        }
        if (
            unique_records == 1
            and item.rate not in unique_price_list
            and len(prices_list) <= max_records
        ):
            unique_price_list.append(item.rate)
            prices_list.append(item_dict)
        elif unique_records != 1 and item.rate and len(prices_list) <= max_records:
            prices_list.append(item_dict)
    return prices_list


@frappe.whitelist()
def get_item_prices_custom(*args):
    filters = args[5]
    start = args[3]
    limit = args[4]
    unique_records = int(frappe.db.get_value("CSF TZ Settings", None, "unique_records"))
    if "customer" in filters:
        customer = filters["customer"]
    else:
        customer = ""
    company = filters["company"]
    item_code = "'{0}'".format(filters["item_code"])
    currency = "'{0}'".format(filters["currency"])
    prices_list = []
    unique_price_list = []
    max_records = int(start) + int(limit)
    conditions = ""
    if "posting_date" in filters:
        posting_date = filters["posting_date"]
        from_date = "'{from_date}'".format(from_date=posting_date[1][0])
        to_date = "'{to_date}'".format(to_date=posting_date[1][1])
        conditions += "AND DATE(SI.posting_date) BETWEEN {start} AND {end}".format(
            start=from_date, end=to_date
        )
    if customer:
        conditions += " AND SI.customer = '%s'" % customer

    query = """ SELECT SI.name, SI.posting_date, SI.customer, SIT.item_code, SIT.qty,  SIT.rate
            FROM `tabSales Invoice` AS SI 
            INNER JOIN `tabSales Invoice Item` AS SIT ON SIT.parent = SI.name
            WHERE 
                SIT.item_code = {0} 
                AND SIT.parent = SI.name
                AND SI.docstatus= 1
                AND SI.currency = {2}
                AND SI.is_return != 1
                AND SI.company = '{3}'
                {1}
            ORDER by SI.posting_date DESC""".format(
        item_code, conditions, currency, company
    )

    items = frappe.db.sql(query, as_dict=True)
    for item in items:
        item_dict = {
            "name": item.item_code,
            "item_code": item.item_code,
            "rate": item.rate,
            "posting_date": item.posting_date,
            "invoice": item.name,
            "customer": item.customer,
            "qty": item.qty,
        }
        if (
            unique_records == 1
            and item.rate not in unique_price_list
            and len(prices_list) <= max_records
        ):
            unique_price_list.append(item.rate)
            prices_list.append(item_dict)
        elif unique_records != 1 and item.rate and len(prices_list) <= max_records:
            prices_list.append(item_dict)
    return prices_list


@frappe.whitelist()
def get_repack_template(template_name, qty):
    template_doc = frappe.get_doc("Repack Template", template_name)
    rows = []
    rows.append(
        {
            "item_code": template_doc.item_code,
            "item_uom": template_doc.item_uom,
            "qty": cint(qty),
            "item_template": 1,
            "s_warehouse": template_doc.default_warehouse,
        }
    )
    for i in template_doc.repack_template_details:
        rows.append(
            {
                "item_code": i.item_code,
                "item_uom": i.item_uom,
                "qty": cint(float(i.qty / template_doc.qty) * float(qty)),
                "item_template": 0,
                "t_warehouse": i.default_target_warehouse,
            }
        )
    return rows


@frappe.whitelist()
def create_delivery_note(doc=None, method=None, doc_name=None):
    if not doc and doc_name:
        doc = frappe.get_doc("Sales Invoice", doc_name)
    if not frappe.get_value(
        "Company", doc.company, "enabled_auto_create_delivery_notes"
    ):
        return
    if not doc.enabled_auto_create_delivery_notes:
        return
    if doc.update_stock:
        return
    from_delivery_note = False
    i = 0
    msg = ""
    warehouses_list = []
    space = "<br>"
    for item in doc.items:
        pending_qty = flt(item.stock_qty) - get_delivery_note_item_count(
            item.name, item.parent
        )
        if (
            item.warehouse not in warehouses_list
            and check_item_is_maintain(item.item_code)
            and pending_qty != 0
        ):
            warehouses_list.append(item.warehouse)
        if item.delivery_note or item.delivered_by_supplier:
            from_delivery_note = True
        if check_item_is_maintain(item.item_code):
            i += 1
    if from_delivery_note or i == 0:
        return

    for warehouse in warehouses_list:
        if not doc.is_new():
            check = get_list_pending_sales_invoice(doc.name, warehouse)
            if warehouse and len(check) == 0:
                return
        delivery_doc = frappe.get_doc(make_delivery_note(doc.name, None, warehouse))
        delivery_doc.set_warehouse = warehouse
        delivery_doc.form_sales_invoice = doc.name
        delivery_doc.flags.ignore_permissions = True
        delivery_doc.flags.ignore_account_permission = True
        delivery_doc.save()
        if method:
            url = frappe.utils.get_url_to_form(delivery_doc.doctype, delivery_doc.name)
            msgprint = "Delivery Note Created as Draft at <a href='{0}'>{1}</a>".format(
                url, delivery_doc.name
            )
            frappe.msgprint(
                _(msgprint), title="Delivery Note Created", indicator="green"
            )

            update_drug_prescription(doc, delivery_doc)


def check_item_is_maintain(item_name):
    is_stock_item = frappe.get_value("Item", item_name, "is_stock_item")
    if is_stock_item != 1:
        return False
    else:
        return True


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None, set_warehouse=None):
    def warehouse_condition(doc):
        if set_warehouse:
            return doc.warehouse == set_warehouse
        else:
            return True

    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")

    def get_qty(source_doc):
        delivery_note_item_count = get_delivery_note_item_count(
            source_doc.name, source_doc.parent
        )
        return flt(source_doc.stock_qty) - delivery_note_item_count

    def update_item(source_doc, target_doc, source_parent):
        target_doc.stock_qty = get_qty(source_doc)
        target_doc.qty = target_doc.stock_qty / flt(source_doc.conversion_factor)
        target_doc.base_amount = target_doc.qty * flt(source_doc.base_rate)
        target_doc.amount = target_doc.qty * flt(source_doc.rate)

    doclist = get_mapped_doc(
        "Sales Invoice",
        source_name,
        {
            "Sales Invoice": {
                "doctype": "Delivery Note",
                "validation": {"docstatus": ["=", 1]},
            },
            "Sales Invoice Item": {
                "doctype": "Delivery Note Item",
                "field_map": {
                    "name": "si_detail",
                    "parent": "against_sales_invoice",
                    "serial_no": "serial_no",
                    "sales_order": "against_sales_order",
                    "so_detail": "so_detail",
                    "cost_center": "cost_center",
                    "Warehouse": "warehouse",
                },
                "postprocess": update_item,
                "condition": lambda doc: check_item_is_maintain(doc.item_code),
                "condition": lambda doc: warehouse_condition(doc),
            },
            "Sales Taxes and Charges": {
                "doctype": "Sales Taxes and Charges",
                "add_if_empty": True,
            },
            "Sales Team": {
                "doctype": "Sales Team",
                "field_map": {"incentives": "incentives"},
                "add_if_empty": True,
            },
        },
        target_doc,
        set_missing_values,
        ignore_permissions=True,
    )

    items_list = []
    for it in doclist.items:
        if float(it.qty) != 0.0 and check_item_is_maintain(it.item_code):
            items_list.append(it)
    doclist.items = items_list

    return doclist


def create_indirect_expense_item(doc, method=None):
    if (
        not doc.parent_account
        or doc.is_group
        or not check_expenses_in_parent_accounts(doc.name)
        or not doc.company
    ):
        return
    if (
        not doc.parent_account
        and not check_expenses_in_parent_accounts(doc.account_name)
        and doc.item
    ):
        doc.item = ""
        return
    indirect_expenses_group = frappe.db.exists("Item Group", "Indirect Expenses")
    if not indirect_expenses_group:
        indirect_expenses_group = frappe.get_doc(
            dict(
                doctype="Item Group",
                item_group_name="Indirect Expenses",
            )
        )
        indirect_expenses_group.flags.ignore_permissions = True
        frappe.flags.ignore_account_permission = True
        indirect_expenses_group.save()
    item = frappe.db.exists("Item", doc.account_name)
    if item:
        item = frappe.get_doc("Item", doc.account_name)
        doc.item = item.name
        company_list = []
        for i in item.item_defaults:
            if doc.company not in company_list:
                if i.company == doc.company:
                    company_list.append(doc.company)
                    if i.expense_account != doc.name:
                        i.expense_account == doc.name
                        item.save()
        if doc.company not in company_list:
            row = item.append("item_defaults", {})
            row.company = doc.company
            row.expense_account = doc.name
            item.save()
            company_list.append(doc.company)
            doc.db_update()
        return item.name
    new_item = frappe.get_doc(
        dict(
            doctype="Item",
            item_code=doc.account_name,
            item_group="Indirect Expenses",
            is_stock_item=0,
            is_sales_item=0,
            stock_uom="Nos",
            include_item_in_manufacturing=0,
            item_defaults=[
                {
                    "company": doc.company,
                    "expense_account": doc.name,
                    "default_warehouse": "",
                }
            ],
        )
    )
    new_item.flags.ignore_permissions = True
    frappe.flags.ignore_account_permission = True
    new_item.save()
    if new_item.name:
        url = frappe.utils.get_url_to_form(new_item.doctype, new_item.name)
        msgprint = "New Item is Created <a href='{0}'>{1}</a>".format(
            url, new_item.name
        )
        frappe.msgprint(_(msgprint))
        doc.item = new_item.name
    doc.db_update()
    return new_item.name


def check_expenses_in_parent_accounts(account_name):
    parent_account_1 = frappe.get_value("Account", account_name, "parent_account")
    if "Indirect Expenses" in str(parent_account_1):
        return True
    else:
        parent_account_2 = frappe.get_value(
            "Account", parent_account_1, "parent_account"
        )
        if "Indirect Expenses" in str(parent_account_2):
            return True
        else:
            parent_account_3 = frappe.get_value(
                "Account", parent_account_2, "parent_account"
            )
            if "Indirect Expenses" in str(parent_account_3):
                return True
            else:
                return False
    return False


@frappe.whitelist()
def add_indirect_expense_item(account_name):
    account = frappe.get_doc("Account", account_name)
    return create_indirect_expense_item(account)


def get_linked_docs_info(doctype, docname):
    linkinfo = get_linked_doctypes(doctype)
    linked_doc = get_linked_docs(doctype, docname, linkinfo)
    linked_doc_list = []
    if linked_doc:
        for key, value in linked_doc.items():
            if key != "Activity Log":
                for val in value:
                    dco_info = {
                        "doctype": key,
                        "docname": val.name,
                        "docstatus": val.docstatus,
                    }
                    linked_doc_list.append(dco_info)
    return linked_doc_list


def cancle_linked_docs(doc_list):
    for doc_info in doc_list:
        if doc_info["docstatus"] == 1:
            linked_doc_list = get_linked_docs_info(
                doc_info["doctype"], doc_info["docname"]
            )
            if len(linked_doc_list) > 0:
                cancle_linked_docs(linked_doc_list)
            cancel_doc(doc_info["doctype"], doc_info["docname"])


def delete_linked_docs(doc_list):
    for doc_info in doc_list:
        linked_doc_list = get_linked_docs_info(doc_info["doctype"], doc_info["docname"])
        if len(linked_doc_list) > 0:
            delete_linked_docs(linked_doc_list)
        delete_doc(doc_info["doctype"], doc_info["docname"])


def cancel_doc(doctype, docname):
    doc = frappe.get_doc(doctype, docname)
    if doc.docstatus == 1:
        doc.flags.ignore_permissions = True
        doc.cancel()
        doc = frappe.get_doc(doctype, docname)
        if doc.docstatus == 2:
            frappe.msgprint(_("{0} {1} is Canceled").format("Stock Entry", doc.name))
        else:
            frappe.msgprint(
                _("{0} {1} is Not Canceled").format("Stock Entry", doc.name)
            )


def delete_doc(doctype, docname):
    doc = frappe.get_doc(doctype, docname)
    if doc.docstatus == 1:
        doc.flags.ignore_permissions = True
        doc.cancel()
        doc = frappe.get_doc(doctype, docname)
        if doc.docstatus == 2:
            frappe.msgprint(_("{0} {1} is Canceled").format("Stock Entry", doc.name))
            doc.flags.ignore_permissions = True
            doc.delete()
            frappe.db.commit()
            frappe.msgprint(_("{0} {1} is Deleted").format("Stock Entry", doc.name))
        else:
            frappe.msgprint(
                _("{0} {1} is Not Canceled").format("Stock Entry", doc.name)
            )
    elif doc.docstatus == 0 or doc.docstatus == 2:
        doc.flags.ignore_permissions = True
        doc.delete()
        frappe.db.commit()
        frappe.msgprint(_("{0} {1} is Deleted").format("Stock Entry", doc.name))


def get_pending_si_delivery_item_count(item_code, company, warehouse):
    query = """SELECT SUM(SII.delivered_qty) as delivered_count ,SUM(SII.stock_qty) as sold_count
            FROM `tabSales Invoice` AS SI 
            INNER JOIN `tabSales Invoice Item` AS SII ON SI.name = SII.parent
            WHERE
                SII.item_code = '%s'
                AND SII.parent = SI.name
                AND SI.docstatus= 1
                AND SI.company = '%s'
                AND SII.warehouse = '%s'
                AND SII.so_detail IS NULL
                AND (SII.so_detail IS NOT NULL AND SII.delivery_note IS NOT NULL)
                AND SI.update_stock = 0
                AND SII.is_ignored_in_pending_qty != 1
                AND SII.delivered_qty != SII.stock_qty
            """ % (
        item_code,
        company,
        warehouse,
    )

    counts = frappe.db.sql(query, as_dict=True)
    if len(counts) > 0:
        if not counts[0]["sold_count"]:
            counts[0]["sold_count"] = 0
        if not counts[0]["delivered_count"]:
            counts[0]["delivered_count"] = 0
        return counts[0]["sold_count"] - counts[0]["delivered_count"]


def get_pending_delivery_item_count(item_code, company, warehouse):
    query = """ SELECT SUM(SOI.delivered_qty) as delivered_count ,SUM(SOI.stock_qty) as sold_count
            FROM `tabSales Order` AS SO
            INNER JOIN `tabSales Order Item` AS SOI ON SO.name = SOI.parent
            WHERE 
                SOI.item_code = '%s' 
                AND SOI.parent = SO.name 
                AND SO.docstatus= 1 
                AND SO.company = '%s' 
                AND SOI.warehouse = '%s' 
                AND SO.status NOT IN ('Closed', 'On Hold', 'Cancelled')
            """ % (
        item_code,
        company,
        warehouse,
    )

    counts = frappe.db.sql(query, as_dict=True)
    if len(counts) > 0:
        if not counts[0]["sold_count"]:
            counts[0]["sold_count"] = 0
        if not counts[0]["delivered_count"]:
            counts[0]["delivered_count"] = 0
        return counts[0]["sold_count"] - counts[0]["delivered_count"]
    else:
        return 0


def get_item_balance(item_code, company, warehouse=None):
    if company and not warehouse:
        warehouse = frappe.get_all(
            "Warehouse", filters={"company": company, "lft": 1}, fields=["name"]
        )[0]["name"]
    values, condition = [item_code], ""
    if warehouse:
        lft, rgt, is_group = frappe.db.get_value(
            "Warehouse", warehouse, ["lft", "rgt", "is_group"]
        )

        if is_group:
            values.extend([lft, rgt])
            condition += "and exists (\
                select name from `tabWarehouse` wh where wh.name = tabBin.warehouse\
                and wh.lft >= %s and wh.rgt <= %s)"

        else:
            values.append(warehouse)
            condition += " AND warehouse = %s"

    actual_qty = frappe.db.sql(
        """select sum(actual_qty) from tabBin
        where item_code=%s {0}""".format(
            condition
        ),
        values,
    )[0][0]

    return actual_qty


@frappe.whitelist()
def validate_item_remaining_qty(
    item_code, company, warehouse=None, stock_qty=None, so_detail=None
):
    if not warehouse:
        return
    if frappe.db.get_single_value("Stock Settings", "allow_negative_stock"):
        return
    is_stock_item = frappe.get_value("Item", item_code, "is_stock_item")
    if is_stock_item == 1:
        item_balance = get_item_balance(item_code, company, warehouse) or 0
        if not item_balance:
            frappe.throw(
                _(
                    "<B>{0}</B> item balance is ZERO. Cannot proceed unless Allow Over Sell"
                ).format(item_code)
            )
        pending_delivery_item_count = (
            get_pending_delivery_item_count(item_code, company, warehouse) or 0
        )
        pending_si = (
            get_pending_si_delivery_item_count(item_code, company, warehouse) or 0
        )
        # The float(stock_qty) is removed to allow ignore the item itself
        if so_detail:
            if pending_delivery_item_count > float(stock_qty):
                qty_to_reduce = pending_delivery_item_count
            else:
                qty_to_reduce = float(stock_qty)
        else:
            qty_to_reduce = pending_delivery_item_count + float(stock_qty)

        item_remaining_qty = item_balance - qty_to_reduce - pending_si
        if item_remaining_qty < 0:
            frappe.throw(
                _(
                    "Item Balance: '{2}'<br>Pending Sales Order: '{3}'<br>Pending Direct Sales Invoice: {5}<br>Current request is {4}<br><b>Results into balance Qty for '{0}' to '{1}'</b>".format(
                        item_code,
                        item_remaining_qty,
                        item_balance,
                        pending_delivery_item_count,
                        float(stock_qty),
                        pending_si,
                    )
                )
            )


def validate_items_remaining_qty(doc, method):
    for item in doc.items:
        if not item.allow_over_sell and not (item.so_detail and item.delivery_note):
            validate_item_remaining_qty(
                item.item_code,
                doc.company,
                item.warehouse,
                item.stock_qty,
                item.so_detail,
            )


def on_cancel_fees(doc, method):
    from erpnext.accounts.utils import unlink_ref_doc_from_payment_entries

    unlink_ref_doc_from_payment_entries(doc)
    from csf_tz.bank_api import cancel_invoice

    cancel_invoice(doc, "before_cancel")


def check_validate_delivery_note(doc=None, method=None, doc_name=None):
    if not doc and doc_name:
        doc = frappe.get_doc("Sales Invoice", doc_name)
        doc.to_save = True
    else:
        doc.to_save = False
    if doc.docstatus != 2:
        doc.delivery_status = "Not Delivered"
    else:
        doc.to_save = False
    if doc.update_stock:
        return

    part_delivery = False
    # full_delivery = False
    items_qty = 0
    items_delivered_qty = 0
    i = 0
    for item in doc.items:
        if doc.is_new():
            item.delivery_status = "Not Delivered"
            item.delivered_qty = 0
        items_qty += item.stock_qty
        if item.delivery_note or item.delivered_by_supplier:
            part_delivery = True
            i += 1
        if item.delivered_qty:
            if item.stock_qty == item.delivered_qty:
                item.delivery_status = "Delivered"
            elif item.stock_qty < item.delivered_qty:
                item.delivery_status = "Over Delivered"
            elif item.stock_qty > item.delivered_qty and item.delivered_qty > 0:
                item.delivery_status = "Part Delivered"
            items_delivered_qty += item.delivered_qty
    if i == len(doc.items):
        doc.delivery_status = "Delivered"
    elif doc.to_save and items_delivered_qty >= items_qty:
        doc.delivery_status = "Delivered"
    elif doc.to_save and items_delivered_qty <= items_qty and items_delivered_qty > 0:
        doc.delivery_status = "Part Delivered"
    elif part_delivery:
        doc.delivery_status = "Part Delivered"
    else:
        doc.delivery_status = "Not Delivered"
    if doc.to_save:
        doc.flags.ignore_permissions = True
        doc.save()


def check_submit_delivery_note(doc, method):
    if doc.update_stock:
        doc.db_set("delivery_status", "Delivered", commit=True)
        for item in doc.items:
            item.db_set("delivered_qty", item.stock_qty, commit=True)
            item.db_set("delivery_status", "Delivered", commit=True)
    else:
        part_deivery = False
        for item in doc.items:
            if not check_item_is_maintain(item.item_code):
                item.db_set("delivered_qty", item.stock_qty, commit=True)
                item.db_set("delivery_status", "Delivered", commit=True)
                part_deivery = True
        if part_deivery:
            doc.db_set("delivery_status", "Part Delivered", commit=True)


def check_cancel_delivery_note(doc, method):
    if not doc.update_stock:
        doc.db_set("delivery_status", "Not Delivered", commit=True)
        for item in doc.items:
            item.db_set("delivered_qty", 0, commit=True)
            item.db_set("delivery_status", "Not Delivered", commit=True)


def update_delivery_on_sales_invoice(doc, method):
    sales_invoice_list = []
    for item in doc.items:
        if (
            item.against_sales_invoice
            and item.against_sales_invoice not in sales_invoice_list
        ):
            sales_invoice_list.append(item.against_sales_invoice)
    for invoice in sales_invoice_list:
        check_validate_delivery_note(None, None, invoice)


def get_delivery_note_item_count(item_row_name, sales_invoice):
    query = """ SELECT SUM(stock_qty) as cont
            FROM `tabDelivery Note Item` 
            WHERE 
                si_detail = '%s' 
                AND docstatus != 2 
                AND against_sales_invoice = '%s' 
            """ % (
        item_row_name,
        sales_invoice,
    )

    counts = frappe.db.sql(query, as_dict=True)
    if len(counts) > 0 and counts[0]["cont"]:
        return float(counts[0]["cont"])
    else:
        return 0


@frappe.whitelist()
def get_pending_sales_invoice(*args):
    filters = args[5]
    start = cint(args[3])
    page_length = cint(args[4])
    conditions = ""
    if args[1] != "":
        conditions += " AND SI.name = '%s'" % args[1]
    if "posting_date" in filters:
        posting_date = filters["posting_date"]
        from_date = "'{from_date}'".format(from_date=posting_date[1][0])
        to_date = "'{to_date}'".format(to_date=posting_date[1][1])
        conditions += "AND DATE(SI.posting_date) BETWEEN {start} AND {end}".format(
            start=from_date, end=to_date
        )
    if "customer" in filters:
        conditions += " AND SI.customer = '%s'" % filters["customer"]
    if "company" in filters:
        conditions += " AND SI.company = '%s'" % filters["company"]
    if "set_warehouse" in filters:
        conditions += " AND SIT.warehouse = '%s'" % filters["set_warehouse"]
    query = """ 
            WITH CTE AS(
                SELECT
                    SIT.stock_qty, 
                    SIT.delivered_qty, 
                    SIT.warehouse AS set_warehouse, 
                    COALESCE (SUM(DNI.stock_qty), 0) As DNI_sum_stock_qty,           
                    SI.name AS name,                      
                    SI.posting_date AS posting_date,                      
                    SI.customer As customer,
                    ROW_NUMBER()OVER(PARTITION BY SI.name ORDER BY SI.name) AS RN            
                FROM `tabSales Invoice` AS SI              
                    INNER JOIN `tabSales Invoice Item` AS SIT ON SIT.parent = SI.name 
                    INNER JOIN `tabItem` AS IT ON IT.name = SIT.item_code and IT.is_stock_item = 1
                    LEFT OUTER JOIN `tabDelivery Note Item` as DNI on DNI.si_detail = SIT.name AND DNI.docstatus < 2
                WHERE                  
                    SIT.parent = SI.name                  
                    AND SI.docstatus= 1              
                    AND SI.update_stock != 1 
                    AND SI.is_return = 0
                    AND SI.status NOT IN ("Credit Note Issued", "Internal Transfer")
                    AND SIT.stock_qty != SIT.delivered_qty 
                    %s    
                GROUP BY SI.name, SIT.name
                HAVING SIT.stock_qty > DNI_sum_stock_qty
            )
            SELECT * FROM `CTE` WHERE RN = 1
            LIMIT %s
            OFFSET %s
            """ % (
        conditions,
        page_length,
        start,
    )
    data = frappe.db.sql(query, as_dict=True)
    return data


def get_list_pending_sales_invoice(invoice_name=None, warehouse=None):
    conditions = ""
    if invoice_name:
        conditions += " AND SI.name = '%s'" % invoice_name
    if warehouse:
        conditions += " AND SIT.warehouse = '%s'" % warehouse
    query = """ 
            WITH CTE AS(
                SELECT
                    SIT.stock_qty, 
                    SIT.delivered_qty, 
                    COALESCE (SUM(DNI.stock_qty), 0) As DNI_sum_stock_qty,           
                    SI.name AS name,                      
                    SI.posting_date AS posting_date,                      
                    SI.customer As customer, 
                    ROW_NUMBER()OVER(PARTITION BY SI.name ORDER BY SI.name) AS RN 
                FROM `tabSales Invoice` AS SI 
                    INNER JOIN `tabSales Invoice Item` AS SIT ON SIT.parent = SI.name
                    INNER JOIN `tabItem` AS IT ON IT.name = SIT.item_code and IT.is_stock_item = 1
                    LEFT OUTER JOIN `tabDelivery Note Item` as DNI on DNI.si_detail = SIT.name AND DNI.docstatus < 2
                WHERE                  
                    SIT.parent = SI.name                  
                    AND SI.docstatus= 1              
                    AND SI.update_stock != 1 
                    AND SIT.stock_qty != SIT.delivered_qty 
                    %s 
                GROUP BY SI.name, SIT.name
                HAVING SIT.stock_qty > DNI_sum_stock_qty 
            )
            SELECT * FROM `CTE` WHERE RN = 1
            """ % (
        conditions
    )
    data = frappe.db.sql(query, as_dict=True)
    return data


def create_delivery_note_for_all_pending_sales_invoice(doc=None, method=None):
    invoices = get_list_pending_sales_invoice()
    for i in invoices:
        invoice = frappe.get_doc("Sales Invoice", i.name)
        create_delivery_note(invoice)


def get_pending_material_request():
    mat_req_list = frappe.get_all(
        "Material Request",
        filters=[["Material Request", "status", "in", ["Pending"]]],
        fields=["name"],
    )
    return mat_req_list


def make_stock_reconciliation(items, company):
    stock_rec_doc = frappe.get_doc(
        {
            "doctype": "Stock Reconciliation",
            "company": company,
            "purpose": "Stock Reconciliation",
            "Posting Date": getdate(),
            "items": items,
        }
    )
    if stock_rec_doc:
        stock_rec_doc.flags.ignore_permissions = True
        stock_rec_doc.flags.ignore_account_permission = True
        stock_rec_doc.run_method("set_missing_values")
        stock_rec_doc.save()
        url = frappe.utils.get_url_to_form(stock_rec_doc.doctype, stock_rec_doc.name)
        msgprint = (
            "Stock Reconciliation Created as Draft at <a href='{0}'>{1}</a>".format(
                url, stock_rec_doc.name
            )
        )
        frappe.msgprint(_(msgprint))
        return stock_rec_doc.name


def get_stock_balance_for(
    item_code,
    warehouse,
    posting_date=None,
    posting_time=None,
    batch_no=None,
    with_valuation_rate=True,
):
    # frappe.has_permission("Stock Reconciliation", "write", throw = True)
    if not posting_date:
        posting_date = nowdate()
    if not posting_time:
        posting_time = nowtime()
    item_dict = frappe.db.get_value(
        "Item", item_code, ["has_serial_no", "has_batch_no"], as_dict=1
    )

    serial_nos = ""
    with_serial_no = True if item_dict.get("has_serial_no") else False
    data = get_stock_balance(
        item_code,
        warehouse,
        posting_date,
        posting_time,
        with_valuation_rate=with_valuation_rate,
        with_serial_no=with_serial_no,
    )

    if with_serial_no:
        qty, rate, serial_nos = data
    else:
        qty, rate = data

    if item_dict.get("has_batch_no"):
        qty = get_batch_qty(batch_no, warehouse) or 0

    return {"qty": qty, "rate": rate, "serial_nos": serial_nos}


@frappe.whitelist()
def make_stock_reconciliation_for_all_pending_material_request(*args):
    mat_req_list = get_pending_material_request()
    data = {}

    for i in mat_req_list:
        mat_req_doc = frappe.get_doc("Material Request", i["name"])

        if not data.get(mat_req_doc.company):
            data[mat_req_doc.company] = {}

        for item in mat_req_doc.items:
            if not check_item_is_maintain(item.item_code):
                continue
            if (
                not data.get(mat_req_doc.company).get(item.warehouse)
                and not item.stock_reconciliation
            ):
                data[mat_req_doc.company][item.warehouse] = []
                item_dict = get_stock_balance_for(item.item_code, item.warehouse)
                item.valuation_rate = item_dict.get("rate")
                item_dict = {
                    "item_code": item.item_code,
                    "warehouse": item.warehouse,
                    "valuation_rate": item_dict.get("rate"),
                    "batch_no": "",
                    "qty": item_dict.get("qty") + item.stock_qty,
                    "material_request": i["name"],
                    "company": mat_req_doc.company,
                    "row_name": item.name,
                }
                data[mat_req_doc.company][item.warehouse].append(item_dict)

    for key, value in data.items():
        for key1, value1 in value.items():
            if len(value1) > 0:
                items_list = []
                items = []
                for item in value1:
                    if item["item_code"] not in items_list:
                        items.append(item)
                        items_list.append(item["item_code"])
                if len(items) > 0:
                    stock_rec_name = make_stock_reconciliation(value1, key)
                    if stock_rec_name:
                        for item in items:
                            frappe.db.set_value(
                                "Material Request Item",
                                item["row_name"],
                                "stock_reconciliation",
                                stock_rec_name,
                                update_modified=False,
                            )


def calculate_price_reduction(doc, method):
    price_reduction = 0
    for item in doc.items:
        price_reduction += item.qty * item.discount_amount
    doc.price_reduction = price_reduction


def calculate_total_net_weight(doc, method):
    if doc.meta.get_field("total_net_weight"):
        doc.total_net_weight = 0.0
        for d in doc.items:
            if d.total_weight:
                doc.total_net_weight += d.total_weight


@frappe.whitelist()
def get_warehouse_options(company):
    warehouses = frappe.get_all(
        "Warehouse",
        filters=[
            ["Warehouse", "company", "=", company],
            ["Warehouse", "is_group", "=", 0],
        ],
        fields=["name"],
    )
    warehouses_list = []
    for warehouse in warehouses:
        warehouses_list.append(warehouse["name"])
    return warehouses_list


def validate_net_rate(doc, method):
    def throw_message(idx, item_name, rate, ref_rate_field):
        frappe.throw(
            _(
                """Row #{}: Net Selling rate for item {} is lower than its {}. Net Selling rate should be atleast above {}"""
            ).format(idx, item_name, ref_rate_field, rate)
        )

    if not frappe.db.get_single_value("CSF TZ Settings", "validate_net_rate"):
        return

    if hasattr(doc, "is_return") and doc.is_return:
        return

    for it in doc.get("items"):
        if not it.item_code or it.allow_override_net_rate:
            continue

        last_purchase_rate, is_stock_item = frappe.get_cached_value(
            "Item", it.item_code, ["last_purchase_rate", "is_stock_item"]
        )
        last_purchase_rate_in_sales_uom = last_purchase_rate / (
            it.conversion_factor or 1
        )
        if flt(it.net_rate) < flt(last_purchase_rate_in_sales_uom):
            throw_message(
                it.idx,
                frappe.bold(it.item_name),
                last_purchase_rate_in_sales_uom,
                "last purchase rate",
            )

        last_valuation_rate = frappe.db.sql(
            """
            SELECT valuation_rate FROM `tabStock Ledger Entry` WHERE item_code = %s
            AND warehouse = %s AND valuation_rate > 0
            ORDER BY posting_date DESC, posting_time DESC, creation DESC LIMIT 1
            """,
            (it.item_code, it.warehouse),
        )
        if last_valuation_rate:
            last_valuation_rate_in_sales_uom = last_valuation_rate[0][0] / (
                it.conversion_factor or 1
            )
            if (
                is_stock_item
                and flt(it.net_rate) < flt(last_valuation_rate_in_sales_uom)
                and not doc.get("is_internal_customer")
            ):
                throw_message(
                    it.idx,
                    frappe.bold(it.item_name),
                    last_valuation_rate_in_sales_uom,
                    "valuation rate",
                )


def make_withholding_tax_gl_entries_for_purchase(doc, method):
    (
        withholding_payable_account,
        default_currency,
        auto_create_for_purchase_withholding,
    ) = frappe.get_value(
        "Company",
        doc.company,
        [
            "default_withholding_payable_account",
            "default_currency",
            "auto_create_for_purchase_withholding",
        ],
    )
    if not auto_create_for_purchase_withholding:
        return
    float_precision = cint(frappe.db.get_default("float_precision")) or 3
    withholding_payable_account, default_currency = frappe.get_value(
        "Company",
        doc.company,
        ["default_withholding_payable_account", "default_currency"],
    )
    if not withholding_payable_account:
        frappe.throw(
            _("Please Setup Withholding Payable Account in Company " + str(doc.company))
        )
    for item in doc.items:
        if not item.withholding_tax_rate > 0:
            continue
        withholding_payable_account_type = (
            frappe.get_value("Account", withholding_payable_account, "account_type")
            or ""
        )
        if withholding_payable_account_type != "Payable":
            frappe.msgprint(_("Withholding Payable Account type not 'Payable'"))
        if doc.party_account_currency == default_currency:
            exchange_rate = 1
        else:
            exchange_rate = doc.conversion_rate
        creditor_amount = flt(
            item.base_net_rate
            * item.qty
            * item.withholding_tax_rate
            / 100
            / exchange_rate,
            float_precision,
        )
        wtax_base_amount = creditor_amount * exchange_rate

        jl_rows = []
        debit_row = dict(
            account=doc.credit_to,
            party_type="Supplier",
            party=doc.supplier,
            debit_in_account_currency=creditor_amount,
            exchange_rate=exchange_rate,
            cost_center=item.cost_center,
            reference_type="Purchase Invoice",
            reference_name=doc.name,
        )
        jl_rows.append(debit_row)
        credit_row = dict(
            account=withholding_payable_account,
            party_type="Supplier"
            if withholding_payable_account_type == "Payable"
            else "",
            party=doc.supplier if withholding_payable_account_type == "Payable" else "",
            credit_in_account_currency=wtax_base_amount,
            cost_center=item.cost_center,
            account_curremcy=default_currency,
        )
        jl_rows.append(credit_row)
        user_remark = (
            "Withholding Tax Payable Against Item "
            + item.item_code
            + " in "
            + doc.doctype
            + " "
            + doc.name
            + " of amount "
            + str(flt(item.net_amount, 2))
            + " "
            + doc.currency
            + " with exchange rate of "
            + str(doc.conversion_rate)
        )
        jv_doc = frappe.get_doc(
            dict(
                doctype="Journal Entry",
                voucher_type="Contra Entry",
                posting_date=doc.posting_date,
                accounts=jl_rows,
                company=doc.company,
                multi_currency=0
                if doc.party_account_currency == default_currency
                else 1,
                user_remark=user_remark,
            )
        )
        console(jl_rows)
        jv_doc.flags.ignore_permissions = True
        frappe.flags.ignore_account_permission = True
        jv_doc.save()
        if (
            frappe.get_value(
                "Company", doc.company, "auto_submit_for_purchase_withholding"
            )
            or False
        ):
            jv_doc.submit()
        item.withholding_tax_entry = jv_doc.name
        jv_url = frappe.utils.get_url_to_form(jv_doc.doctype, jv_doc.name)
        si_msgprint = (
            "Journal Entry Created for Withholding Tax <a href='{0}'>{1}</a>".format(
                jv_url, jv_doc.name
            )
        )
        frappe.msgprint(_(si_msgprint))


@frappe.whitelist()
def set_fee_abbr(doc=None, method=None):
    doc.company = frappe.get_value("Fee Structure", doc.fee_structure, "company")
    send_fee_details_to_bank = (
        frappe.get_value("Company", doc.company, "send_fee_details_to_bank") or 0
    )
    if not send_fee_details_to_bank:
        return
    doc.abbr = frappe.get_value("Company", doc.company, "abbr")


@frappe.whitelist()
def enroll_all_students(self):
    """Enrolls students or applicants.

    :param self: Program Enrollment Tool

    This is created to allow enqueue of students creation.
    The default enroll process fails when there are too many enrollments to do at a go
    """
    import json

    self = json.loads(self)
    self = frappe.get_doc(dict(self))

    if self.get_students_from == "Student Applicant":
        frappe.msgprint("Remove student applicants that are already created")

    if len(self.students) > 30:
        frappe.enqueue("csf_tz.custom_api.enroll_students", self=self)
        return "queued"
    else:
        enroll_students(self=self)
        return len(self.students)


@frappe.whitelist()
def enroll_students(self):
    """Enrolls students or applicants.

    :param self: Program Enrollment Tool

    This is a copy of ERPNext function meant to allow loading from custom doctypes and frappe.enqueue
    Used in csf_tz.custom_api.enroll_students
    """
    from erpnext.education.api import enroll_student

    total = len(self.students)
    for i, stud in enumerate(self.students):
        frappe.publish_realtime(
            "program_enrollment_tool",
            dict(progress=[i + 1, total]),
            user=frappe.session.user,
        )
        if stud.student:
            prog_enrollment = frappe.new_doc("Program Enrollment")
            prog_enrollment.student = stud.student
            prog_enrollment.student_name = stud.student_name
            prog_enrollment.program = self.new_program
            prog_enrollment.academic_year = self.new_academic_year
            prog_enrollment.academic_term = self.new_academic_term
            prog_enrollment.student_batch_name = (
                stud.student_batch_name
                if stud.student_batch_name
                else self.new_student_batch
            )
            prog_enrollment.save()
        elif stud.student_applicant:
            prog_enrollment = enroll_student(stud.student_applicant)
            prog_enrollment.academic_year = self.academic_year
            prog_enrollment.academic_term = self.academic_term
            prog_enrollment.student_batch_name = (
                stud.student_batch_name
                if stud.student_batch_name
                else self.new_student_batch
            )
            prog_enrollment.save()


@frappe.whitelist()
def get_tax_category(doc_type, company):
    fetch_default_tax_category = (
        frappe.db.get_value("CSF TZ Settings", None, "fetch_default_tax_category") or 0
    )
    if int(fetch_default_tax_category) != 1:
        return ""
    sales_list_types = ["Sales Order", "Sales Invoice", "Delivery Note", "Quotation"]
    Puchase_list_types = ["Purchase Order", "Purchase Invoice", "Purchase Receipt"]
    tax_category = []
    if doc_type in sales_list_types:
        tax_category = frappe.get_all(
            "Sales Taxes and Charges Template",
            filters=[
                ["Sales Taxes and Charges Template", "company", "=", company],
                ["Sales Taxes and Charges Template", "is_default", "=", 1],
            ],
            fields=["name", "tax_category"],
        )
    elif doc_type in Puchase_list_types:
        tax_category = frappe.get_all(
            "Purchase Taxes and Charges Template",
            filters=[
                ["Purchase Taxes and Charges Template", "company", "=", company],
                ["Purchase Taxes and Charges Template", "is_default", "=", 1],
            ],
            fields=["name", "tax_category"],
        )
    return tax_category[0]["tax_category"] if len(tax_category) > 0 else [""]


def make_withholding_tax_gl_entries_for_sales(doc, method):
    (
        withholding_receivable_account,
        default_currency,
        auto_create_for_sales_withholding,
    ) = frappe.get_value(
        "Company",
        doc.company,
        [
            "default_withholding_receivable_account",
            "default_currency",
            "auto_create_for_sales_withholding",
        ],
    )
    if not auto_create_for_sales_withholding:
        return
    float_precision = cint(frappe.db.get_default("float_precision")) or 3
    if not withholding_receivable_account:
        frappe.throw(
            _(
                "Please Setup Withholding Receivable Account in Company "
                + str(doc.company)
            )
        )
    for item in doc.items:
        if not item.withholding_tax_rate > 0:
            continue
        withholding_receivable_account_type = (
            frappe.get_value("Account", withholding_receivable_account, "account_type")
            or ""
        )
        if withholding_receivable_account_type != "Receivable":
            frappe.msgprint(_("Withholding Receivable Account type not 'Receivable'"))
        if doc.party_account_currency == default_currency:
            exchange_rate = 1
        else:
            exchange_rate = doc.conversion_rate
        debtor_amount = flt(
            item.base_net_rate
            * item.qty
            * item.withholding_tax_rate
            / 100
            / exchange_rate,
            float_precision,
        )
        wtax_base_amount = debtor_amount * exchange_rate
        jl_rows = []
        credit_row = dict(
            account=doc.debit_to,
            party_type="customer",
            party=doc.customer,
            credit_in_account_currency=debtor_amount,
            account_curremcy=default_currency
            if doc.party_account_currency == default_currency
            else doc.currency,
            exchange_rate=exchange_rate,
            cost_center=item.cost_center,
            reference_type="Sales Invoice",
            reference_name=doc.name,
        )
        jl_rows.append(credit_row)

        debit_row = dict(
            account=withholding_receivable_account,
            party_type="customer"
            if withholding_receivable_account_type == "Receivable"
            else "",
            party=doc.customer
            if withholding_receivable_account_type == "Receivable"
            else "",
            debit_in_account_currency=wtax_base_amount,
            cost_center=item.cost_center,
            account_curremcy=default_currency,
        )
        jl_rows.append(debit_row)

        user_remark = (
            "Withholding Tax Receivable Against Item "
            + item.item_code
            + " in "
            + doc.doctype
            + " "
            + doc.name
            + " of amount "
            + str(flt(item.net_amount, 2))
            + " "
            + doc.currency
            + " with exchange rate of "
            + str(doc.conversion_rate)
        )
        jv_doc = frappe.get_doc(
            dict(
                doctype="Journal Entry",
                voucher_type="Contra Entry",
                posting_date=doc.posting_date,
                accounts=jl_rows,
                company=doc.company,
                multi_currency=0
                if doc.party_account_currency == default_currency
                else 1,
                user_remark=user_remark,
            )
        )
        jv_doc.flags.ignore_permissions = True
        frappe.flags.ignore_account_permission = True
        jv_doc.save()
        if (
            frappe.get_value(
                "Company", doc.company, "auto_submit_for_sales_withholding"
            )
            or False
        ):
            jv_doc.submit()
        item.withholding_tax_entry = jv_doc.name
        jv_url = frappe.utils.get_url_to_form(jv_doc.doctype, jv_doc.name)
        si_msgprint = (
            "Journal Entry Created for Withholding Tax <a href='{0}'>{1}</a>".format(
                jv_url, jv_doc.name
            )
        )
        frappe.msgprint(_(si_msgprint))

def update_drug_prescription(doc, delivery_doc):
    if doc.patient and doc.enabled_auto_create_delivery_notes:
        for item in doc.items:
            if item.reference_dt == "Drug Prescription":
                if delivery_doc.patient and (delivery_doc.form_sales_invoice == item.parent):
                    for dni in delivery_doc.items:
                        if (
                            item.name == dni.si_detail and 
                            item.item_code == dni.item_code and 
                            item.parent == dni.against_sales_invoice
                        ):
                            frappe.db.set_value("Drug Prescription", item.reference_dn, {
                                "dn_detail": dni.name,
                                "sales_invoice_number": dni.against_sales_invoice,
                                "invoiced": 1
                            })