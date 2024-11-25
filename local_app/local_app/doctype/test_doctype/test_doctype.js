// Copyright (c) 2024, Gokul and contributors
// For license information, please see license.txt

frappe.ui.form.on("Test Doctype", {
	refresh(frm) {                                                                                                     
        frm.add_custom_button(__('Update Changes'), function () {                                                   //frm.add_custom_button
            frappe.call({                                                                                           //frappe.call
                method: "local_app.local_app.doctype.test_doctype.test_doctype.update_changes",
                args: {
                    "name": frm.doc.name
                },
                callback: function (r) {
                    console.log(r)
                    frm.refresh_fields("posting_date")                                                                     //frm.refresh_field
                    // new frappe.ui.form.MultiSelectDialog({                                                                  //multiselect Dialog
                    //     doctype: "Doctype Checking",
                    //     target: frm,
                    //     columns :"person_name",
                    //     setters: {},
                    //     add_filters_group: 1,
                    //     action(selections) {
                    //         const plan_name = frm.doc.__newname;
                    //         frappe
                    //             .call({
                    //                 method: "call_multiselect_dialog",
                    //                 doc: frm.doc,
                    //                 args: selections,
                    //             })
                    //             .then((r) => {
                                    
                    //                 refresh_field("staffing_details");
                    //             });
            
                    //         cur_dialog.hide();
                    //     },
                    // });
                }
            });
        });
        // var d = new frappe.ui.Dialog({                                                                           //frappe.ui.dialog
		// 	title: __("Select Company"),
		// 	fields: [
		// 		{
		// 			fieldname: "company",
		// 			fieldtype: "Link",
		// 			label: __("Company"),
		// 			options: "Company",
		// 			get_query: function () {
		// 				return {
		// 				};
		// 			},
		// 			reqd: 1,
		// 		},
		// 	],
		// });
		// d.set_primary_action(__("Create"), function () {
		// 	d.hide();
		// 	var args = d.get_values();
		// 	frappe.call({
		// 		args: {
		// 			name: frm.doc.name,
		// 			voucher_type: frm.doc.voucher_type,
		// 			company: args.company,
		// 		},
		// 		method: "erpnext.accounts.doctype.journal_entry.journal_entry.make_inter_company_journal_entry",
		// 		callback: function (r) {
		// 			if (r.message) {
		// 				var doc = frappe.model.sync(r.message)[0];
		// 				frappe.set_route("Form", doc.doctype, doc.name);
		// 			}
		// 		},
		// 	});
		// });
		// d.show();     
        // cur_frm.set_value('to_date' , frm.doc.from_date)                                                           //set_value          //cur_frm
        if (frm.doc.person_name=="Supplier 1"){
        frm.toggle_display("company",false);                                //frm.toogle_display
        }
        // frm.refresh_field("to_date")                                                                     //frm.refresh_field

        // frm.set_df_property("purchase_inv", "read_only", 1);                                            //frm.set_df_property
        // frm.set_df_property("from_date", "hidden", 1);

	},
    validate(frm){

        // var v = cur_frm.add_child("child_table");                                                       //add child
        // v.child_name = "Child1"
        // v.roll_number = 12
        frappe.confirm(__("Are you sure you want Save the document?"), () => {                          //frappe.confirm
			frm.call("save_document").then((r) => {
				if (!r.exec) {
					frm.reload_doc();
				}
			});
		});
    }
});
