import frappe
from frappe import _
from erpnext.accounts.general_ledger import make_gl_entries 

def calculate_additional_costs(bom, method):
    additional_costs = 0
    for cost in bom.additional_costs:
        additional_costs += cost.cost_per_unit
    return additional_costs

def validate_bom_changes(self, method):
    if self.docstatus == 1:
        frappe.throw(_("Cannot change Additional Costs after BOM submission"))

def on_submit_stock_entry(doc, method):
    if doc.purpose == "Manufacture" and doc.work_order:
        work_order = frappe.get_doc('Work Order', doc.work_order)
        bom = frappe.get_doc("BOM", work_order.bom_no)
        additional_costs = calculate_additional_costs(bom, method)
        for item in doc.items:
            if item.is_finished_item:
                item.additional_cost = additional_costs / len(doc.items)

        # Accounting Entry
        create_gl_entry(doc, additional_costs)
        distribute_additional_costs(doc, method)


def create_gl_entry(doc, additional_costs):
    company = frappe.get_doc('Company', doc.company)
    gl_entries = [
        frappe._dict({
            "account": f"Stock In Hand - {company.abbr}",
            "debit": additional_costs,
            "credit": 0,
            "voucher_type": "Stock Entry",
            "voucher_no": doc.name,
            "remarks": "Additional Costs for Manufacturing",
            "company": doc.company,
            "posting_date": doc.posting_date
        }),
        frappe._dict({
            "account": f"Additional Costs - {company.abbr}",
            "debit": 0,
            "credit": additional_costs,
            "voucher_type": "Stock Entry",
            "voucher_no": doc.name,
            "remarks": "Additional Costs for Manufacturing",
            "company": doc.company,
            "posting_date": doc.posting_date
        })
    ]
    make_gl_entries(gl_entries)

def distribute_additional_costs(doc, method):
    total_qty = sum(item.qty for item in doc.items if item.is_finished_item)
    for item in doc.items:
        if item.is_finished_item:
            item.additional_cost = (item.qty / total_qty) * doc.total_additional_costs
