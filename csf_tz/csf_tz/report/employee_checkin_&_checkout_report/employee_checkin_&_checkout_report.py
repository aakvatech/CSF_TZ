# Copyright (c) 2013, Aakvatech and contributors
# For license information, please see license.txt

import frappe
import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
from frappe import msgprint, _
from frappe.utils.nestedset import get_descendants_of


def execute(filters=None):
    conditions, filters = get_conditions(filters)

    columns = get_columns(filters)

    chift_type_details = frappe.get_all("Shift Type", {"enable_auto_attendance": 1},
        ["name", "start_time", "end_time", "late_entry_grace_period", "early_exit_grace_period"]
    )

    data = []
    checkin_records = get_checkin_data(conditions, filters, chift_type_details)
    checkout_records = get_checkout_data(conditions, filters, chift_type_details)
    
    if (checkin_records and checkout_records):
        checkin_colnames = [key for key in checkin_records[0].keys()]
        checkin_data = pd.DataFrame.from_records(
            checkin_records, columns=checkin_colnames
        )
        
        checkout_colnames = [key for key in checkout_records[0].keys()]
        checkout_data = pd.DataFrame.from_records(
            checkout_records, columns=checkout_colnames
        )
        
        df = checkin_data.merge(
            checkout_data,
            how="outer",
            on=["employee", "employee_name", "department", "shift", "date"]
        )
        df.fillna("empty", inplace=True)
        
        data += df.values.tolist()
    
    elif (checkin_records or checkout_records):
        if checkin_records:
            data += checkin_records
        
        if checkout_records:
            data += checkout_records
    
    else:
        msgprint(
            "No Record found for the filters From Date: {0},To Date: {1}, Company: {2}, Department: {3} and Employee: {4}\
			you specified...!!!, Please set different filters and Try again..!!!".format(
                frappe.bold(filters.from_date),
                frappe.bold(filters.to_date),
                frappe.bold(filters.company),
                frappe.bold(filters.department),
                frappe.bold(filters.employee),
            )
        )

    return columns, data

def get_columns(filters):
    columns = [
        {"fieldname": "employee", "label": _("Employee No"), "fieldtype": "Data"},
        {"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data"},
        {"fieldname": "department", "label": _("Department"), "fieldtype": "Data"},
        {"fieldname": "shift", "label": _("Shift"), "fieldtype": "Data"},
        {"fieldname": "date", "label": _("Date"), "fieldtype": "Date"},

        # for checkin
        {"fieldname": "actual_checkin_time", "label": _("Actual Time to Checkin"), "fieldtype": "Time"},
        {"fieldname": "checkin_time", "label": _("Checkin Time"), "fieldtype": "Time"},
        {"fieldname": "late_entry_grace_time", "label": _("Late Entry Grace Period"), "fieldtype": "Int"},
        {"fieldname": "checkin_status", "label": _("Checkin Status"), "fieldtype": "Data"},

        # for checkout
        {"fieldname": "actual_checkout_time", "label": _("Actual Time to Checkout"), "fieldtype": "Time"},
        {"fieldname": "checkout_time", "label": _("Checkout Time"), "fieldtype": "Time"},
        {"fieldname": "early_exit_grace_time", "label": _("Early Exit Grace Period"), "fieldtype": "Int"},
        {"fieldname": "checkout_status", "label": _("Checkout Status"), "fieldtype": "Data"},
    ]
    return columns

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND DATE(chec.time) >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND DATE(chec.time) <= %(to_date)s"
    if filters.get("company"):
        conditions += " AND emp.company = %(company)s"
    if filters.get("department") and filters.get("company"):
        department_list = get_department(
            filters.get("department"), filters.get("company")
        )
        conditions += (
            "AND emp.department in ("
            + ", ".join(("'" + d + "'" for d in department_list))
            + ")"
        )
    if filters.get("employee"):
        conditions += " AND chec.employee = %(employee)s"
    return conditions, filters

def get_department(department, company):
    department_list = get_descendants_of("Department", department)
    department_list.append(department)
    return department_list

