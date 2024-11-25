// Copyright (c) 2024, Gokul and contributors
// For license information, please see license.txt

frappe.ui.form.on("Doctype Checking", {
	refresh(frm) {
        // frappe.throw("121345")
        frm.add_custom_button(__('Update Changes'), function () {
            frappe.call({
                method: "local_app.local_app.doctype.doctype_checking.doctype_checking.get_update",
                args: {
                    "name": frm.doc.name
                },
                callback: function (r) {
                    console.log(r)
                }
            });
        });
	},
});
