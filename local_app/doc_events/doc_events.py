
import frappe
from datetime import datetime,timedelta,time

from frappe.utils import today

@frappe.whitelist()
def set_status_asset(self,method):
    self.status = "In Use"
    # frappe.errprint(self.status)
    self.save()


@frappe.whitelist()
def update_asset_maintenance(self,method):
    if self.status == "Completed":
        asset_main = frappe.get_doc("Asset Maintenance Request",self.custom_asset_maintenance_request)
        # asset_main.expected_completion_date = self.completed_on
        # working_days = (self.completed_on - asset_main.request_date).days
        time_diff_h = 0
        time_diff_m = 0
        if(asset_main.request_date == self.completed_on):
            time_diff1 = datetime.now() - self.creation
            time_diff_h += (time_diff1.seconds) //3600
            time_diff_m += (time_diff1.seconds // 60) %60
            # print(self.creation, "1111" , datetime.now())
        else:
            # creation = time(self.creation).replace(microsecond=0)
            
            # print(creation,"----------------------")

            # print(time_diff,type(time_diff))
            req_date = asset_main.request_date
            while(req_date <= self.completed_on):
                # print(req_date, self.completed_on)
                office_start_time = datetime.combine(req_date,time(9,30,00))
                office_close_time = datetime.combine(req_date,time(18,30,00))
                if req_date == asset_main.request_date:
                    # print(office_close_time)
                    # creation = datetime.time(self.creation).replace(microsecond=0)
                    # print(office_close_time , datetime.strftime(self.creation,"%Y-%m-%d %H:%M:%S"))
                    time_diff1 = (office_close_time - self.creation)

                    time_diff_h += (time_diff1.seconds) //3600
                    time_diff_m += (time_diff1.seconds // 60) %60
                elif req_date == self.completed_on:
                    time_diff2 = datetime.now() - office_start_time
                    time_diff_h += (time_diff2.seconds) //3600
                    time_diff_m += (time_diff2.seconds // 60) %60
                else:
                    
                    time_diff3 = office_close_time - office_start_time
                    time_diff_h += (time_diff3.seconds) //3600
                    time_diff_m += (time_diff3.seconds // 60) %60
                req_date += timedelta(days=1)
            #  diff = BusinessHours(start_time, end_time, worktiming=[9, 18], weekends=[6, 7], holidayfile=None)
            # time_diff = datetime.now() - self.creation
        # time_diff = timedelta(days = 0)
        # print(time_diff)
        time_diff = float(str(time_diff_h) + "." + str(time_diff_m))
        # frappe.throw("{0}".format(str(time_diff) + "." + str(time_diff_m)))
        # hours = time_diff.seconds //3600
        # mins = (time_diff.seconds // 60) % 60
        # total = float(str(hours)+ '.' + str(mins))
        asset_main.resolution_time = time_diff
        asset_main.expected_completion_date = self.completed_on
        asset_main.status = "In Review"
        asset_main.save()
        # frappe.throw("{0}".format(time_diff))



@frappe.whitelist()
def create_asset_movement(doct,email_list):
    task = frappe.get_doc("Task",doct)
    amr = frappe.get_doc("Asset Maintenance Request",task.custom_asset_maintenance_request)
    asset_movement = frappe.new_doc("Asset Movement")
    asset_movement.purpose = "Issue"
    row = asset_movement.append("assets")
    row.asset = task.custom_asset_name
    row.from_employee = amr.requested_by
    row.to_employee = frappe.db.get_value("Employee",{"user_id" :email_list},"name")
    row.source_location = frappe.db.get_value("Asset",task.custom_asset_name,"location")
    # print(row.as_dict())
    asset_movement.save()
    asset_movement.submit()
    amr.status = "In Progress"
    amr.expected_completion_date = task.exp_end_date
    amr.save()
    task.status = "Asset Collected"
    task.custom_asset_collection = asset_movement.name
    task.save()
    # frappe.throw("1234")
    # frappe.throw("hello")

@frappe.whitelist()
def create_asset_return(doct):
    task = frappe.get_doc("Task",doct)
    amr = frappe.get_doc("Asset Maintenance Request",task.custom_asset_maintenance_request)
    task.status = "Ask for Return"
    # task.custom_asset_return = asset_movement.name
    task.save()
    amr.status = "In Review"
    amr.save()


@frappe.whitelist()
def asset_repaired(doct):
    task = frappe.get_doc("Task",doct)
    # amr = frappe.get_doc("Asset Maintenance Request",task.custom_asset_maintenance_request)
    task.status = "Pending Review"
    task.save()
    # amr.status = "In Review"
    # amr.save()


@frappe.whitelist()
def create_asset_return_movement(doct):
    task = frappe.get_doc("Task",doct)
    amr = frappe.get_doc("Asset Maintenance Request",task.custom_asset_maintenance_request)
    asset_movement = frappe.new_doc("Asset Movement")
    asset_movement.purpose = "Issue"
    row = asset_movement.append("assets")
    row.asset = task.custom_asset_name
    user = frappe.db.get_value("ToDo",{"reference_name" :task.name},"allocated_to")
    row.from_employee = frappe.db.get_value("Employee",{"user_id" :user},"name")
    row.to_employee = amr.requested_by
    row.source_location = frappe.db.get_value("Asset",task.custom_asset_name,"location")
    # print(row.as_dict())
    asset_movement.save()
    asset_movement.submit()
    task.completed_on = today()
    task.status = "Completed"
    task.save()
    amr.status = "Completed"
    amr.save()

@frappe.whitelist()
def create_notification_log(doct,email_list):
    task = frappe.get_doc("Task",doct)
    amr = frappe.get_doc("Asset Maintenance Request",task.custom_asset_maintenance_request)
    notification = frappe.new_doc("Notification Log")
    notification.subject = "{0} asset is repaired".format(task.custom_asset_name)
    # print(frappe.session)
    notification.email_content = "Hello {1}, <br>Your {0} has been repaired. Please check and collect it from {2}.".format(task.custom_asset_name,amr.requested_by,email_list)
    notification.from_user = frappe.session.user
    notification.document_type = "Task"
    notification.document_name = task.name
    notification.type = "Alert"
    notification.for_user = frappe.db.get_value("Employee",amr.requested_by,"user_id")
    print(notification.as_dict())
    # frappe.throw("1234")
    notification.save()
    frappe.db.commit()



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
def update_last_rate(item_code,supplier,conversion_rate,company,currency):
    if not supplier:
        frappe.throw("Please enter Supplier Name")
    last_purchase_rate = frappe.db.get_value("Item",item_code,"last_purchase_rate")
    pur_rate = last_purchase_rate / float(conversion_rate)
    if frappe.db.get_value("Company",company,"default_currency") == currency:
        pur_rate = last_purchase_rate
    pur_order = frappe.db.sql(""" select poi.item_code,poi.base_net_amount,poi.amount,po.name from `tabPurchase Order` as po,
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
        return last_purchase_rate,pur_rate
    return last_purchase_rate,pur_rate