# Copyright (c) 2023, Aakvatech and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {
            "label": "Voucher Type",
            "fieldname": "Voucher Type",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": "Value",
            "fieldname": "Value",
            "fieldtype": "Currency",
            "width": 250,
        },
        {
            "label": "Count",
            "fieldname": "Count",
            "fieldtype": "Int",
            "width": 250,
        }
    ]
    return columns

def get_data(filters):

    if filters.get("from_date") and filters.get("to_date"):
        conditions = "  BETWEEN %(from_date)s AND %(to_date)s"
    return frappe.db.sql(
        f""" 
		SELECT CONCAT("Main ", voucher_type) AS "Voucher Type", SUM(stock_value_difference) AS "Value", COUNT(*) AS "Count"
		FROM `tabStock Ledger Entry`
		WHERE stock_value_difference > 0
		AND voucher_type IN ("Purchase Receipt", "Purchase Invoice")
		AND posting_date {conditions}
		AND is_cancelled = 0
		GROUP BY voucher_type
		UNION ALL
		SELECT CONCAT("Return ", voucher_type) AS "Voucher Type", SUM(stock_value_difference) AS "Value", COUNT(*) AS "Count"
		FROM `tabStock Ledger Entry`
		WHERE stock_value_difference < 0
		AND voucher_type IN ("Purchase Receipt", "Purchase Invoice")
		AND posting_date {conditions}
		AND is_cancelled = 0
		GROUP BY voucher_type
		UNION ALL
		SELECT CONCAT("Adjustment ", voucher_type) AS "Voucher Type", SUM(stock_value_difference) AS "Value", COUNT(*) AS "Count"
		FROM `tabStock Ledger Entry`
		WHERE voucher_type NOT IN ("Purchase Receipt", "Purchase Invoice", "Delivery Note", "Sales Invoice")
		AND posting_date {conditions}
		AND is_cancelled = 0
		GROUP BY voucher_type
	""",filters,
        as_dict=1,
    )