# Copyright (c) 2013, Aakvatech and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	columns, data = [], []

	columns = [
		{"fieldname": "group","label": _("Diff Group"),"fieldtype": "Data","width": 200},
		{"fieldname": "voucher_type","label": _("Voucher Type"),"fieldtype": "Data","width": 200},
		{"fieldname": "voucher_no","label": _("Voucher No"),"fieldtype": "Data","width": 200},
		{"fieldname": "item_code", "label": _("Item Code"), "fieldtype": "Data", "width": 200},
		{"fieldname": "warehouse", "label": _("Warehouse"), "fieldtype": "Data",  "width": 200},
		{"fieldname": "actual_qty",	"label": _("Actual Quantity"), "fieldtype": "Data",	"width": 200},
		{"fieldname": "qty_after_transaction",	"label": _("Actual Qty After Transaction"),	"fieldtype": "Data","width": 200}
	]

	data = []
	total_records = 0

	if not filters:
		return
	item_list = frappe.db.sql("""
		select distinct item_code, warehouse from `tabBin` ORDER BY item_code, warehouse
	""", as_dict = 1)

	skipped = 0
	prev_row = {"actual_qty": 0, "qty_after_transaction": 0, "voucher_no": "", "voucher_type": "Header"}
	data.append(prev_row)
	for item in item_list:
		item_wh_sle_list = frappe.db.get_all("Stock Ledger Entry", 
			filters = [["posting_date", ">=", filters.from_date], ["posting_date", "<=", filters.end_date], ["item_code", "=", item.item_code], ["warehouse", "=", item.warehouse], ["is_cancelled", "=", 0], ["docstatus", "=", 1]],
			fields = ["name", "voucher_type", "voucher_no", "actual_qty", "qty_after_transaction"],
			order_by = "posting_date asc, posting_time asc"
		)
		if not item_wh_sle_list or len(item_wh_sle_list) == 1:
			continue
		total_records += len(item_wh_sle_list) or 0

		prev_row = {"actual_qty": 0, "qty_after_transaction": 0, "voucher_no": "", "voucher_type": "First"}
		for item_wh_sle in item_wh_sle_list:
			if prev_row["voucher_type"] == "First" or item_wh_sle.voucher_type == "Stock Reconciliation":
				skipped += 1
			else:
				if flt(prev_row["qty_after_transaction"], 2) + flt(item_wh_sle.actual_qty, 2) != flt(item_wh_sle.qty_after_transaction, 2):
					row = {"group": item_wh_sle.name, "voucher_type": item_wh_sle.voucher_type, "voucher_no": item_wh_sle.voucher_no, "item_code": item.item_code,"warehouse": item.warehouse, "actual_qty": item_wh_sle.actual_qty, "qty_after_transaction": item_wh_sle.qty_after_transaction}

					data.append({"group": item_wh_sle.name, "voucher_type": prev_row["voucher_type"], "voucher_no": prev_row["voucher_no"], "item_code": item.item_code,"warehouse": item.warehouse, "actual_qty": prev_row["actual_qty"], "qty_after_transaction": prev_row["qty_after_transaction"]})
					data.append(row)
			prev_row["actual_qty"] = item_wh_sle.actual_qty
			prev_row["qty_after_transaction"] = item_wh_sle.qty_after_transaction
			prev_row["voucher_no"] = item_wh_sle.voucher_no
			prev_row["voucher_type"] = item_wh_sle.voucher_type
	frappe.msgprint(_("Total records analyzed: " + str(total_records) + ". Skipped records: " + str(skipped)))

	return columns, data
