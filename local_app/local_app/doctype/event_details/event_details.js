// Copyright (c) 2024, Gokul and contributors
// For license information, please see license.txt

frappe.ui.form.on("Event Details", {
    event_capacity(frm){
	    let capacity = frm.doc.event_capacity;
		frm.set_query("hall_number", function() {
		    return {
                filters :[ 
                    ["room_capacity", ">", capacity],
                    ["room_status" ,"=", "Active"]
                ]
            };
		});
	},
	refresh(frm) {
        if(!frm.is_new())
        {
            frm.add_custom_button(__('Create Meeting Room Bookings'), function()
            {
                frappe.call({
                    method: "local_app.local_app.doctype.event_details.event_details.create_meeting_bookings",
                    args: {
                        "doct": frm.doc.name
                    },
                    callback: function(r){
	                    frappe.msgprint(__('New Meeting Room Booking created successfully'));
                    }
                });
        });
        }
	},
    // validate(frm){
    //     frappe.call({
    //         method: "local_app.local_app.doctype.event_details.event_details.validate_bookings",
    //         args: {
    //             "hall_number": frm.doc.hall_number,
    //             "start_date" : frm.doc.event_start_date,
    //             "end_date" : frm.doc.event_end_date
    //         },
    //         callback: function(r){
    //             // frappe.msgprint(__('New Meeting Room Booking created successfully'));
    //         }
    //     });
    // }
});
