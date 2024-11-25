# Copyright (c) 2024, Gokul and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class EventDetails(Document):
	pass
	def validate(self):
		list = frappe.db.get_all("Event Details")
		s_date = datetime.strptime(self.event_start_date, '%Y-%m-%d %H:%M:%S')
		e_date = datetime.strptime(self.event_end_date, '%Y-%m-%d %H:%M:%S')
		for event in list:
			event_det = frappe.get_doc("Event Details",event.name)
			if event_det.hall_number == self.hall_number and event_det.event_start_date <= s_date <= event_det.event_end_date or event_det.event_start_date <= e_date <= event_det.event_end_date:
				# frappe.errprint(event_det.as_dict())
				frappe.throw("An event is already booked for this hall on this date and time.")

@frappe.whitelist()
def create_meeting_bookings(doct):
	event = frappe.get_doc("Event Details", doct)
	if frappe.get_all("Meeting Room Bookings",{"event_name":doct}):
		duplicate = frappe.get_doc("Meeting Room Bookings",{"event_name":doct})
		frappe.throw("""Meeting Room Bookings created Already.'<a href="/app/meeting-room-bookings/{0}">{0}</a>'""".format(duplicate.name))
	else:
		doc = frappe.new_doc("Meeting Room Bookings")
		doc.event_name = doct
		doc.employee_name = event.event_organiser
		doc.employee_nname = event.organiser_name
		doc.capacity_needed = event.event_capacity
		doc.meeting_room_number = event.hall_number
		doc.start_date_and_time = event.event_start_date
		doc.end_date_and_time = event.event_end_date
		doc.meeting_hours = event.event_end_date - event.event_start_date
		doc.insert()
		doc.save()


# @frappe.whitelist()
# def validate_bookings(hall_number,start_date,end_date):
# 	list = frappe.db.get_all("Event Details")
# 	# frappe.errprint(hall_number)
# 	# frappe.errprint(start_date)
# 	# frappe.errprint(end_date)
# 	# frappe.errprint(list)
# 	s_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
# 	e_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
# 	for event in list:
# 		event_det = frappe.get_doc("Event Details",event.name)
# 		if event_det.hall_number == hall_number and event_det.event_start_date <= s_date <= event_det.event_end_date or event_det.event_start_date <= e_date <= event_det.event_end_date:
# 			frappe.throw("An event is already booked for this hall and date.")