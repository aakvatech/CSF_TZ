import frappe

from frappe.desk import query_report

# override print formats
old_get_script = query_report.get_script


@frappe.whitelist()
def get_script(report_name):
    old_result = old_get_script(report_name)

    if not frappe.db.exists("AV Report Extension", report_name):
        return old_result
    av_report_extension_doc = frappe.get_doc("AV Report Extension", report_name)
    if av_report_extension_doc.active:
        if av_report_extension_doc.script:
            old_result["script"] = av_report_extension_doc.script
        if av_report_extension_doc.html_format:
            old_result["html_format"] = av_report_extension_doc.html_format

    return old_result


query_report.get_script = get_script
