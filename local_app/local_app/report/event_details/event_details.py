# Copyright (c) 2024, Gokul and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import datetime
from datetime import datetime

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	# print(columns,data)
	return columns, data


def get_columns(filters = None):
	columns = []
	columns.append(
	{
		"label": _("Event Name"),
		"fieldname": "name",
		"fieldtype": "Link",
		"options": "Event Details",
		"width": 120,
	})
	columns.append(
	{
		"label": _("Event"),
		"fieldname": "event",
		"fieldtype": "Data",
		"width": 120,
	})
	columns.append(
	{
		"label": _("Hall Number"),
		"fieldname": "hall_number",
		"fieldtype": "Data",
		"width": 120,
	})
	columns.append(
	{
		"label": _("Event Organiser"),
		"fieldname": "event_organiser",
		"fieldtype": "Link",
		"options": "Employee",
		"width": 120,
	})
	columns.append(
	{
		"label": _("Event Start Date"),
		"fieldname": "event_start_date",
		"fieldtype": "Datetime",
		"width": 120,
	})
	columns.append(
	{
		"label": _("Event End Date"),
		"fieldname": "event_end_date",
		"fieldtype": "Datetime",
		"width": 120,
	})
	columns.append(
	{
		"label": _("Event Capacity"),
		"fieldname": "event_capacity",
		"fieldtype": "Data",
		"width": 120,
	})
	columns.append({
		"label": _("Participants"),
		"fieldname":"participants",
		"fieldtype": "Data",
		"width": 120,
	})
	# columns.append(													# with both employee and other participants list
	# {
	# 	"label": _("Employee Participants"),
	# 	"fieldname": "employee_participants",
	# 	"fieldtype": "Data",
	# 	"width": 120,
	# })
	# columns.append(
	# {
	# 	"label": _("Other Participants"),
	# 	"fieldname": "participants",
	# 	"fieldtype": "Data",
	# 	"width": 120,
	# })

	return columns



