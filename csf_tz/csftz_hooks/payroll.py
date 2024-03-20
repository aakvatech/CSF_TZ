from __future__ import unicode_literals
import frappe
from frappe import _
import frappe
import os
from frappe.utils.background_jobs import enqueue
from frappe.utils.pdf import get_pdf, cleanup
from PyPDF2 import PdfFileWriter
from csf_tz import console
from frappe.model.workflow import apply_workflow
from frappe.utils import cint, flt


def before_insert_payroll_entry(doc, method):
    enable_payroll_approval = frappe.db.get_single_value(
        "CSF TZ Settings", "enable_payroll_approval"
    )
    if enable_payroll_approval:
        doc.has_payroll_approval = 1


def before_insert_salary_slip(doc, method):
    enable_payroll_approval = frappe.db.get_single_value(
        "CSF TZ Settings", "enable_payroll_approval"
    )
    if enable_payroll_approval:
        doc.has_payroll_approval = 1


def before_cancel_payroll_entry(doc, method):
    if not doc.has_payroll_approval:
        return

    doc.ignore_linked_doctypes = "GL Entry"
    salary_slips = frappe.get_all(
        "Salary Slip", filters={"payroll_entry": doc.name}, pluck="name"
    )

    journal_entry = None
    if len(salary_slips) > 0:
        for slip in salary_slips:
            try:
                slip_doc = frappe.get_doc("Salary Slip", slip)
                if not journal_entry:
                    journal_entry = slip_doc.journal_entry

                if slip_doc.docstatus == 1:
                    slip_doc.cancel()
                slip_doc.delete()
            except:
                traceback = frappe.get_traceback()
                title = _(f"Error for Salary Slip: <b>{slip_doc.name}</b>")
                frappe.log_error(traceback, title)
                continue

    if journal_entry:
        try:
            jv_doc = frappe.get_doc("Journal Entry", journal_entry)
            if jv_doc.docstatus == 1:
                jv_doc.cancel()
            jv_doc.delete()
        except:
            traceback = frappe.get_traceback()
            title = _(f"Error for Journal Entry: <b>{jv_doc.name}</b>")
            frappe.log_error(traceback, title)
            return


@frappe.whitelist()
def update_slips(payroll_entry):
    ss_list = frappe.get_all("Salary Slip", filters={"payroll_entry": payroll_entry})
    count = 0
    for salary in ss_list:
        ss_doc = frappe.get_doc("Salary Slip", salary.name)
        if ss_doc.docstatus != 0:
            continue
        ss_doc.earnings = []
        ss_doc.deductions = []
        ss_doc.queue_action("save", timeout=4600)
        count += 1

    frappe.msgprint(_("{0} Salary Slips is updated".format(count)))
    return count


@frappe.whitelist()
def update_slip(salary_slip):
    ss_doc = frappe.get_doc("Salary Slip", salary_slip)
    if ss_doc.docstatus != 0:
        return
    ss_doc.earnings = []
    ss_doc.deductions = []
    ss_doc.save()
    frappe.msgprint(_("Salary Slips is updated"))
    return "True"


@frappe.whitelist()
def print_slips(payroll_entry):
    enqueue(
        method=enqueue_print_slips,
        queue="short",
        timeout=100000,
        is_async=True,
        job_name="print_salary_slips",
        kwargs=payroll_entry,
    )


def enqueue_print_slips(kwargs):
    console("Start Printing")
    payroll_entry = kwargs
    ss_data = frappe.get_all("Salary Slip", filters={"payroll_entry": payroll_entry})
    ss_list = []
    for i in ss_data:
        ss_list.append(i.name)
    doctype = dict({"Salary Slip": ss_list})
    print_format = ""
    default_print_format = frappe.db.get_value(
        "Property Setter",
        dict(property="default_print_format", doc_type="Salary Slip"),
        "value",
    )
    if default_print_format:
        print_format = default_print_format
    else:
        print_format = "Standard"

    pdf = download_multi_pdf(
        doctype, payroll_entry, format=print_format, no_letterhead=0
    )
    if pdf:
        ret = frappe.get_doc(
            {
                "doctype": "File",
                "attached_to_doctype": "Payroll Entry",
                "attached_to_name": payroll_entry,
                "folder": "Home/Attachments",
                "file_name": payroll_entry + ".pdf",
                "file_url": "/files/" + payroll_entry + ".pdf",
                "content": pdf,
            }
        )
        ret.save(ignore_permissions=1)
        console("Printing Finished", "The PDF file is ready in attatchments")
        return ret


def download_multi_pdf(doctype, name, format=None, no_letterhead=0):
    output = PdfFileWriter()
    if isinstance(doctype, dict):
        for doctype_name in doctype:
            for doc_name in doctype[doctype_name]:
                try:
                    console(doc_name)
                    output = frappe.get_print(
                        doctype_name,
                        doc_name,
                        format,
                        as_pdf=True,
                        output=output,
                        no_letterhead=no_letterhead,
                    )
                except Exception:
                    frappe.log_error(
                        "Permission Error on doc {} of doctype {}".format(
                            doc_name, doctype_name
                        )
                    )
        frappe.local.response.filename = "{}.pdf".format(name)

    return read_multi_pdf(output)


def read_multi_pdf(output):
    fname = os.path.join("/tmp", "frappe-pdf-{0}.pdf".format(frappe.generate_hash()))
    output.write(open(fname, "wb"))

    with open(fname, "rb") as fileobj:
        filedata = fileobj.read()

    return filedata


