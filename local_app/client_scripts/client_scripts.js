

frappe.ui.form.on("Task", {
    refresh(frm){
        // console.log("123")
        // if (frm.doc.exp_end_date)
        // {
            
        // }
        if(frm.doc.status == "Open")
        {
            frm.add_custom_button(__('Asset Collected'), function()
            {
                var assignees = frm.get_docinfo().assignments;
                let email_list = assignees.length > 0 ? assignees[0]["owner"] : null;
                frappe.call({
                    method: "local_app.doc_events.doc_events.create_asset_movement",
                    args: {
                        "doct": frm.doc.name,
                        "email_list": email_list
                    },
                    callback: function(r){
                        frappe.msgprint(__('Asset is given to Maintenance Team successfully'));
                        // window.location.reload();
                    }
                });
            });
            // console.log(frm.doc.status)
            if (frm.doc.status == "Asset Collected")
            {
                // console.log(frm.status)
                frm.remove_custom_button('Asset Collected');

            }
        }
    // },
    // refresh(frm){
        // console.log("123")
        if(frm.doc.status == "Asset Collected")
        {
            frm.add_custom_button(__('Asset Repaired'), function()
            {
                frappe.call({
                    method: "local_app.doc_events.doc_events.asset_repaired",
                    args: {
                        "doct": frm.doc.name
                    },
                    callback: function(r){
                    }
                });
            });
            // console.log(frm.doc.status)
            if (frm.doc.status == "Pending Review")
            {
                // console.log(frm.status)
                frm.remove_custom_button('Asset Repaired');
                
            }
        }
        if(frm.doc.status == "Pending Review")
        {
            frm.add_custom_button(__('Request for Return'), function()
            {
                frappe.call({
                    method: "local_app.doc_events.doc_events.create_asset_return",
                    args: {
                        "doct": frm.doc.name
                    },
                    callback: function(r){
                    }
                });
            });
            if (frm.doc.status == "Repair Completed")
            {
                frm.remove_custom_button('Request for Return');
                
            }
        }
        if(frm.doc.status == "Repair Completed")
        {
            frm.add_custom_button(__('Create Asset Movement'), function()
            {
                frappe.call({
                    method: "local_app.doc_events.doc_events.create_asset_return_movement",
                    args: {
                        "doct": frm.doc.name
                    },
                    callback: function(r){
                    }
                });
            });
            if (frm.doc.status == "Completed")
            {
                frm.remove_custom_button('Create Asset Movement');
                
            }
        }
    },
    validate(frm){
        if (frm.doc.status == "Ask for Return" && frappe.user.has_role("Maintenance Team Supervisor"))
        {
            // console.log(frm.doc.status)
            var assignees = frm.get_docinfo().assignments;
            let email_list = assignees.length > 0 ? assignees[0]["owner"] : null;
            frappe.call({
                method: "local_app.doc_events.doc_events.create_notification_log",
                args: {
                    "doct": frm.doc.name,
                    "email_list": email_list
                },
                callback: function(r){
                    frappe.msgprint(__('Notification sent successfully'));
                    // window.location.reload();
                }
            });
        }
        else if (frm.doc.status == "Ask for Return")
        {
            frappe.throw("Only Maintenance Team Supervisor can update the status 'Ask for Return' ")
        }
    }
})
var item_code = ""
frappe.ui.form.on('Purchase Order Item', {
	item_code(frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        var supplier = frm.doc.supplier
        var company = frm.doc.company
        var currency = frm.doc.currency
        if(frm.doc.conversion_rate)
        {
            var conversion_rate = frm.doc.conversion_rate
        }
        else
        {
            var conversion_rate = 1
        }
		frappe.call({
            method: "local_app.doc_events.purchase_order_script.update_last_rate",
            args:{
                "item_code" : row.item_code,
                "supplier" : supplier,
                "conversion_rate" : conversion_rate,
                "company" : company,
                "currency" : currency
            },
            callback: function(r){
                    row.custom_last_purchase_rate_company_currency = r.message[0]
                    row.last_purchase_rate = r.message[1]
                    row.rate = r.message[1]
                    
            }
        })
	},
})
frappe.ui.form.on('Purchase Order',{
    refresh(frm) {
        var new_name = ""
        frappe.db.get_value("Company",frm.doc.company,'default_currency').then((r) => {
        new_name = "Last Purchase Rate ("+ r.message.default_currency + ")";
        frm.fields_dict['items'].grid.update_docfield_property('custom_last_purchase_rate_company_currency', 'label', new_name);
        })
        frm.add_custom_button(
			__("Update Rate as per Last Purchase"),
			function () {
                frm.doc.items.forEach(child => {
                if(frm.doc.conversion_rate)
                {
                    var conversion_rate = frm.doc.conversion_rate
                }
                else
                {
                    var conversion_rate = 1.0
                }
				frappe.call({
					method: "local_app.doc_events.purchase_order_script.update_last_rate",
                    args:{
					    "item_code" : child.item_code,
                        "supplier" : frm.doc.supplier,
                        "conversion_rate" : conversion_rate,
                        "company" : frm.doc.company,
                        "currency" : frm.doc.currency},
					callback: function (r, rt) {
						frm.dirty();
                        child.custom_last_purchase_rate_company_currency = r.message[0]
                        child.last_purchase_rate = r.message[1]
                        child.rate = r.message[1]
					},
				});
            })
			},
			__("Tools")
		);
    },
    supplier(frm) {
        // console.log(frm.doc.items)
        if(frm.doc.items[0].actual_qty>0)
        {
            frm.doc.items.forEach(child => {
                if(frm.doc.conversion_rate)
                {
                    var conversion_rate = frm.doc.conversion_rate
                }
                else
                {
                    var conversion_rate = 1.0
                }
                frappe.call({
                    method: "local_app.doc_events.purchase_order_script.update_last_rate",
                    args:{
                        "item_code" : child.item_code,
                        "supplier" : frm.doc.supplier,
                        "conversion_rate" : conversion_rate,
                        "company" : frm.doc.company,
                        "currency" : frm.doc.currency
                    },
                    callback: function(r){
                        child.custom_last_purchase_rate_company_currency = r.message[0]
                        child.last_purchase_rate = r.message[1]
                        child.rate = r.message[1]
                    }
                })
            });
        }
	},
    currency(frm) {
        // console.log(frm.doc.items)
        var conversion_rate = frm.doc.conversion_rate
        if(frm.doc.supplier && frm.doc.items[0].actual_qty>0)
        {
            frm.doc.items.forEach(child => {
                frappe.call({
                    method: "local_app.doc_events.purchase_order_script.update_last_rate",
                    args:{
                        "item_code" : child.item_code,
                        "supplier" : frm.doc.supplier,
                        "conversion_rate" : conversion_rate,
                        "company" : frm.doc.company,
                        "currency" : frm.doc.currency
                    },
                    callback: function(r){
                        child.custom_last_purchase_rate_company_currency = r.message[0]
                        child.last_purchase_rate = r.message[1]
                        child.rate = r.message[1]
                    }
                })
            });
        }
	},
})