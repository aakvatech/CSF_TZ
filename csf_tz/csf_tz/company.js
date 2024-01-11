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
		frm.add_custom_button(__('create Item Tax Template'), function() {
			frm.trigger("create_tax_template");
		}, __("Setup"));
		frm.add_custom_button(__('Create Tax Category'), function() {
			frm.trigger("make_tax_category");
		}, __("Setup"));
		frm.add_custom_button(__('Linking Tax Template'), function () {
			let d = new frappe.ui.Dialog({
				title: 'Automation',
				fields: [
					{
						label: 'Item Tax Template',
						fieldname: 'item_tax_template',
						fieldtype: 'Link',
						options: 'Item Tax Template',
						// Add other field properties as needed
					},
				],
				primary_action_label: 'Submit',
				primary_action: function (values) {
					frappe.call({
						method: "csf_tz.custom_api.linking_tax_template",
						args: {
							item_tax_template: values.item_tax_template
						},
						freeze: true,
						callback: function (r) {
							frappe.msgprint(__("Linking Tax Template and Tax Category."));
							frm.reload_doc();
						}
					});
					d.hide();
				}
			});
			d.show();
		}, __("Setup"));
		frm.add_custom_button(__('Create Salary Components'), function() {
			frm.trigger("make_salary_components");
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
		})
	},
	create_tax_template: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.create_tax_template',
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Tax Category created successfully.'));
				}
			}
		})
	},
	
	make_tax_category: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.create_tax_category',
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Tax Category created successfully.'));
				}
			}
		})
	},
	
	make_salary_components: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.make_salary_components',
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Salary Components created successfully.'));
				}
			}
		})
	},
});
