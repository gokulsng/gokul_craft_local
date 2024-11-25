
import frappe
from datetime import datetime,timedelta,time

from frappe.utils import flt, today


# @frappe.whitelist()
# def update_last_rate(item_code,supplier):
#     last_purchase_rate = frappe.db.get_value("Item",item_code,"last_purchase_rate")
#     pur_order = frappe.get_all("Purchase Order",{"supplier":supplier,"item_code":item_code})
#     if pur_order:
#         # frappe.errprint(pur_order)
#         for order in pur_order:
#             order1 = frappe.get_doc("Purchase Order",order['name'])
#             # frappe.errprint(order1.as_dict())
#             for item in order1.items:
#                 # frappe.errprint(item.as_dict())
#                 itm = item
#                 if itm['item_code'] == item_code:
#                     last_purchase_rate = itm['amount']
#                 # frappe.errprint(item)
#     # print(last_purchase_rate)
#     return last_purchase_rate



@frappe.whitelist()
def update_last_rate(item_code,supplier,conversion_rate,company,currency,conversion_factor=1.0):
    if not supplier:
        frappe.throw("Please enter Supplier Name")
    last_purchase_rate = frappe.db.get_value("Item",item_code,"last_purchase_rate")
    pur_rate = last_purchase_rate * (flt(conversion_factor) or 1.0) / float(conversion_rate)
    if frappe.db.get_value("Company",company,"default_currency") == currency:
        pur_rate = last_purchase_rate
    pur_order = frappe.db.sql(""" select poi.item_code,poi.base_net_rate,poi.net_rate,po.name from `tabPurchase Order` as po,
            `tabPurchase Order Item` as poi where poi.parent = po.name and po.supplier = '{0}' and poi.item_name = '{1}' 
            order by po.name DESC""".format(supplier,item_code))
    if pur_order:
        last_purchase_rate = pur_order[0][1]
        # frappe.errprint(frappe.db.get_value("Company",company,"default_currency") == currency)
        if frappe.db.get_value("Company",company,"default_currency") == currency:
            pur_rate = last_purchase_rate
        else:
            pur_rate = pur_order[0][2]
        frappe.errprint(pur_rate)
        # frappe.errprint(item_last_purchase_rate( item_code,supplier,conversion_rate, company,currency, conversion_factor=1.0))
        return last_purchase_rate,pur_rate
    return last_purchase_rate,pur_rate

# @frappe.request_cache
# def item_last_purchase_rate(name, conversion_rate, item_code, conversion_factor=1.0):
# 	"""get last purchase rate for an item"""
#     frappe.throw("errere")

# 	conversion_rate = flt(conversion_rate) or 1.0

# 	last_purchase_details = get_last_purchase_details(item_code, name) # type: ignore
# 	if last_purchase_details:
# 		last_purchase_rate = (
# 			last_purchase_details["base_net_rate"] * (flt(conversion_factor) or 1.0)
# 		) / conversion_rate
# 		return last_purchase_rate
# 	else:
# 		item_last_purchase_rate = frappe.get_cached_value("Item", item_code, "last_purchase_rate")
# 		if item_last_purchase_rate:
# 			return item_last_purchase_rate