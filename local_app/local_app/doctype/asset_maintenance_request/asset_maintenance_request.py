# Copyright (c) 2024, Gokul and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AssetMaintenanceRequest(Document):
	pass


@frappe.whitelist()
def create_task(asset_name):
	# pass
	doct = frappe.get_doc("Asset Maintenance Request",asset_name)
	if frappe.get_all("Task",{"custom_asset_maintenance_request":doct.name}):
		duplicate = frappe.get_doc("Task",{"custom_asset_maintenance_request":doct.name})
		frappe.throw("""A task is already created. '<a href="/app/task/{0}">{0}</a>'""".format(duplicate.name))
	else:
		# frappe.throw("_____")
		doc = frappe.new_doc("Task")
		doc.custom_asset_maintenance_request = doct.name
		frappe.utils.cint(doc.project)
		# frappe.errprint(doct.name[4:])
		# frappe.throw("____")
		doc.subject = doct.asset_name+"-"+doct.maintenance_type+"-"+ doct.name[4:]
		doc.custom_asset_name = doct.asset
		doc.custom_maintenance_type = doct.maintenance_type
		doc.status = doct.status
		doc.priority = doct.priority
		doc.insert()
		doc.save()
		doct.task = doc.name
		doct.save()
		frappe.msgprint('New Task has created successfully. <a href="/app/task/{0}">{0}</a>'.format(doc.name))
		return doct.name


@frappe.whitelist()
def create_asset_return(doct):
	amr = frappe.get_doc("Asset Maintenance Request",doct)
	task = frappe.get_doc("Task",amr.task)
	task.status = "Repair Completed"
	# task.custom_asset_return = asset_movement.name
	task.save()
	amr.status = "In Review"
	amr.save()
