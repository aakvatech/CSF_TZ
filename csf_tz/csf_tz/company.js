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
		frm.add_custom_button(__('Create Salary Component'), function() {
			frm.trigger("make_salary_components_and_structure");
		}, __("Setup"));
		frm.add_custom_button(__('Link Item Tax Template'), function() {
			let d = new frappe.ui.Dialog({
				title: 'Enter details',
				fields: [
					{
						fieldtype: 'Link',
						options: 'Item Tax Template',
						label: __('Item Tax Category'),
						fieldname: 'default_tax_template',
						reqd: 1
					}
				],
				primary_action_label: 'Submit',
				primary_action(values) {
					console.log(values);
		
					frappe.call({
						method: 'csf_tz.custom_api.linking_tax_template',
						args: {
							doctype: 'Item',
							default_tax_template: {
								default_tax_template: values.default_tax_template
							}
						},
						callback: function(response) {
							if (response.message) {
								frappe.msgprint(__('Item Tax Template Linked successfully.'));
							}
						}
					});
		
					d.hide();
				}
			});
		
			d.show();
		}, __("Setup"));
		
		frm.add_custom_button(__('TRA Asset Cartegories'), function() {
			frm.trigger("tra_asset_components");
		}, __("Setup"));
		
	},

	auto_create_account: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.auto_create_account',
			args: {
				abbr: frm.doc.abbr
			},
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Accounts created successfully.'));
				}
			}
		})
	},
	create_tax_template: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.create_item_tax_template',
			args: {
				abbr: frm.doc.abbr
			},
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Item Tax Templates created successfully.'));
				}
			}
		})
	},
	
	make_tax_category: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.create_tax_category',
			args: {
				abbr: frm.doc.abbr
			},
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Tax Category created successfully.'));
				}
			}
		})
	},
	make_salary_components_and_structure: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.make_salary_components_and_structure',
			args: {
				abbr: frm.doc.abbr
			},
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('Salary Components and Structure are created successfully.'));
				}
			}
		})
	},
	tra_asset_components: function(frm) {
		frappe.call({
			method: 'csf_tz.custom_api.tra_asset_components',
			args: {
				abbr: frm.doc.abbr
			},
			callback: function(response) {
				if (response.message) {
					frappe.msgprint(__('TRA Asset cartegoies are created successfully.'));
				}
			}
		})
	},
});