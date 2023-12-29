frappe.ui.form.on("Company", {
	
	setup: function(frm) {
		frm.set_query("default_withholding_payable_account", function() {
			return {
				"filters": {
                    "company": frm.doc.name,
                    "account_type": "Payable",
				}
			};
		});
		frm.set_query("default_withholding_receivable_account", function() {
			return {
				"filters": {
                    "company": frm.doc.name,
                    "account_type": "Receivable",
				}
			};
		});
		frm.set_query("fee_bank_account", function() {
			return {
				"filters": {
                    "company": frm.doc.name,
					"account_type": ["in",["Cash","Bank"]],
					"account_currency": frm.doc.default_currency,
				}
			};
		});
		frm.set_query("student_applicant_fees_revenue_account", function() {
			return {
				"filters": {
                    "company": frm.doc.name,
					"account_type": "Income Account",
					"account_currency": frm.doc.default_currency,
				}
			};
        });
	},
	refresh: function(frm) {
        frm.add_custom_button(__('Auto create accounts'), function() {
            frm.trigger("auto_create_account");
        }, __("Setup"));

        frm.add_custom_button(__('Create Item Tax Template'), function() {
            frm.trigger("create_tax_template");
        }, __("Setup"));

        frm.add_custom_button(__('Create Tax Category'), function() {
            frm.trigger("make_tax_category");
        }, __("Setup"));
    },

	auto_create_account: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.auto_create_account',
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Accounts created successfully.'));
				}
			}
		});
	},

	create_tax_template: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.create_tax_template',
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Tax Category and Item Tax Template created successfully.'));
				}
			}
		});
	},

	make_tax_category: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.create_tax_category',
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Tax Category created successfully.'));
				}
			}
		});
	}

	
});
