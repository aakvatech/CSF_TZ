# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BackgroundDocumentPosting(Document):
	def on_submit(self):
		post_doc = frappe.get_doc(self.document_type, self.document_name)
		post_doc.queue_action(self.posting_type, timeout=self.timeout)
