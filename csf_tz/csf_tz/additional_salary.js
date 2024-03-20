frappe.ui.form.on('Additional Salary', {
	refresh: function(frm) {
		cur_frm.add_custom_button(__("Generate Additional Salary Records"), function() {
			frappe.call({
				method: "csf_tz.csftz_hooks.additional_salary.generate_additional_salary_records",
				args: {},
				callback: function () {
					cur_frm.reload_doc();
				}
			});
		});
	},
	payroll_date: function(frm) {
		if (!frm.doc.payroll_date) {
			frm.set_value("no_of_hours", null);
		}
	},
	employee: function(frm) {
		if (!frm.doc.employee) {
			frm.set_value("no_of_hours", null);
		}
	},
	salary_component: function(frm) {
		if (!frm.doc.salary_component) {
			frm.set_value("based_on_hourly_rate", null);
			frm.set_value("hourly_rate", null);
		}
	},
	no_of_hours: function(frm) {
		if (frm.doc.employee && frm.doc.payroll_date) {
			frappe.call({
				method: "csf_tz.csftz_hooks.additional_salary.get_employee_base_salary_in_hours",
				args: {
					employee: frm.doc.employee,
					payroll_date: frm.doc.payroll_date
				},
				async: false,
				callback: function(r) {
					console.log(r.message)
					if(r.message) {
						frm.set_value("amount", frm.doc.hourly_rate / 100 * frm.doc.no_of_hours * r.message.base_salary_in_hours);
					}
				}
			});	
		}
	},
});
