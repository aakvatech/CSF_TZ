// Copyright (c) 2020, Aakvatech and contributors
// For license information, please see license.txt

frappe.ui.form.on('CSF TZ Settings', {
	start_sle_gle_reporting: function (frm) {
        frappe.call({
            method: 'csf_tz.csftz_hooks.item_reposting.enqueue_reposting_sle_gle',
            callback: function (data) {
                console.log(data);
            }
        })
    },
});
