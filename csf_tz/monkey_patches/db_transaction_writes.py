import frappe
from frappe import _
from frappe.utils import cint
from frappe.database.database import Database


def check_transaction_status(self, query, *args, **kwargs):
    if (
        self.transaction_writes
        and query
        and query.strip().split()[0].lower()
        in ("start", "alter", "drop", "create", "begin", "truncate")
    ):
        raise Exception("This statement can cause implicit commit")

    if query and query.strip().lower() in ("commit", "rollback"):
        self.transaction_writes = 0

    if query[:6].lower() not in ("update", "insert", "delete"):
        return

    self.transaction_writes += 1
    if self.transaction_writes > (cint(frappe.conf._max_writes_allowed) or 200000):
        if self.auto_commit_on_many_writes:
            self.commit()
        else:
            frappe.throw(
                _("Too many writes in one request. Please send smaller requests"),
                frappe.ValidationError,
            )

Database.check_transaction_status = check_transaction_status
