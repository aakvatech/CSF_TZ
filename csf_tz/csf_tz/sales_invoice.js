frappe.ui.form.on("Sales Invoice", {
    setup: function (frm) {

        // frm.trigger("update_stock");
    },
    refresh: function (frm) {
        frm.trigger("set_pos");
        frm.trigger("make_sales_invoice_btn");

    },
    onload: function (frm) {
        frm.trigger("set_pos");
        if (frm.doc.document_status == "Draft") {
            if (frm.doc.is_return == "0") {
                frm.set_value("naming_series", "ACC-SINV-.YYYY.-");
            }
            else if (frm.doc.is_return == "1") {
                frm.set_value("naming_series", "ACC-CN-.YYYY.-");
                frm.set_value("select_print_heading", "CREDIT NOTE");
            }
        }
        // frm.trigger("update_stock");
    },
    customer: function (frm) {
        setTimeout(function () {
            if (!frm.doc.customer) {
                return;
            }
            if (!frm.doc.tax_category) {
                frappe.call({
                    method: "csf_tz.custom_api.get_tax_category",
                    args: {
                        doc_type: frm.doc.doctype,
                        company: frm.doc.company,
                    },
                    callback: function (r) {
                        if (!r.exc) {
                            frm.set_value("tax_category", r.message);
                            frm.trigger("tax_category");
                        }
                    }
                });
            }
        }, 1000);
    },
    // update_stock: (frm) => {
    //     const warehouse_field = frappe.meta.get_docfield("Sales Invoice Item", "warehouse", frm.doc.name);
    //     const item_field = frappe.meta.get_docfield("Sales Invoice Item", "item_code", frm.doc.name);
    //     const qty_field = frappe.meta.get_docfield("Sales Invoice Item", "qty", frm.doc.name);
    //     if (frm.doc.update_stock){
    //         warehouse_field.in_list_view = 1;
    //         warehouse_field.idx = 3;
    //         warehouse_field.columns = 2;
    //         item_field.columns =3;
    //         qty_field.columns =1;
    //         refresh_field("items");
    //     }else{
    //         warehouse_field.in_list_view = 0;
    //         warehouse_field.columns = 0;
    //         item_field.columns =4;
    //         qty_field.columns =2;
    //         refresh_field("items");
    //     }
    // },
    make_sales_invoice_btn: function (frm) {
        if (frm.doc.docstatus == 1 && frm.doc.enabled_auto_create_delivery_notes == 1) {
            frm.add_custom_button(__('Create Delivery Note'),

                function () {
                    frappe.call({
                        method: "csf_tz.custom_api.create_delivery_note",
                        args: {
                            doc_name: frm.doc.name,
                            method: 1,
                        },
                    });
                });
        }
    },
    set_pos: function (frm) {
        frappe.db.get_value("CSF TZ Settings", {}, "auto_pos_for_role").then(r => {
            if (r.message) {
                if (
                    frappe.user_roles.includes(r.message.auto_pos_for_role) &&
                    frm.doc.docstatus == 0 &&
                    frappe.session.user != 'Administrator' &&
                    frm.doc.is_pos != 1
                ) {
                    frm.set_value("is_pos", true);
                    frm.set_df_property("is_pos", "read_only", true);
                }
            }
        });
    },
});

frappe.ui.form.on("Sales Invoice Item", {
    item_code: function (frm, cdt, cdn) {
        validate_item_remaining_qty(frm, cdt, cdn);
    },
    qty: function (frm, cdt, cdn) {
        validate_item_remaining_qty(frm, cdt, cdn);
    },
    stock_qty: function (frm, cdt, cdn) {
        validate_item_remaining_stock_qty(frm, cdt, cdn);
    },
    uom: function (frm, cdt, cdn) {
        validate_item_remaining_qty(frm, cdt, cdn);
    },
    allow_over_sell: function (frm, cdt, cdn) {
        validate_item_remaining_stock_qty(frm, cdt, cdn);
    },
    conversion_factor: function (frm, cdt, cdn) {
        validate_item_remaining_stock_qty(frm, cdt, cdn);
    },
    warehouse: function (frm, cdt, cdn) {
        validate_item_remaining_stock_qty(frm, cdt, cdn);
    },
});

