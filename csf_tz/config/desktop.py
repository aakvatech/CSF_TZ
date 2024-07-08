# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "CSF TZ",
			"category": "Modules",
			"label": _("Country Specifics"),
			"color": "green",
			"icon": "octicon octicon-bookmark",
			"type": "module",
			"description": "Country specific customizations for compliance, taxation and statutory reports.",
		},
		{
			"module_name": "After Sales Services",
			"category": "Modules",
			"label": _("After Sales Services"),
			"color": "green",
			"icon": "octicon octicon-bookmark",
			"type": "module",
		},
		{
			"module_name": "Workshop",
			"category": "Modules",
			"label": _("Workshop"),
			"color": "green",
			"icon": "octicon octicon-bookmark",
			"type": "module",
		},
		{
			"module_name": "Purchase and Stock Management",
			"category": "Modules",
			"label": _("Purchase and Stock Management"),
			"color": "green",
			"icon": "octicon octicon-bookmark",
			"type": "module",
		},
		{
			"module_name": "Sales and Marketing",
			"category": "Modules",
			"label": _("Sales and Marketing"),
			"color": "green",
			"icon": "octicon octicon-bookmark",
			"type": "module",
		},
	]
