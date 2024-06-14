// Copyright (c) 2024, Aakvatech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Supplier GL Entries by Fiscal Year"] = {
	"filters": [
        {
            fieldname: 'from_date',
            label: __('From Date'),
            fieldtype: 'Date',
			mandatory: 1
        },
        {
            fieldname: 'to_date',
            label: __('To Date'),
            fieldtype: 'Date',
			mandatory: 1
        },
        {
            fieldname: 'company',
            label: __('Company'),
            fieldtype: 'Link',
            options: 'Company',
			mandatory: 1
        }

	]
};
