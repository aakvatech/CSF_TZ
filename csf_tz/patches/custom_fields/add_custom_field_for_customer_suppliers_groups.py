import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields = {
        "Customer Group":[
            dict(
                fieldname= "tax_category",
                fieldtype="Link",
                label="Tax Category",
                options= "Tax Category",
                default="Purchase"
            ),
        ],
          "Supplier Group":[
            dict(
                fieldname= "tax_category",
                fieldtype="Link",
                label="Tax Category",
                options= "Tax Category",
                default="Sales"
            ),
        ],
        

    }
    create_custom_fields(fields, update=True)