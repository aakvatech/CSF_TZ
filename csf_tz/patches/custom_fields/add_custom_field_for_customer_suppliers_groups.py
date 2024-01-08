import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields = {
        "Customer Group":[
            dict(
                fieldname= "tax_category",
                fieldtype="Link",
                label="Tax Category",
                options= "Tax Category"
            ),
        ],
          "Supplier Group":[
            dict(
                fieldname= "tax_category",
                fieldtype="Link",
                label="Tax Category",
                options= "Tax Category"
            ),
        ],
        

    }
    create_custom_fields(fields, update=True)
    tax_categories = ['Sales', 'Purchase']
    for tax_category in tax_categories:
        if 'Sales' in tax_category:
            supplier_group_lists = frappe.get_all('Supplier Group')
            for supplier_group in supplier_group_lists:
                frappe.db.set_value('Supplier Group', supplier_group.name, 'tax_category', tax_category)
        elif 'Purchase' in tax_category:
            customer_group_lists = frappe.get_all('Customer Group')
            for customer_group in customer_group_lists:
                frappe.db.set_value('Customer Group', customer_group.name, 'tax_category', tax_category) 