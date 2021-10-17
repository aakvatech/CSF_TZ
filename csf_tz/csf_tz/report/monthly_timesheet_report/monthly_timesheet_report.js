// Copyright (c) 2016, Aakvatech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Timesheet Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "hours_per_day",
			"label": __("Hours Per Day"),
			"fieldtype": "Check"
		},
		{
			"fieldname": "hours_per_project",
			"label": __("Hours Per Project"),
			"fieldtype": "Check"
		}

	],
};


