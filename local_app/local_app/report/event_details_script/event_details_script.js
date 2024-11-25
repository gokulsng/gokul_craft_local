// Copyright (c) 2024, Gokul and contributors
// For license information, please see license.txt

frappe.query_reports["Event Details Script"] = {
	"filters": [
		{
			"fieldname":"name",
			"label": __("Event Details"),
			"fieldtype": "Link",
			"Options": "Event Details"
		},
		{
			"fieldname":"event_name",
			"label": __("Event Name"),
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
			"fieldtype": "Date",
			"default": frappe.utils.today()
		},
		{
			"fieldname":"event_end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"default": frappe.utils.today()
		},
	]
};