def get_data(filters):
	data = []
	conditions = ""
	# print(filters)
	if filters and filters.name and conditions == "":
		conditions = " ed.name = '{0}'".format(filters.name)
	elif filters.name:
		conditions += " and ed.name = '{0}'".format(filters.name)

	if filters.event_organiser and conditions == "":
		conditions = " ed.event_organiser = '{0}'".format(filters.event_organiser)
	elif filters.event_organiser:
		conditions += " and ed.event_organiser = '{0}'".format(filters.event_organiser)

	if filters.hall_number and conditions == "":
		conditions = " ed.hall_number = '{0}'".format(filters.hall_number)
	elif filters.hall_number:
		conditions += " and ed.hall_number = '{0}'".format(filters.hall_number)

	if filters.event_capacity and conditions == "":
		conditions = " ed.event_capacity = '{0}'".format(filters.event_capacity)
	elif filters.event_capacity:
		conditions += " and ed.event_capacity = '{0}'".format(filters.event_capacity)

	if filters.event_start_date and filters.event_end_date and conditions == "":
		conditions = " ed.event_start_date >= '{0}' and ed.event_start_date <= '{1}'".format(filters.event_start_date,filters.event_end_date)
	elif filters.event_start_date and filters.filters_end_date:
		conditions +=  " and ed.event_start_date >= '{0}' and ed.event_start_date <= '{1}'".format(filters.event_start_date,filters.event_end_date)

	if filters.event_start_date and filters.event_end_date and conditions == "":
		conditions = " event_end_date >= '{0}' and event_end_date <= '{1}'".format(filters.event_end_date,filters.event_end_date)
	elif filters.event_end_date and filters.event_end_date:
		conditions +=  "and event_end_date >= '{0}' and event_end_date <= '{1}'".format(filters.event_start_date,filters.event_end_date)
	# print(conditions)
	# if conditions:
	 							# It is for both employee and other participants
	# data = frappe.db.sql("""
	# 	Select
	# 		ed.name,
	# 		ed.event_name as event,
	# 		ed.hall_number,
	# 		ed.event_organiser,
	# 		ed.event_start_date,
	# 		ed.event_end_date,
	# 		ed.event_capacity,
	# 		NULL as employee_participants,
	# 		pd.participant_name as participants
	# 	from
	# 		`tabEvent Details` as ed
	# 	left join `tabPublic Details` as pd ON ed.name = pd.parent
	# 	where 
	# 		{0}
	# 	union all
	# 	Select
	# 		distinct
	# 		ed.name,
	# 		ed.event_name as event,
	# 		ed.hall_number,
	# 		ed.event_organiser,
	# 		ed.event_start_date,
	# 		ed.event_end_date,
	# 		ed.event_capacity,
	# 		empd.employee_name as employee_participants,
	# 		NULL as participants
	# 	from
	# 		`tabEvent Details` as ed
	# 	left join `tabEmployee Participation list` as empd ON ed.name = empd.parent
	# 	where 
	# 		{0}
	# 	order by
	# 		name """.format(conditions),as_dict=1)


	if filters.participants == "Employee Participants" : 												# It is for either employee or other participants
		data = frappe.db.sql("""
			Select
				ed.name,
				ed.event_name as event,
				ed.hall_number,
				ed.event_organiser,
				ed.event_start_date,
				ed.event_end_date,
				ed.event_capacity,
				if(ISNULL(empd.employee_name),NULL, empd.employee_name) as participants
			from
		 		`tabEvent Details` as ed
			left join
				`tabEmployee Participation list` as empd
			on
				ed.name = empd.parent
			where
				{0}""".format(conditions),as_dict=1)
		
	if filters.participants == "Public Participants" : 												# It is for either employee or other participants
		data = frappe.db.sql("""
			Select
				ed.name,
				ed.event_name as event,
				ed.hall_number,
				ed.event_organiser,
				ed.event_start_date,
				ed.event_end_date,
				ed.event_capacity,
				if(ISNULL(pd.participant_name),NULL, pd.participant_name) as participants
			from
		 		`tabEvent Details` as ed
			left join
				`tabPublic Details` as pd 
			on
				ed.name = pd.parent
			where
				{0}""".format(conditions),as_dict=1)


	# print("\n\n\n\n")
	# print(data)
	# print("\n\n\n\n")
	# data = frappe.db.sql(""" select ed.name, ed.event_name as event, ed.hall_number, ed.event_organiser,
	# 	ed.event_start_date, ed.event_end_date, ed.event_capacity,coalesce(empd.employee_name,"") as employee_participants, 
	# 	coalesce(pd.participant_name,"") as participants from `tabEvent Details` ed,`tabEmployee Participation list` empd,
	# 	`tabPublic Details` pd  where empd.parent = ed.name and pd.parent = ed.name""")
	# else:
	# 	data = frappe.db.sql(""" Select name, event_name as event, hall_number, event_organiser, 
	# 		event_start_date, event_end_date, event_capacity from `tabEvent Details`""")
	row1 = row2 = row3 = row4 = row5 = row6 = row7 = None
	for column in data:
		if column["name"] == row1:
			column["name"] = ""
		else:
			row1 = column["name"]
			
		if column["event"] == row2 and column["name"] != row1:
			column["event"] = ""
		else:
			row2 = column["event"]
		if column["hall_number"] == row3 and column["name"] != row1:
			column["hall_number"] = ""
		else:
			row3 = column["hall_number"]
		if column["event_organiser"] == row4 and column["name"] != row1:
			column["event_organiser"] = ""
		else:
			row4 = column["event_organiser"]
		if column["event_start_date"] == row5 and column["name"] != row1:
			column["event_start_date"] = ""
		else:
			row5 = column["event_start_date"]
		if column["event_end_date"] == row6 and column["name"] != row1:
			column["event_end_date"] = ""
		else:
			row6 = column["event_end_date"]
		if column["event_capacity"] == row7 and column["name"] != row1:
			column["event_capacity"] = ""
		else:
			row7 = column["event_capacity"]
	return data