frappe.ui.form.on('Landed Cost Voucher', {
    validate: function(frm) {
        $.each(frm.doc.items, function(i, d) {
            var applicable_item = d.applicable_charges / d.qty;
            var price_item = applicable_item + (d.amount / d.qty);
            frappe.model.set_value(d.doctype, d.name, "applicable_charges_per_item", applicable_item);
            frappe.model.set_value(d.doctype, d.name, "price_per_item", price_item);
        });
    }
});
