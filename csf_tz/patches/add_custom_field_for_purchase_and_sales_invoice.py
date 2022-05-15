import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    new_fields = {
        'Purchase Invoice': [
            dict(fieldname='csf_tz_specifics', label='CSF TZ Specifics', fieldtype='Section Break', insert_after='hold_comment'),
            dict(fieldname='csf_tz_wtax_jv_created', label='CSF TZ Wtax JV Created', fieldtype='Check', insert_after='csf_tz_specifics',
            allow_on_submit=1)
        ],
        'Sales Invoice': [
            dict(fieldname='csf_tz_specifics', label='CSF TZ Specifics', fieldtype='Section Break', insert_after='language'),
            dict(fieldname='csf_tz_wtax_jv_created', label='CSF TZ Wtax JV Created', fieldtype='Check', insert_after='csf_tz_specifics',
            allow_on_submit=1)
        ],
    }

    create_custom_fields(new_fields, update=True)