// Copyright (c) 2024, Gokul and contributors
// For license information, please see license.txt

frappe.ui.form.on("Asset Maintenance Request", {
    refresh(frm) {
        // console.log(frappe.user_roles)
        // console.log(frappe.user_roles.includes("Maintenance Team Supervisor"))
        if (!frm.is_new() && frappe.user_roles.includes("Maintenance Team Supervisor")) {
            // console.log("Test")
            frm.add_custom_button(__('Create Maintenance Task'), function () {
                frappe.call({
                    method: "local_app.local_app.doctype.asset_maintenance_request.asset_maintenance_request.create_task",
                    args: {
                        "asset_name": frm.doc.name
                    },
                    callback: function (r) {
                        console.log(r)
                    }
                });
            });
            if (frm.doc.status != "Open")
            {
                frm.remove_custom_button('Create Maintenance Task');
            }
        }
        frm.set_query("asset", function () {
            return {
                filters: [
                    ["status", "=", "In Use"]
                ]
            };
        });
        if(frm.doc.status == "In Progress")
        {
            frm.add_custom_button(("Asset Verified"),function()
            {
                frappe.call({
                    method : "local_app.local_app.doctype.asset_maintenance_request.asset_maintenance_request.create_asset_return",
                    args : {
                        "doct": frm.doc.name
                    },
                    callback : function(){
                        frappe.msgprint(__('Asset is verrified successfully.'));
                    }
                })
            })
            if (frm.doc.status == "Completed")
                {
                    frm.remove_custom_button('Asset Verified');
                    
                }
        }
    },
    validate(frm) {
        // if(!frm.is_new())
        // {
        //     frm.add_custom_button(("Create Maintenance Task"),function()
        //     {
        //         frappe.call({
        //             method : "local_app.local_app.doctype.asset_maintenance_request.asset_maintenance_request.create_task",
        //             args : {"asset_name" : frm.doc.name},
        //             callback : function(){}
        //         })
        //     })
        // }
        
    },
});
