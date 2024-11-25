// Copyright (c) 2024, Gokul and contributors
// For license information, please see license.txt

frappe.query_reports["Event Details"] = {
	"filters": [
		{
			"fieldname":"name",
			"label": __("Event Details"),
			"fieldtype": "Link",
			"options": "Event Details"
		},
		{
			"fieldname":"event_organiser",
			"label": __("Event Organiser"),
			"fieldtype": "Link",
			"options" : "Employee"
		},{
			"fieldname":"hall_number",
			"label": __("Hall Number"),
			"fieldtype": "Data",
		},
		{
			"fieldname":"event_capacity",
			"label": __("Event Capacity"),
			"fieldtype": "Data",
		},
		{
			"fieldname":"event_start_date",
			"label": __("From Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"event_end_date",
			"label": __("End Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"participants",
			"label": __("Participants"),
			"fieldtype": "Select",
			"options" : ["Employee Participants", "Public Participants"],
			"default": "Employee Participants"
		}
	]
};
