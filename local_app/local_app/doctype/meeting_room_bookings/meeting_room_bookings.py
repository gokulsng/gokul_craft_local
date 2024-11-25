# Copyright (c) 2024, Gokul and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document


class MeetingRoomBookings(Document):
	pass
	def validate(self):
		if not(self.event_name) :
			list = frappe.db.get_all("Meeting Room Bookings")
			s_date = datetime.strptime(self.start_date_and_time, '%Y-%m-%d %H:%M:%S')
			e_date = datetime.strptime(self.end_date_and_time, '%Y-%m-%d %H:%M:%S')
			self.meeting_hours = e_date - s_date
			for event in list:
				event_det = frappe.get_doc("Meeting Room Bookings",event.name)
				if event_det.meeting_room_number == self.meeting_room_number and event_det.start_date_and_time <= s_date <= event_det.end_date_and_time or event_det.start_date_and_time <= e_date <= event_det.end_date_and_time:
					frappe.errprint(event_det.as_dict())
					frappe.throw("An event is already booked for this hall on this date and time.")
		# frappe.throw("__________________")

# @frappe.whitelist()
# def validate_bookings(hall_number,start_date,end_date):
# 	pass
	# list = frappe.db.get_all("Meeting Room Bookings")
	# # frappe.errprint(hall_number)
	# # frappe.errprint(start_date)
	# # frappe.errprint(end_date)
	# frappe.errprint(list)
	# s_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
	# e_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
	# for event in list:
	# 	event_det = frappe.get_doc("Meeting Room Bookings",event.name)
	# 	if event_det.meeting_room_number == hall_number and event_det.start_date_and_time <= s_date <= event_det.end_date_and_time or event_det.start_date_and_time <= e_date <= event_det.end_date_and_time:
	# 		frappe.errprint(event_det.as_dict())
	# 		frappe.throw("An event is already booked for this hall and date.")