// Copyright (c) 2024, Gokul and contributors
// For license information, please see license.txt
var mins = ""
frappe.ui.form.on("Vehicle Cab Booking", {
	end_date(frm) {
        if (frm.doc.start_date && frm.doc.end_date)
        {
            const sdate = new Date(frm.doc.start_date)
            let minutes = sdate.getMinutes();
            let roundedMinutes = Math.round(minutes / 30) / 30;
            sdate.setMinutes(roundedMinutes);
            sdate.setSeconds(0);

            const edate = new Date(frm.doc.end_date)
            let eminutes = edate.getMinutes();
            let eroundedMinutes = Math.round(eminutes / 30) * 30;
            edate.setMinutes(eroundedMinutes);
            edate.setSeconds(0);
            frappe.call({
                    method : "local_app.local_app.doctype.vehicle_cab_booking.vehicle_cab_booking.add_minutes",
                    args : {sdate : sdate,edate : edate},
                    callback : function(r)
                    {
                        frm.doc.start_date = r.message[0]
                        frm.doc.end_date = r.message[1]
                        frm.refresh_fields('start_date','end_date')
                    }
                })
        }
        if(frm.doc.from_location && frm.doc.start_date && frm.doc.end_date)
        {
            frappe.call({
                method : "local_app.local_app.doctype.vehicle_cab_booking.vehicle_cab_booking.set_filters",
                args : {data : frm.doc},
                callback : function(r)
                {
                    if (r.message)
                    {
                        frm.set_query("vehicle_number", function() {
                            return {
                                filters :[ 
                                    ["location", "=", r.message[1]],
                                    ["custom_status" ,"=", "Available"],
                                    ["name", "not in", r.message[0]]
                                ]
                            };
                        });  
                    }
                    else
                    {
                        frm.set_query("vehicle_number", function() {
                            return {
                                filters :[ 
                                    ["location", "=", frm.doc.from_location],
                                    ["custom_status" ,"=", "Available"],
                                ]
                            };
                            
                        });
                    }                    
                }
            }) 
        }
	},
    start_date(frm) {
        if (frm.doc.start_date && frm.doc.end_date)
        {
            const sdate = new Date(frm.doc.start_date)
            let minutes = sdate.getMinutes();
            let roundedMinutes = Math.round(minutes / 30) * 30;
            sdate.setMinutes(roundedMinutes);
            sdate.setSeconds(0);

            const edate = new Date(frm.doc.end_date)
            let eminutes = edate.getMinutes();
            let eroundedMinutes = Math.round(eminutes / 30) * 30;
            edate.setMinutes(eroundedMinutes);
            edate.setSeconds(0);
            frappe.call({
                method : "local_app.local_app.doctype.vehicle_cab_booking.vehicle_cab_booking.add_minutes",
                args : {sdate : sdate,edate : edate},
                callback : function(r)
                {
                    frm.doc.start_date = r.message[0]
                    frm.doc.end_date = r.message[1]
                    frm.refresh_fields('start_date','end_date')
                }
            })
        }
        if(frm.doc.from_location && frm.doc.start_date && frm.doc.end_date)
        {
            frappe.call({
                method : "local_app.local_app.doctype.vehicle_cab_booking.vehicle_cab_booking.set_filters",
                args : {data : frm.doc},
                callback : function(r)
                {
                    if (r.message)
                    {
                        frm.set_query("vehicle_number", function() {
                            return {
                                filters :[ 
                                    ["location", "=", r.message[1]],
                                    ["custom_status" ,"=", "Available"],
                                    ["name" ,"not in ", r.message[0]],
                                ]
                            };
                        });  
                    }
                    else
                    {
                        frm.set_query("vehicle_number", function() {
                            return {
                                filters :[ 
                                    ["location", "=", frm.doc.from_location],
                                    ["custom_status" ,"=", "Available"],
                                ]
                            };
                            
                        });
                    }
                }
            }) 
        }

	},
   on_submit(frm){
        frappe.call({
            method : "local_app.local_app.doctype.vehicle_cab_booking.vehicle_cab_booking.status_update",
            args : {
                "doc" : frm.doc.name,
                // "sdate":sdate,
                // "edate" : edate
            },
            callback : function(r)
            {
                if (r.message)
                {
                    // console.log(r.message) 
                }
            }
        })
    }
});