def get_checkin_data(conditions, filters, chift_type_details):
    checkin_data = []
    checkin_details = get_checkin_details(conditions, filters)
    
    for checkin_d in checkin_details:
        if checkin_d.default_shift and checkin_d.shift_type:
            checkin_d["shift"] = checkin_d.shift_type

        if checkin_d.default_shift or checkin_d.shift_type:
            checkin_d["shift"] = checkin_d.shift_type or checkin_d.default_shift

        if checkin_d.shift:
            for shift_type in chift_type_details:
                if checkin_d.shift == shift_type.name:

                    checkin_time = datetime.strptime(checkin_d.checkin_time, "%H:%M:%S")
                    checkin_time_diff = (checkin_time - shift_type.start_time).time()
                    checkin_time_diff_in_min = (checkin_time_diff.hour * 60 + checkin_time_diff.minute) * 60 + checkin_time_diff.second // 60

                    if checkin_time_diff_in_min <= shift_type.early_exit_grace_period:
                        checkin_status = "Early Checkin"
                    else:
                        checkin_status = "Late Checkin"

                    start_time = (str(shift_type.start_time))

                    complete_row = {
                        "employee": checkin_d.employee,
                        "employee_name": checkin_d.employee_name,
                        "department": checkin_d.department,
                        "shift": checkin_d.shift,
                        "date": checkin_d.date,
                        "actual_checkin_time": start_time,
                        "checkin_time": checkin_d.checkin_time,
                        "late_entry_grace_time": shift_type.late_entry_grace_period,
                        "checkin_status": checkin_status
                    }

                    checkin_data.append(complete_row)

                else:
                    continue
        
        else:
            half_row = {
                "employee": checkin_d.employee,
                "employee_name": checkin_d.employee_name,
                "department": checkin_d.department,
                "shift": '',
                "date": checkin_d.date,
                "actual_checkin_time": '',
                "checkin_time": checkin_d.checkin_time,
                "late_entry_grace_time": '',
                "checkin_status": ''
            }

            checkin_data.append(half_row)

    return checkin_data

def get_checkout_data(conditions, filters, chift_type_details):
    checkout_data = []
    checkout_details = get_checkout_details(conditions, filters)
    
    for checkout_d in checkout_details:
        if checkout_d.default_shift and checkout_d.shift_type:
            checkout_d["shift"] = checkout_d.shift_type

        if checkout_d.default_shift or checkout_d.shift_type:
            checkout_d["shift"] = checkout_d.shift_type or checkout_d.default_shift

        if checkout_d.shift:
            for shift_type in chift_type_details:
                if checkout_d.shift == shift_type.name:

                    checkout_time = datetime.strptime(checkout_d.checkout_time, "%H:%M:%S")
                    checkout_time_diff = (checkout_time - shift_type.end_time).time() 
                    checkout_time_diff_in_min = (checkout_time_diff.hour * 60 + checkout_time_diff.minute) * 60 + checkout_time_diff.second // 60

                    if checkout_time_diff_in_min <= shift_type.early_exit_grace_period:
                        checkout_status = "Early Checkout"
                    else:
                        checkout_status = "Late Checkout"
                    
                    end_time = str(shift_type.end_time)

                    complete_row = {
                        "employee": checkout_d.employee,
                        "employee_name": checkout_d.employee_name,
                        "department": checkout_d.department,
                        "shift": checkout_d.shift,
                        "date": checkout_d.date,
                        "actual_checkout_time": end_time,
                        "checkout_time": checkout_d.checkout_time,
                        "early_exit_grace_time": shift_type.early_exit_grace_period,
                        "checkout_status": checkout_status
                    }

                    checkout_data.append(complete_row)

                else:
                    continue
        
        else:
            half_row = {
                "employee": checkout_d.employee,
                "employee_name": checkout_d.employee_name,
                "department": checkout_d.department,
                "shift": '',
                "date": checkout_d.date,
                "actual_checkout_time": '',
                "checkout_time": checkout_d.checkout_time,
                "early_exit_grace_time": '',
                "checkout_status": ''
            }

            checkout_data.append(half_row)

    return checkout_data

def get_checkin_details(conditions, filters):
    data = frappe.db.sql("""
        SELECT 
            chec.employee AS employee,
            chec.employee_name AS employee_name,
            emp.department AS department,
            emp.default_shift AS default_shift,
            sha.shift_type AS shift_type,
            DATE_FORMAT(chec.time, '%%Y-%%m-%%d') AS date,
            DATE_FORMAT(chec.time, '%%T') AS checkin_time
        FROM `tabEmployee Checkin` chec
            INNER JOIN `tabEmployee` emp ON emp.name = chec.employee
            LEFT JOIN `tabShift Assignment` sha ON chec.employee = sha.employee 
            AND sha.start_date BETWEEN  %(from_date)s AND %(to_date)s
            AND  DATE(chec.time) BETWEEN sha.start_date AND sha.end_date
        WHERE chec.log_type = "IN" {conditions}
        ORDER BY chec.time ASC
    """.format(conditions=conditions), filters, as_dict=1)
    return data

def get_checkout_details(conditions, filters):
    data = frappe.db.sql("""
        SELECT 
            chec.employee AS employee,
            chec.employee_name AS employee_name,
            emp.department AS department,
            emp.default_shift AS default_shift,
            sha.shift_type AS shift_type,
            DATE_FORMAT(chec.time, '%%Y-%%m-%%d') AS date,
            DATE_FORMAT(chec.time, '%%T') AS checkout_time
        FROM `tabEmployee Checkin` chec
            INNER JOIN `tabEmployee` emp ON emp.name = chec.employee
            LEFT JOIN `tabShift Assignment` sha ON chec.employee = sha.employee 
            AND sha.start_date BETWEEN  %(from_date)s AND %(to_date)s
            AND  DATE(chec.time) BETWEEN sha.start_date AND sha.end_date
        WHERE chec.log_type = "OUT" {conditions}
        ORDER BY chec.time ASC
    """.format(conditions=conditions), filters, as_dict=1)
    return data