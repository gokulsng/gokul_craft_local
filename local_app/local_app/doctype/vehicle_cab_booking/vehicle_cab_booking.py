# Copyright (c) 2024, Gokul and contributors
# For license information, please see license.txt
import json
import frappe
from datetime import time, timedelta,datetime
from frappe.model.document import Document
from frappe.utils import now


class VehicleCabBooking(Document):
	pass




@frappe.whitelist()
def set_filters(data):
	data1 = json.loads(data)
	start_d = datetime.strptime(data1['start_date'],"%Y-%m-%d %H:%M:%S")
	end_d = datetime.strptime(data1['end_date'],"%Y-%m-%d %H:%M:%S")

	out = frappe.db.sql(""" select name from `tabVehicle Cab Booking` where 
			start_date >= '{0}'and start_date <= '{1}' or
			end_date >= '{0}' and end_date <= '{1}' and from_location = '{2}' """.format(start_d,end_d,data1['from_location']))
	list = []
	if out:
		list1 = []
		for val in out:
			vehicle_cab = frappe.get_doc("Vehicle Cab Booking",val[0])
			vehicle_det = frappe.get_doc("Vehicle",vehicle_cab.vehicle_number)
			list1.append(vehicle_det.name)
		list.append(list1)
		list.append(data1['from_location'])
		return list
	else:
		return list




@frappe.whitelist()
def add_minutes(sdate,edate):
	stdate = sdate.split(' (')[0]
	parse_sdate = datetime.strptime(stdate, '%a %b %d %Y %H:%M:%S GMT%z')
	sdate1 = datetime.strftime(parse_sdate,"%Y-%m-%d %H:%M:%S")

	endate = edate.split(' (')[0]
	parse_edate = datetime.strptime(endate, '%a %b %d %Y %H:%M:%S GMT%z')
	edate1 = datetime.strftime(parse_edate,"%Y-%m-%d %H:%M:%S")
	return sdate1,edate1


@frappe.whitelist()
def status_update(doc):
	vehicle_booking = frappe.get_doc("Vehicle Cab Booking",doc)
	vehicle = frappe.get_doc("Vehicle",{"name":vehicle_booking.vehicle_number})
	now = datetime.now()
	sdate1 = now.replace(minute=0, second=0, microsecond=0)
	edate1 = now.replace(minute=30, second=0, microsecond=0)
	if vehicle_booking.start_date == sdate1 or vehicle_booking.start_date == edate1:
		vehicle.custom_status = 'Booked'
		# frappe.errprint(vehicle.custom_status)
		vehicle.save()
		vehicle_booking.status = "Trip Started"
		# vehicle_booking.save()
		# frappe.errprint(vehicle.as_dict())


@frappe.whitelist()
def cron_status_update():
	vehicle_booking = frappe.get_list("Vehicle Cab Booking")
	# frappe.errprint(vehicle_booking)
	if vehicle_booking:
		for booking in vehicle_booking:
			vehicle_book = frappe.get_doc("Vehicle Cab Booking",booking)
			now = datetime.now()
			new_time = now.replace(second=0, microsecond=0)
			if vehicle_book.status == "Yet to Start" and vehicle_book.start_date == new_time:
				vehicle = frappe.get_doc("Vehicle",vehicle_book.vehicle_number)
				vehicle_1 = frappe.get_doc("Vehicle Cab Booking",booking)
				vehicle.custom_status = 'Booked'
				vehicle.save()
				vehicle_1.status = "Trip Started"
				vehicle_1.save()
	
	vehicle_booking_c = frappe.get_list("Vehicle Cab Booking")
	if vehicle_booking_c:
		for booking_c in vehicle_booking_c:
			vehicle_book_c = frappe.get_doc("Vehicle Cab Booking",booking_c)
			now = datetime.now()
			now_time = now.replace(second=0, microsecond=0)
			if vehicle_book_c.status == "Trip Started" and vehicle_book_c.end_date == now_time:
				vehicle_c = frappe.get_doc("Vehicle",vehicle_book_c.vehicle_number)
				vehicle_1 = frappe.get_doc("Vehicle Cab Booking",booking)
				vehicle_c.custom_status = 'Available'
				vehicle_c.location = booking_c.to_location
				vehicle_c.save()
				vehicle_1.status = "Trip Completed"
				vehicle_1.save()
	# frappe.reload_doc("local_app","Vehicle Cab Booking")