var validate_item_remaining_qty = function (frm, cdt, cdn) {
    const item_row = locals[cdt][cdn];
    if (item_row.item_code == null) { return; }
    if (item_row.allow_over_sell == 1) { return; }
    const conversion_factor = get_conversion_factor(item_row, item_row.item_code, item_row.uom);
    frappe.call({
        method: 'csf_tz.custom_api.validate_item_remaining_qty',
        args: {
            item_code: item_row.item_code,
            company: frm.doc.company,
            warehouse: item_row.warehouse,
            stock_qty: item_row.qty * conversion_factor,
        },
        async: false,
    });
};

var validate_item_remaining_stock_qty = function (frm, cdt, cdn) {
    const item_row = locals[cdt][cdn];
    if (item_row.item_code == null) { return; }
    if (item_row.allow_over_sell == 1) { return; }
    frappe.call({
        method: 'csf_tz.custom_api.validate_item_remaining_qty',
        args: {
            item_code: item_row.item_code,
            company: frm.doc.company,
            warehouse: item_row.warehouse,
            stock_qty: item_row.stock_qty,
        },
        async: false,
    });
};


var get_conversion_factor = function (item_row, item_code, uom) {
    if (item_code && uom) {
        let conversion_factor = 0;
        frappe.call({
            method: "erpnext.stock.get_item_details.get_conversion_factor",
            child: item_row,
            args: {
                item_code: item_code,
                uom: uom
            },
            async: false,
            callback: function (r) {
                if (!r.exc) {

                    conversion_factor = r.message.conversion_factor;
                }
            }
        });
        return conversion_factor;
    }
};

frappe.ui.keys.add_shortcut({
    shortcut: 'ctrl+q',
    action: () => {
        const current_doc = $('.data-row.editable-row').parent().attr("data-name");
        const item_row = locals["Sales Invoice Item"][current_doc];
        frappe.call({
            method: 'csf_tz.custom_api.get_item_info',
            args: { item_code: item_row.item_code },
            callback: function (r) {
                if (r.message.length > 0) {
                    const d = new frappe.ui.Dialog({
                        title: __('Item Balance'),
                        width: 600
                    });
                    $(`<div class="modal-body ui-front">
                            <h2>${item_row.item_code} : ${item_row.qty}</h2>
                            <p>Choose Warehouse and click Select :</p>
                            <table class="table table-bordered">
                            <thead>
                            </thead>
                            <tbody>
                            </tbody>
                            </table>
                        </div>`).appendTo(d.body);
                    const thead = $(d.body).find('thead');
                    if (r.message[0].batch_no) {
                        r.message.sort((a, b) => a.expiry_status - b.expiry_status);
                        $(`<tr>
                            <th>Check</th>
                            <th>Warehouse</th>
                            <th>Qty</th>
                            <th>UOM</th>
                            <th>Batch No</th>
                            <th>Expires On</th>
                            <th>Expires in Days</th>
                            </tr>`).appendTo(thead);
                    } else {
                        $(`<tr>
                            <th>Check</th>
                            <th>Warehouse</th>
                            <th>Qty</th>
                            <th>UOM</th>
                            </tr>`).appendTo(thead);
                    }
                    r.message.forEach(element => {
                        const tbody = $(d.body).find('tbody');
                        const tr = $(`
                            <tr>
                                <td><input type="checkbox" class="check-warehouse" data-warehouse="${element.warehouse}"></td>
                                <td>${element.warehouse}</td>
                                <td>${element.actual_qty}</td>
                                <td>${item_row.stock_uom}</td>
                            </tr>
                            `).appendTo(tbody);
                        if (element.batch_no) {
                            $(`
                                    <td>${element.batch_no}</td>
                                    <td>${element.expires_on}</td>
                                    <td>${element.expiry_status}</td>
                                `).appendTo(tr);
                            tr.find('.check-warehouse').attr('data-batch', element.batch_no);
                            tr.find('.check-warehouse').attr('data-batchQty', element.actual_qty);
                        }
                        tbody.find('.check-warehouse').on('change', function () {
                            $('input.check-warehouse').not(this).prop('checked', false);
                        });
                    });
                    d.set_primary_action("Select", function () {
                        $(d.body).find('input:checked').each(function (i, input) {
                            frappe.model.set_value(item_row.doctype, item_row.name, 'warehouse', $(input).attr('data-warehouse'));
                            if ($(input).attr('data-batch')) {
                                frappe.model.set_value(item_row.doctype, item_row.name, 'batch_no', $(input).attr('data-batch'));
                            }
                        });
                        cur_frm.rec_dialog.hide();
                        cur_frm.refresh_fields();
                    });
                    cur_frm.rec_dialog = d;
                    d.show();
                }
                else {
                    frappe.show_alert({ message: __('There is No Records'), indicator: 'red' }, 5);
                }
            }
        });
    },
    page: this.page,
    description: __('Select Item Warehouse'),
    ignore_inputs: true,
});


