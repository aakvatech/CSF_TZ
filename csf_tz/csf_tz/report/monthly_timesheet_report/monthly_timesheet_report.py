# Copyright (c) 2013, Aakvatech and contributors
# For license information, please see license.txt

import frappe
import pandas as pd
import numpy as np
from frappe import msgprint, _
from frappe.utils import data, flt

def execute(filters=None):
	conditions, filters = get_conditions(filters)

	columns = get_columns(filters)
	data = []

	if filters.hours_per_day:
		columns = [_("Date") + "::160"]
		
		records = hours_per_day_data(conditions, filters)
		if not records:
			frappe.throw("No Record found for the filters From Date: {0}, To Date: {1}, Hours Per Day: {2} you specified..., \
			Please change your filters and try again..!!".format(
				frappe.bold(filters.from_date),
				frappe.bold(filters.to_date),
				frappe.bold(filters.hours_per_day),
			))
		
		df_colnames = [key for key in records[0].keys()]
		
		df = pd.DataFrame.from_records(records, columns=df_colnames)
		
		table_pvt = pd.pivot_table(
			df,
			index=["employee_name"],
			values="total_hours",
			columns="date",
			fill_value = " ",
			aggfunc="first"
		)

		columns += table_pvt.columns.values.tolist()
		data += table_pvt.reset_index().values.tolist()
	
		if filters.hours_per_project:
			frappe.throw(frappe.bold("No Records..!!"))


	elif filters.hours_per_project:
		columns = [_("Project") + ":Link/Project:180"]

		project_details = hours_per_project_data(conditions, filters)

		if not project_details:
			frappe.throw("No Record found for the filters From Date: {0}, To Date: {1} and Hours Per Project: {2} you specified..., \
			Please change your filters and try again..!!".format(
				frappe.bold(filters.from_date),
				frappe.bold(filters.to_date),
				frappe.bold(filters.hours_per_project)
			))
		
		project_colnames = [key for key in project_details[0].keys()]
		
		df_project = pd.DataFrame.from_records(project_details, columns=project_colnames)

		project_pvt = pd.pivot_table(
			df_project,
			index=["employee_name"],
			values="hours",
			columns="project",
			fill_value = " ",
			aggfunc= np.sum,
			margins = True
		)

		columns += project_pvt.columns.values.tolist()
		data += project_pvt.reset_index().values.tolist()

		if filters.hours_per_day:
			frappe.throw(frappe.bold("No Records..!!"))
	
	else:
		timesheet_rows = timesheet_details(conditions, filters)

		if not timesheet_rows:
			frappe.throw("No Record found for the filters From Date: {0}, To Date: {1} you specified..., \
			Please change your filters and try again..!!".format(
				frappe.bold(filters.from_date),
				frappe.bold(filters.to_date),
			))

		for row in timesheet_rows:
			data.append(row)
			
	return columns, data


def get_columns(filters):
	columns = []

	if ( filters.summerized_view != "Hours Used Per Day" and 
		filters.summerized_view != "Hours Used Per Project" ):
		columns += [
			{"fieldname": "date", "label": _("Date"), "fieldtype": "Date", "width": 120 },
			# {"fieldname": "employee", "label": _("Employee"), "fieldtype": "Data", "width": 120 },
			{"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 120 },
			{"fieldname": "activity_type", "label": _("Actuvuty Type"), "fieldtype": "Data", "width": 120 },
			{"fieldname": "from_time", "label": _("From Time"), "fieldtype": "Time", "width": 120 },
			{ "fieldname": "to_time", "label": _("To Time"), "fieldtype": "Time", "width": 120 },
			{"fieldname": "hours_used", "label": _("Hours Used"), "fieldtype": "Data", "width": 120 },
			{"fieldname": "task", "label": _("Task"), "fieldtype": "Data", "width": 120 },
			{ "fieldname": "project", "label": _("Project"), "fieldtype": "Data", "width": 120 },
		]
	return columns


def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"): conditions += "ts.start_date >= %(from_date)s"
	if filters.get("to_date"): conditions += "AND ts.start_date <= %(to_date)s"
	return conditions, filters


def timesheet_details(conditions, filters):
	employees = frappe.get_all("Timesheet", 
		filters=[["start_date", ">=", filters.from_date],["start_date", "<=", filters.to_date]],
		fields=["start_date", "employee", "employee_name"]
	)

	logs_data = get_timesheet_logs(conditions, filters)

	data = []
	for emp in employees:
		parent_row = {
			"date": emp["start_date"].strftime("%Y-%m-%d"),
			# "employee": emp["employee"],
			"employee_name": emp["employee_name"]
		}

		data.append(parent_row)

		for log in logs_data:
			if (
				emp["start_date"].strftime("%Y-%m-%d") == log["date2"] and 
				emp["employee"] == log["employee"] and 
				emp["employee_name"] == log["employee_name"]
			):
				
				child_row = {
					"indent": 2,
					"activity_type": log.activity_type,
					"from_time": log.from_time,
					"to_time": log.to_time,
					"hours_used": flt(log.hours_used, 1),
					"task": log.task,
					"project": log.project
				}

				data.append(child_row)
				
			else:
				continue
	return data


def hours_per_day_data(conditions, filters):
	data = []
	records = frappe.get_all("Timesheet", 
		filters=[["start_date", ">=", filters.from_date], ["start_date", "<=", filters.to_date]],
		fields=["employee", "employee_name", "start_date", "total_hours"])

	for record in records:
		data.append({
			"employee": record.employee,
			"employee_name": record.employee_name,
			"date": record.start_date.strftime("%d-%m-%Y"),
			"total_hours": flt(record.total_hours, 1)
		})
	return data


def hours_per_project_data(conditions, filters):
	project_details = frappe.db.sql("""
		SELECT ts.employee, 
			ts.employee_name, 
			tsd.project,
			tsd.hours
		FROM `tabTimesheet Detail` tsd
		INNER JOIN `tabTimesheet` ts ON tsd.parent = ts.name
		WHERE {conditions}
		ORDER BY ts.start_date
		""".format(conditions=conditions), filters, as_dict=1 
	)
	
	data = []
	for entry in project_details:
		entry.update({
			"hours": flt(entry.hours, 1)
		})
		data.append(entry)
	return data


def get_timesheet_logs(conditions, filters):
	timesheet_logs = frappe.db.sql("""
		SELECT ts.employee AS employee,
				ts.employee_name AS employee_name,
				tsd.activity_type AS activity_type,
				DATE_FORMAT(tsd.from_time, "%%Y-%%m-%%d") AS date2,
				DATE_FORMAT(tsd.from_time, "%%T") AS from_time,
				DATE_FORMAT(tsd.to_time, "%%T") AS to_time,
				tsd.hours AS hours_used,
				tsd.task AS task,
				tsd.project AS project
		FROM `tabTimesheet Detail` tsd
		INNER JOIN `tabTimesheet` ts ON tsd.parent = ts.name
		WHERE {conditions}
		ORDER BY ts.start_date
	""".format(conditions=conditions), filters, as_dict=1
	)
	return timesheet_logs