@frappe.whitelist()
def create_journal_entry(payroll_entry):
    payroll_entry_doc = frappe.get_doc("Payroll Entry", payroll_entry)
    if (
        payroll_entry_doc.docstatus != 1
        or payroll_entry_doc.salary_slips_submitted == 1
    ):
        return
    draft_slips_count = frappe.db.count(
        "Salary Slip", filters={"payroll_entry": payroll_entry, "docstatus": 0}
    )

    if draft_slips_count > 0:
        frappe.throw(_("Salary Slips are not submitted"))
    else:
        jv_name = payroll_entry_doc.make_accrual_jv_entry()
        jv_url = frappe.utils.get_url_to_form("Journal Entry", jv_name)
        si_msgprint = _("Journal Entry Created <a href='{0}'>{1}</a>").format(
            jv_url, jv_name
        )
        frappe.msgprint(si_msgprint)
        return "True"


def before_update_after_submit(doc, method):
    if not doc.has_payroll_approval:
        return

    # submit salary slips directly if payroll entry is approved
    if "Approved" in doc.workflow_state:
        doc.submit_salary_slips()
        return

    salary_slips = frappe.get_all(
        "Salary Slip", filters={"payroll_entry": doc.name}, pluck="name"
    )
    if len(salary_slips) == 0:
        return

    params = {"salary_slips": salary_slips, "action": get_workflow_action(doc)}

    enqueue(
        method=enqueue_apply_workflow_for_salary_slips,
        queue="short",
        timeout=100000,
        is_async=True,
        job_name="apply_workflow_for_salary_slips",
        kwargs=params,
    )


def get_workflow_action(doc):
    if doc.workflow_state == "Approval Requested":
        return "Submit"
    elif doc.workflow_state == "Change Requested":
        return "Reject"
    elif "Reviewed" in doc.workflow_state:
        return "Submit"


def enqueue_apply_workflow_for_salary_slips(kwargs):
    for slip in kwargs.get("salary_slips"):
        slip_doc = frappe.get_doc("Salary Slip", slip)

        if kwargs.get("action") == "Reject" and slip_doc.workflow_state == "Open":
            continue
        elif (
            kwargs.get("action") == "Submit"
            and slip_doc.workflow_state == "Ongoing Approval"
        ):
            continue
        elif kwargs.get("action") == "Submit" and slip_doc.workflow_state == "Approved":
            continue
        elif (
            kwargs.get("action") == "Cancel" and slip_doc.workflow_state == "Cancelled"
        ):
            continue
        elif not kwargs.get("action"):
            continue

        try:
            apply_workflow(slip_doc, kwargs.get("action"))

        except:
            traceback = frappe.get_traceback()
            title = _(f"Error for Salary Slip: <b>{slip_doc.name}</b>")
            frappe.log_error(traceback, title)
            continue


@frappe.whitelist()
def generate_component_in_salary_slip_update(doc, method):
    if not doc.name.upper().startswith("NEW") and frappe.db.get_single_value(
        "CSF TZ Settings", "ot_module"
    ):
        base = 0
        list = []

        for component in doc.earnings:
            if str(component.salary_component).upper() == "BASIC":
                base = component.amount / doc.payment_days * doc.total_working_days
                list.append(component)
        if base == 0:
                f"Basic Component not Found on this Salary Slip: <b>{doc.name}</b>"

        for component in doc.salary_slip_ot_component:
            earning_dict = frappe.new_doc("Salary Detail")
            earning_dict.parent = doc.name
            earning_dict.parenttype = doc.doctype
            earning_dict.parentfield = "earnings"
            earning_dict.salary_component = component.salary_component
            earning_dict.amount = calculate_amount(
                base, component.no_of_hours, component.salary_component
            )
            list.append(earning_dict)

            doc.earnings = []
            doc.earnings.extend(list)
            doc.calculate_net_pay()


@frappe.whitelist()
def generate_component_in_salary_slip_insert(doc, method):
    if frappe.db.get_single_value("CSF TZ Settings", "ot_module"):
        doc.salary_slip_ot_component = []
        employee = frappe.get_doc("Employee", doc.employee)
        doc.run_method("get_emp_and_leave_details")
        base = 0
        list = []
        for component in doc.earnings:
            if str(component.salary_component).upper() == "BASIC":
                base = component.amount / doc.payment_days * doc.total_working_days
                list.append(component)
        if base == 0:
            frappe.throw(
                f"Basic Component not Found on this Salary Slip: <b>{doc.name}</b>"
            )

        for component in employee.employee_ot_component:
            component.doctype = "Salary Slip OT Component"
            component.parentfield = "salary_slip_ot_component"
            doc.salary_slip_ot_component.append(component)

            earning_dict = frappe.new_doc("Salary Detail")
            earning_dict.parent = doc.name
            earning_dict.parenttype = doc.doctype
            earning_dict.parentfield = "earnings"
            earning_dict.salary_component = component.salary_component
            earning_dict.amount = calculate_amount(
                base, component.no_of_hours, component.salary_component
            )
            list.append(earning_dict)

            doc.earnings = []
            doc.earnings.extend(list)
            doc.calculate_net_pay()


@frappe.whitelist()
def calculate_amount(base, no_of_hours, salary_component):
    working_hours_per_month = frappe.db.get_single_value(
        "CSF TZ Settings", "working_hours_per_month"
    )
    based_on_hourly_rate, hourly_rate = frappe.db.get_value(
        "Salary Component", salary_component, ["based_on_hourly_rate", "hourly_rate"]
    )
    if based_on_hourly_rate:
        calc = (
            (flt(base) / flt(working_hours_per_month))
            * flt(no_of_hours)
            * (flt(hourly_rate) / 100)
        )
        return calc
    else:
        frappe.throw(
            f"Hourly Rate not set on this Salary Component: <b>{salary_component}</b>, Please set it and try again."
        )
