// Copyright (c) 2023, Aakvatech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Price by Price List"] = {
	"filters": [
		{
			"fieldname": "item_description",
			"label": __("Item or Part of Description"),
			"fieldtype": "Data",
			"default": "",
		},
		{
			"fieldname": "tax_rate",
			"label": __("Tax Rate"),
			"fieldtype": "Percent",
			"default": "18",
			"mandatory": 1,
		},
	    {
			"fieldname": "barcode",
			"label": __("Scan Barcode"),
			"fieldtype": "Data",
			"default": "",
			"options": "Barcode"
        },
	]
}