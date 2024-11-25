# Copyright (c) 2024, Gokul and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MeetingRooms(Document):
	pass

@frappe.whitelist()
def status_update(selfe,doct):
	# print(selfe,type(selfe))
	hall = frappe.get_doc("Meeting Room Bookings",doct)
	# print(hall.as_dict())
	if hall.workflow_state == "Approved":
		frappe.db.sql(""" UPDATE `tabMeeting Rooms` SET room_status='{0}' WHERE name='{1}' """.format("Occupied",int(selfe)))
	doc = frappe.get_doc("Meeting Rooms",selfe)
	if(hall.docstatus == 2):
		# print(doc.as_dict())
		for temp in doc.meeting_details:
			# print(temp.meeting_room_bookings)
			if temp.meeting_room_bookings == hall.name:
				doc.room_status = "Active"
				temp.status = hall.workflow_state
				doc.save()
	elif(hall.docstatus == 1):
		row = doc.append("meeting_details", {})
		row.employee_name = hall.employee_nname
		row.capacity_needed = hall.capacity_needed
		row.start_date_and_time = hall.start_date_and_time
		row.meeting_hours = hall.meeting_hours
		row.meeting_room_bookings = hall.name
		# print(hall.workflow_state)
		row.status = hall.workflow_state
		print(row.as_dict())
		print('/n')
		print(doc.as_dict())
		doc.save()
		frappe.db.commit()
