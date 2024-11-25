# Copyright (c) 2024, Gokul and contributors
# For license information, please see license.txt

import frappe
from frappe.auth import today
from frappe.core.doctype.communication.email import make
from frappe.model.document import Document
import frappe.permissions
import frappe.utils
import datetime


class DoctypeChecking(Document):
	pass
	# def onload(self):
	# # 	# frappe.throw("-------------------------")
	# 	if frappe.has_permission("Doctype Checking","write",throw=False):						#has_permission
	# 	# 	frappe.errprint(frappe.permissions.add_permission("Doctype Checking", "Employee",permlevel=0,ptype="write"))
	# 		frappe.permissions.add_permission("Doctype Checking", "Employee",permlevel=0,ptype="write")			#add permissions
	# 		frappe.msgprint("Permission is added")

@frappe.whitelist(allow_guest=1)
def get_update(name):
	# # self.save()
	if not frappe.has_permission("Doctype Checking","write",throw=False):											#has_permission
			frappe.errprint("1234")
			frappe.permissions.update_permission_property("Doctype Checking", "Employee",0,"write",1)			#add permissions
			frappe.msgprint("Permission is added")
	self = frappe.get_doc("Doctype Checking",name)
	# age = '40'
	
	# a = int('abc')
	# frappe.errprint(type("20"))
	try:
		# self.age = int('255.54')
		# self.age = frappe.utils.cint("24.589")								#frappe.utils.cint
		# frappe.errprint(self.age)
		a = int('abc')
	except Exception as e:
		frappe.log_error(e)	
		# frappe.throw(e)									#frappe.log_error
	# frappe.has_permission(self.test)message
	self.transport = frappe.has_permission("Doctype Checking","write",throw=False)						#has_permission
	self.user = frappe.session.user																		#frappe.session.user
	list1 = frappe.get_list("Doctype Checking",filters={"person_name": self.person_name},fields=["*"])			#get_list
	self.list12 = list1[0]['name']
	frappe.errprint(list1)
	self.test = frappe.db.exists("Doctype Checking",{"person_name": self.person_name})		#frappe.db.exists
	try:
		self.date = frappe.utils.getdate('20031212')													#frappe.utils.getdate
	except Exception:
		frappe.log_error(Exception)
		self.date = frappe.utils.getdate()
# 	attachments = frappe.attach_print("Doctype Checking",self.name,doc=self,print_format="Standard")		#attach_print

# 	file = frappe.get_doc("File",)
# 	send_email( self,"gokulsk.craftinteractive@gmail.com", "test subject", "Test message", attachments=None)
# frappe.attach_print(
# 					self.reference_doctype,
# 					self.reference_name,
# 					file_name=self.reference_name,
# 					print_format=self.print_format,
				# )
	
	# frappe.errprint(self.as_dict())
	# doc = frappe.get_cached_value("Doctype Checking", self.person_name, "test")
	# frappe.errprint(doc)
	# frappe.clear_cache(doctype="Doctype Checking")					#frappe.clear_cache
	# doc = frappe.get_cached_value("Doctype Checking", self.person_name, "test")
	# frappe.errprint(doc)
	self.save()
	frappe.reload_doc("Local App","Doctype Checking",self.name)				#frappe.reload_doc
	# # self.save()
	frappe.db.commit()														#frappe.db.commit
	frappe.rename_doc("Doctype Checking",self.name,"testns23e",merge=True)				#rename Doc comand

def send_email(self, sender, subject, message, attachments):
	make(
		subject=subject,
		content=message,
		recipients="gokulsng57760@gmail.com",
		sender=sender,
		attachments=attachments,
		send_email=True,
		doctype=self.doctype,
		name=self.name,
	)