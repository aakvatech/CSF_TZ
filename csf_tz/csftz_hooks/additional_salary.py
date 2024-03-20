import frappe
from frappe import _
from frappe.utils import flt, add_days, getdate, add_months, today


@frappe.whitelist()
def create_additional_salary_journal(doc, method):
    if frappe.get_value(
        "Salary Component", doc.salary_component, "create_cash_journal"
    ):
        cash_account = frappe.db.get_single_value(
            "CSF TZ Settings", "default_account_for_additional_component_cash_journal"
        )
        if not cash_account:
            frappe.throw(
                _(
                    "Default Account for Additional Salary Cash Journal not found. Please set it in CSF TZ Settings."
                )
            )
        component_account = frappe.db.get_value(
            "Salary Component Account",
            {"parent": doc.salary_component, "company": doc.company},
            "account",
        )
        if not component_account:
            frappe.throw(
                _(
                    f"Salary Component Account not found for {doc.salary_component} in {doc.company}. Please set it in Salary Component."
                )
            )

        if method == "on_submit":
            dr_account = component_account
            cr_account = cash_account
        elif method == "on_cancel":
            dr_account = cash_account
            cr_account = component_account
        else:
            frappe.msgprint("Unknown method on create_additional_salary_journal")
            return

        precision = frappe.get_precision(
            "Journal Entry Account", "debit_in_account_currency"
        )
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.voucher_type = "Cash Entry"
        journal_entry.user_remark = _(
            f"{doc.doctype} - {doc.name} by {doc.employee_name} for {doc.salary_component}"
        )
        journal_entry.company = doc.company
        journal_entry.posting_date = doc.payroll_date
        journal_entry.referance_doctype = doc.doctype
        journal_entry.referance_docname = doc.name

        payment_amount = flt(doc.amount, precision)

        journal_entry.set(
            "accounts",
            [
                {"account": dr_account, "debit_in_account_currency": payment_amount},
                {"account": cr_account, "credit_in_account_currency": payment_amount},
            ],
        )
        journal_entry.save(ignore_permissions=True)

        if method == "on_submit":
            # remark this since the field of 'journal_name' is not available in Additional Salary
            # frappe.set_value(doc.doctype, doc.name, "journal_name", journal_entry.name)
            msg_to_print = (
                doc.doctype + " journal " + journal_entry.name + " has been created."
            )
        elif method == "on_cancel":
            msg_to_print = (
                doc.doctype
                + " reverse journal "
                + journal_entry.name
                + " has been created."
            )
        frappe.msgprint(msg_to_print)
    if doc.auto_created_based_on:
        frappe.set_value(
            "Additional Salary",
            doc.auto_created_based_on,
            "last_transaction_amount",
            doc.amount,
        )


@frappe.whitelist()
def generate_additional_salary_records():
    today_date = today()
    auto_repeat_frequency = {"Monthly": 1, "Annually": 12}
    additional_salary_list = frappe.get_all(
        "Additional Salary",
        filters={
            "docstatus": "1",
            "auto_repeat_frequency": ("!=", "None"),
            "auto_repeat_end_date": ("!=", ""),
            "auto_repeat_end_date": (">=", today_date),
        },
        fields={
            "name",
            "auto_repeat_end_date",
            "last_transaction_date",
            "last_transaction_amount",
            "auto_repeat_frequency",
            "payroll_date",
            "employee",
            "employee_name",
            "salary_component",
            "type",
            "overwrite_salary_structure_amount",
            "amount",
            "company",
        },
    )
    if len(additional_salary_list) > 0:
        for entry in additional_salary_list:
            if entry.last_transaction_date == None:
                entry.last_transaction_date = entry.payroll_date
            if entry.last_transaction_amount == 0:
                entry.last_transaction_amount = entry.amount
            if entry.auto_repeat_frequency == "Weekly":
                next_date = add_days(getdate(entry.last_transaction_date), 7)
            else:
                frequency_factor = auto_repeat_frequency.get(
                    entry.auto_repeat_frequency, "Invalid frequency"
                )
                if frequency_factor == "Invalid frequency":
                    frappe.throw(
                        f"Invalid frequency: {entry.auto_repeat_frequency} for {entry.name} not found. Contact the developers!"
                    )
                next_date = add_months(
                    getdate(entry.last_transaction_date),
                    frequency_factor,
                )
            # Create 13 days in advance - specificaly to allow mid salary advance.
            if next_date <= add_days(getdate(today_date), 13):
                additional_salary = frappe.new_doc("Additional Salary")
                additional_salary.employee = entry.employee
                additional_salary.payroll_date = next_date
                additional_salary.salary_component = entry.salary_component
                additional_salary.employee_name = entry.employee_name
                additional_salary.amount = entry.last_transaction_amount
                additional_salary.company = entry.company
                additional_salary.overwrite_salary_structure_amount = (
                    entry.overwrite_salary_structure_amount
                )
                additional_salary.type = entry.type
                additional_salary.auto_repeat_frequency = "None"
                additional_salary.auto_created_based_on = entry.name
                additional_salary.auto_repeat_end_date = None
                additional_salary.last_transaction_date = None
                additional_salary.save(ignore_permissions=True)
                frappe.set_value(
                    "Additional Salary",
                    entry.name,
                    "last_transaction_date",
                    next_date,
                )
                frappe.msgprint(
                    "New additional salary created for "
                    + entry.auto_repeat_frequency
                    + " dated "
                    + str(next_date)
                )


@frappe.whitelist()
def get_employee_base_salary_in_hours(employee, payroll_date):
    """
    Returns the base salary in hours of the employee for this month
    """
    last_salary_assignment = frappe.get_all(
        "Salary Structure Assignment",
        filters={"employee": employee, "from_date": ["<=", payroll_date]},
        fields=["name", "base"],
        order_by="`from_date` DESC",
        limit=1,
    )
    last_salary_assignment = (
        last_salary_assignment[0] if last_salary_assignment else None
    )

    working_hours_per_month = frappe.db.get_single_value(
        "CSF TZ Settings", "working_hours_per_month"
    )
    if not working_hours_per_month:
        frappe.throw(
            _(
                "Working Hours per Month not defind in CSF TZ Settings. Define it there and try again."
            )
        )
    base_salary_in_hours = (last_salary_assignment.base or 0) / working_hours_per_month
    return {"base_salary_in_hours": base_salary_in_hours}


def set_employee_base_salary_in_hours(doc, method):
    if doc.based_on_hourly_rate:
        doc.payroll_date = str(doc.payroll_date)
        base_salary_in_hours = get_employee_base_salary_in_hours(
            doc.employee, doc.payroll_date
        )["base_salary_in_hours"]
        doc.amount = doc.hourly_rate / 100 * doc.no_of_hours * base_salary_in_hours