frappe.ui.keys.add_shortcut({
    shortcut: 'ctrl+i',
    action: () => {
        const current_doc = $('.data-row.editable-row').parent().attr("data-name");
        const item_row = locals["Sales Invoice Item"][current_doc];
        new frappe.ui.form.SelectDialog({
            target: cur_frm,
            title: "Select The Rate",
            multi_select: 0,
            date_field: "posting_date",
            query_fields: [
                {
                    fieldname: "rate",
                    fieldtype: "Currency",
                    label: "Rate",
                    options: "currency",
                    precision: "2",
                    filter: 0
                },
                {
                    fieldname: "qty",
                    fieldtype: "Float",
                    label: "Qty",
                    filter: 0
                },
                {
                    fieldname: "invoice",
                    fieldtype: "Link",
                    label: "Invoice",
                    options: "Sales Invoice",
                    filter: 0
                },
                {
                    default: cur_frm.doc.customer,
                    fieldname: "customer",
                    fieldtype: "Link",
                    label: "Customer",
                    options: "Customer",
                    filter: 1
                },

            ],
            get_query () {
                return {
                    filters: {
                        item_code: item_row.item_code,
                        customer: "",
                        currency: cur_frm.doc.currency,
                        company: cur_frm.doc.company
                    },
                    query: "csf_tz.custom_api.get_item_prices_custom",
                };
            },
            return_field: "rate",
            action (selections) {
                console.log(selections);
                frappe.model.set_value(item_row.doctype, item_row.name, 'rate', selections[0]);
                cur_frm.refresh_fields();

            }
        });
    },
    page: this.page,
    description: __('Select Customer Item Price'),
    ignore_inputs: true,
});


frappe.ui.keys.add_shortcut({
    shortcut: 'ctrl+u',
    action: () => {
        const current_doc = $('.data-row.editable-row').parent().attr("data-name");
        const item_row = locals["Sales Invoice Item"][current_doc];
        frappe.call({
            method: 'csf_tz.custom_api.get_item_prices',
            args: {
                item_code: item_row.item_code,
                currency: cur_frm.doc.currency,
                company: cur_frm.doc.company
            },
            callback: function (r) {
                if (r.message.length > 0) {
                    const e = new frappe.ui.Dialog({
                        title: __('Item Prices'),
                        width: 600
                    });
                    $(`<div class="modal-body ui-front">
                            <h2>${item_row.item_code} : ${item_row.qty}</h2>
                            <p>Choose Price and click Select :</p>
                            <table class="table table-bordered">
                            <thead>
                            </thead>
                            <tbody>
                            </tbody>
                            </table>
                        </div>`).appendTo(e.body);
                    const thead = $(e.body).find('thead');
                    $(`<tr>
                            <th>Check</th>
                            <th>Rate</th>
                            <th>Qty</th>
                            <th>Date</th>
                            <th>Invoice</th>
                            <th>Customer</th>
                        </tr>`).appendTo(thead);
                    r.message.forEach(element => {
                        const tbody = $(e.body).find('tbody');
                        const tr = $(`
                            <tr>
                                <td><input type="checkbox" class="check-rate" data-rate="${element.price}"></td>
                                <td>${element.price}</td>
                                <td>${element.qty}</td>
                                <td>${element.date}</td>
                                <td>${element.invoice}</td>
                                <td>${element.customer}</td>
                            </tr>
                            `).appendTo(tbody);

                        tbody.find('.check-rate').on('change', function () {
                            $('input.check-rate').not(this).prop('checked', false);
                        });
                    });
                    e.set_primary_action("Select", function () {
                        $(e.body).find('input:checked').each(function (i, input) {
                            frappe.model.set_value(item_row.doctype, item_row.name, 'rate', $(input).attr('data-rate'));
                        });
                        cur_frm.rec_dialog.hide();
                        cur_frm.refresh_fields();
                    });
                    cur_frm.rec_dialog = e;
                    e.show();
                }
                else {
                    frappe.show_alert({ message: __('There is No Records'), indicator: 'red' }, 5);
                }
            }
        });
    },
    page: this.page,
    description: __('Select Item Price'),
    ignore_inputs: true,
});