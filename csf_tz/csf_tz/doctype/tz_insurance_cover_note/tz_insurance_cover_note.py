# Copyright (c) 2022, Aakvatech and contributors
# For license information, please see license.txt

import frappe
import requests
import json
from datetime import datetime
from frappe.utils import cint
from frappe.model.document import Document

class TZInsuranceCoverNote(Document):
	pass

@frappe.whitelist()
def update_covernote_docs():
    """Create or Update covernote document after getting necessary details from Tira.

    The routine to create or update covernote document runs at 00:00 AM on the 1st day of every month.
    For example:
        for June: the routine will run at 00:00 AM, June 1, 2022.
    """
    
    motor_vehicles = frappe.get_all('Vehicle', ['number_plate', 'license_plate'])
    for vehicle in motor_vehicles:
        plate = vehicle.number_plate if vehicle.number_plate else vehicle.license_plate
        if plate is not None:
            req = get_covernote_details(plate)
            try:
                for record in req.get('data'):
                    if not frappe.db.exists('TZ Insurance Cover Note', record['coverNoteNumber']):
                        doc = frappe.new_doc('TZ Insurance Cover Note')
                    else:
                        doc = frappe.get_doc('TZ Insurance Cover Note', record['coverNoteNumber'])

                    for key, value in record.items():
                        if key.lower() == 'motor':
                            row = {}
                            doc.insurance_motors = []
                            for motor_child_key, motor_child_value in value.items():
                                motor_new_value = None
                                if motor_child_value and motor_child_key.lower() in ['createddate', 'updateddate']:
                                    unix_timestamp_int = cint(motor_child_value)
                                    motor_new_value = datetime.utcfromtimestamp((unix_timestamp_int/1000)).strftime('%Y-%m-%d %H:%M:%S')
                                else:
                                    motor_new_value = motor_child_value

                                row[motor_child_key.lower()] = motor_new_value

                            doc.append('insurance_motors', row)

                        elif key.lower() == 'company':
                            row = {}
                            doc.insurance_provider = []
                            for company_child_key, company_child_value in value.items():
                                company_new_value = None
                                if company_child_value and company_child_key.lower() in ['createddate', 'updateddate', 'incorporationdate', 'initialregistrationdate', 'businesscommencementdate']:
                                    unix_timestamp_int = cint(company_child_value)
                                    company_new_value = datetime.utcfromtimestamp((unix_timestamp_int/1000)).strftime('%Y-%m-%d %H:%M:%S')
                                elif company_child_key.lower() == 'shareholders':
                                    company_new_value = json.dumps(company_child_value)
                                else:
                                    company_new_value = company_child_value

                                row[company_child_key.lower()] = company_new_value

                            doc.append('insurance_provider', row)

                        elif key.lower() == 'policyholders':
                            doc.policy_holders = []
                            for i, row in enumerate(value):
                                new_row = {}
                                for policy_child_key, policy_child_value in row.items():
                                    policy_new_value = None
                                    if policy_child_value and policy_child_key.lower() in ['createddate', 'updateddate', 'policyholderbirthdate']:
                                        unix_timestamp_int = cint(policy_child_value)
                                        policy_new_value = datetime.utcfromtimestamp((unix_timestamp_int/1000)).strftime('%Y-%m-%d %H:%M:%S')
                                    else:
                                        policy_new_value = policy_child_value

                                    new_row[policy_child_key.lower()] = policy_new_value

                                doc.append('policy_holders', new_row)

                        elif key.lower() not in ['covernotestartdate', 'covernoteenddate', 'company', 'motor', 'policyholders']:
                            doc.update({key.lower(): value})

                        elif key.lower() in ['covernotestartdate', 'covernoteenddate']:
                            unix_timestamp_int = cint(value)
                            date_value = datetime.utcfromtimestamp((unix_timestamp_int/1000.0)).strftime('%Y-%m-%d %H:%M:%S')
                            doc.update({key.lower(): date_value})

                    doc.vehicle = vehicle.name
                    doc.save(ignore_permissions=True)

            except Exception as e:
                frappe.log_error(frappe.get_traceback(), str(e))

    frappe.db.commit()
    return True

def get_covernote_details(regnumber):
	"""Fetch motor insurance details from tira

	:param regnumber: car registration number
	"""
	url = "https://tiramis.tira.go.tz/covernote/api/public/portal/verify"

	payload = json.dumps({
        "paramType": 2,
        "searchParam": regnumber
    })
	headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

	try:
		response = requests.post(url, headers=headers, data=payload, timeout=3000, verify=False)
		if response.status_code == 200:
			return json.loads(response.text)
		else:
			frappe.log_error(response.text, str(response.status_code))

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), str(e))


