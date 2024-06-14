# Copyright (c) 2024, Aakvatech and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    raw_data = get_data(filters)
    fiscal_years = get_unique_fiscal_years(raw_data)
    columns = get_columns(fiscal_years)
    result_data = build_data(raw_data, fiscal_years)
    return columns, result_data

def get_unique_fiscal_years(raw_data):
    # Extract unique fiscal years from raw data
    return sorted(set(row['fiscal_year'] for row in raw_data))

def get_columns(fiscal_years):
    # Build the columns dynamically based on unique fiscal years
    columns = [_("Party") + ":Link/Customer:120", _("Account") + ":Link/Account:120"]
    columns.extend(_(year) + ":Currency:100" for year in fiscal_years)
    return columns

def get_data(filters):
    # Fetch data from the database
    results = frappe.db.sql("""
        SELECT
            party,
            account,
            fiscal_year,
            SUM(debit - credit) as balance
        FROM
            `tabGL Entry`
        WHERE
            party_type = 'Customer'
            AND is_cancelled = 0
            AND posting_date BETWEEN %(from_date)s AND %(to_date)s AND company = %(company)s
        GROUP BY
            party, account, fiscal_year
    """, filters, as_dict=True)
    return results

def build_data(raw_data, fiscal_years):
    # Initialize a dictionary to store balances by party, account, and fiscal year
    data_dict = {}
    
    # Populate the dictionary with balances
    for row in raw_data:
        party = row['party']
        account = row['account']
        fiscal_year = row['fiscal_year']
        balance = row['balance']
        
        if (party, account) not in data_dict:
            data_dict[(party, account)] = {fy: 0 for fy in fiscal_years}
        
        data_dict[(party, account)][fiscal_year] = balance
    
    # Convert the dictionary to a list of lists for the report
    data = []
    for (party, account), balances in data_dict.items():
        row = [party, account]
        row.extend(balances[fiscal_year] for fiscal_year in fiscal_years)
        data.append(row)
    
    return data
