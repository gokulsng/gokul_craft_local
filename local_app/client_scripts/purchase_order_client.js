

var item_code = ""
frappe.ui.form.on('Purchase Order Item', {
	item_code(frm, cdt, cdn) {
        if(!frm.doc.supplier)
        {
            frappe.throw("Please select supplier first")
        }
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
            method: "local_app.doc_events.purchase_order.update_last_rate",
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
					method: "local_app.doc_events.purchase_order.update_last_rate",
                    args:{
					    "item_code" : child.item_code,
                        "supplier" : frm.doc.supplier,
                        "conversion_rate" : conversion_rate,
                        "company" : frm.doc.company,
                        "currency" : frm.doc.currency,
                    },
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
                    method: "local_app.doc_events.purchase_order.update_last_rate",
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
        if(frm.doc.supplier && frm.doc.items[0].actual_qty>0)
        {
            frm.refresh_fields("conversion_rate")
            frm.doc.items.forEach(child => {
                frappe.call({
                    method: "local_app.doc_events.purchase_order.update_last_rate",
                    args:{
                        "item_code" : child.item_code,
                        "supplier" : frm.doc.supplier,
                        "conversion_rate" : frm.doc.conversion_rate,
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