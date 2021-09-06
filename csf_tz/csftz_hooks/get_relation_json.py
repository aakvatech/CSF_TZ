import frappe
import json

def get_json():

    doc_list = frappe.db.sql(
        """SELECT CONCAT_WS('.', "erpnext", dt.module, dt.name) as name, dt.name as doctype_name
        FROM `tabDocType` dt
        INNER JOIN `tabDocField` df ON dt.name = df.parent
        WHERE df.options IS NOT NULL
        AND df.fieldtype = "Link"
        GROUP BY dt.module, dt.name
        UNION ALL
        SELECT CONCAT_WS('.', "erpnext", dt.module, dt.name) as name, dt.name as doctype_name
        FROM `tabDocType` dt
        INNER JOIN `tabCustom Field` df ON dt.name = df.parent
        WHERE df.options IS NOT NULL
        AND df.fieldtype = "Link"
        GROUP BY dt.module, dt.name""", as_dict=1)
    
    for doc in doc_list:
        docfield_list = frappe.get_all("DocField", filters={"parent": doc.doctype_name, "fieldtype": "Link"}, fields="options", group_by="options")
        custom_field_list = frappe.get_all("Custom Field", filters={"parent": doc.doctype_name, "fieldtype": "Link"}, fields="options", group_by="options")
        doc["imports"] = []
        for options in docfield_list:
            options_string = "erpnext." + frappe.get_value("DocType", doc.doctype_name, "module") + "." + options.get("options")
            doc["imports"].append(options_string)
        for options in custom_field_list:
            options_string = "erpnext." + frappe.get_value("DocType", doc.doctype_name, "module") + "." + options.get("options")
            doc["imports"].append(options_string)

    return json.dumps(doc_list)
