frappe.ui.form.on("Payment Entry", {
	onload: function (frm) {
		if (frm.is_new()) {
			frm.trigger("payment_type");
		}
	},
	payment_type: function (frm) {
		if (frm.is_new()) {
			if (frm.doc.payment_type == "Receive") {
				frm.set_value("naming_series", "RE-.YYYY.-");
				if (!["Student", "Donor"].includes(frm.doc.party_type)) {
					frm.set_value("party_type", "Customer");
				}
			}
			else if (frm.doc.payment_type == "Pay") {
				frm.set_value("naming_series", "PE-.YYYY.-");
				if (frm.doc.party_type != "Employee") {
					frm.set_value("party_type", "Supplier");
				}
			}
			else if (frm.doc.payment_type == "Internal Transfer") {
				frm.set_value("naming_series", "IT-.YYYY.-");
				frm.set_value("party_type", "");
			}
		}
		frm.refresh_fields()
	},

	party: function (frm) {
		if (frm.is_new()) {
			const today = frappe.datetime.get_today();
			const filters = {
				from_posting_date: frappe.datetime.add_days(today, -3650),
				to_posting_date: today,
				allocate_payment_amount: 1
			}
			if (["Customer", "Supplier"].includes(frm.doc.party_type)) {
				frm.events.get_outstanding_documents(frm, filters);
			}
		}
	},

	get_outstanding_documents: function (frm, filters) {
		if (typeof frappe.route_history[frappe.route_history.length - 2] != "undefined") {
			if (frappe.route_history[frappe.route_history.length - 2][1] in ["Sales Invoice", "Employee Advance", "Purchase Invoice"]) {
				return;
			}
		}

		frm.clear_table("references");

		if (!frm.doc.party) {
			return;
		}

		frm.events.check_mandatory_to_fetch(frm);
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;

		var args = {
			"posting_date": frm.doc.posting_date,
			"company": frm.doc.company,
			"party_type": frm.doc.party_type,
			"payment_type": frm.doc.payment_type,
			"party": frm.doc.party,
			"party_account": frm.doc.payment_type == "Receive" ? frm.doc.paid_from : frm.doc.paid_to,
			"cost_center": frm.doc.cost_center
		}

		for (let key in filters) {
			args[key] = filters[key];
		}

		frappe.flags.allocate_payment_amount = filters['allocate_payment_amount'];

		return frappe.call({
			method: 'csf_tz.csftz_hooks.payment_entry.get_outstanding_reference_documents',
			args: {
				args: args
			},
			callback: function (r, rt) {
				if (r.message) {
					var total_positive_outstanding = 0;
					var total_negative_outstanding = 0;

					$.each(r.message, function (i, d) {
						var c = frm.add_child("references");
						c.reference_doctype = d.voucher_type;
						c.reference_name = d.voucher_no;
						c.due_date = d.due_date
						c.total_amount = d.invoice_amount;
						c.outstanding_amount = d.outstanding_amount;
						c.bill_no = d.bill_no;

						if (!in_list(["Sales Order", "Purchase Order", "Expense Claim", "Fees"], d.voucher_type)) {
							if (flt(d.outstanding_amount) > 0)
								total_positive_outstanding += flt(d.outstanding_amount);
							else
								total_negative_outstanding += Math.abs(flt(d.outstanding_amount));
						}

						var party_account_currency = frm.doc.payment_type == "Receive" ?
							frm.doc.paid_from_account_currency : frm.doc.paid_to_account_currency;

						if (party_account_currency != company_currency) {
							c.exchange_rate = d.exchange_rate;
						} else {
							c.exchange_rate = 1;
						}
						if (in_list(['Sales Invoice', 'Purchase Invoice', "Expense Claim", "Fees"], d.reference_doctype)) {
							c.due_date = d.due_date;
						}
					});

					if (
						(frm.doc.payment_type == "Receive" && frm.doc.party_type == "Customer") ||
						(frm.doc.payment_type == "Pay" && frm.doc.party_type == "Supplier") ||
						(frm.doc.payment_type == "Pay" && frm.doc.party_type == "Employee") ||
						(frm.doc.payment_type == "Receive" && frm.doc.party_type == "Student")
					) {
						if (total_positive_outstanding > total_negative_outstanding)
							if (!frm.doc.paid_amount)
								frm.set_value("paid_amount",
									total_positive_outstanding - total_negative_outstanding);
					} else if (
						total_negative_outstanding &&
						total_positive_outstanding < total_negative_outstanding
					) {
						if (!frm.doc.received_amount)
							frm.set_value("received_amount",
								total_negative_outstanding - total_positive_outstanding);
					}
				}

				frm.events.allocate_party_amount_against_ref_docs(frm,
					(frm.doc.payment_type == "Receive" ? frm.doc.paid_amount : frm.doc.received_amount));

			}
		});
	},
});
