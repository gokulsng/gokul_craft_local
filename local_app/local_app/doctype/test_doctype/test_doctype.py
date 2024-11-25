# Copyright (c) 2024, Gokul and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import utils
import frappe.utils

class TestDoctype(Document):
	pass

	@frappe.whitelist()
	def call_multiselect_dialog(doc):
		return "10"
	def on_update(self):
		if not frappe.db.exists("Test Doctype",{"person_name":"Person1"}):
			frappe.errprint("11111")
			test = frappe.new_doc("Test Doctype")																				#frappe.new_doc
			test.person_name = "Person1"
			test.save()
		else:
			test = frappe.get_doc("Test Doctype",{"person_name":"Person1"})
			frappe.delete_doc("Test Doctype", test.name)																		#frappe.delete_doc
	@frappe.whitelist()
	def save_document(self):
		self.save()

# def onload(self):																					#onload_function
# 	ser = frappe.get_single("Test Single")															#get_single
# 	ser.test_doc_name = frappe.utils.random_string(10)												#random_string
# 	ser.save()

# 	# frappe.errprint(type(frappe.utils.now_datetime()))
# 	# frappe.errprint(self.as_dict())
# 	# self.save()
	# frappe.msgprint(ser.test_doc_name)											#msgprint

@frappe.whitelist()
def scheduler_jobs():
	doc = frappe.get_doc("Test Doctype",{"name":"mflqiume00"})
	doc.random_name = frappe.utils.random_string(15)
	# frappe.db.sql("""update `tabTest Doctype` set random_name = '{0}' where name = '{1}'""".format(frappe.utils.random_string(15), doc.name))
	doc.save()
	# print(doc,"11111111111111111111111111111111111111111")
	# print(doc.as_dict())
	# return doc


@frappe.whitelist()
def update_changes(name):
	doc = frappe.get_doc("Test Doctype",name)
	# if frappe.get_hooks("doctype_js")['Task']:													#frappe.get_hooks
	# 	frappe.throw("The task hook is running on other app!!")										#frappe.throw
	# frappe.enqueue(method=frappe.get_hooks("doctype_js")['Task'],
	# 				queue="long",
	# 				is_async=True,
	# 				job_name="Test Enqueue",
	# 				doc=doc.name,
	# 			)
	# var = frappe.get_hooks("demo_transaction_doctypes")												#frappe.get_hooks
	# doc.hooks = var[0]
	# # frappe.db.sql("""update `tabTest Doctype` set hooks = '{0}' where name = '{1}'""".format(var[0], doc.name))			#frappe.db.sql()

	# doc.to_date = utils.add_days(doc.from_date,10)													#frappe.utils.add_days
	# frappe.db.sql("""update `tabTest Doctype` set to_date = '{0}' where name = '{1}'""".format(utils.add_days(doc.from_date,10), doc.name))

	msg = "Testing Send mail function with some message and tried to attach attachments!!"
	# attachments = frappe.attach_print(
	# 	"Sales Invoice",
	# 	"ACC-SINV-2024-00004",
	# 	file_name="ACC-SINV-2024-00004.pdf.crdownload",
	# 	print_format="Sales Invoice Format"
	# )
	attachments = [frappe.attach_print(doctype='Test Doctype', name=doc.name, print_letterhead=True)]   
	# # frappe.sendmail(recipients="gokulsng57760@gmail.com", subject="Send email function", message=msg, attachments=attachments)			#sendmail function 
	# attachments=[{
    #         "fname": f"ACC-SINV-2024-00004.pdf.crdownload",
    #         "fcontent": frappe.attach_print("Sales Invoice", "ACC-SINV-2024-00004", print_format="Standard"),
    #         "file_url": "/private/files/ACC-SINV-2024-00004.pdf.crdownload"
    #     }]



	frappe.enqueue(																											#enqueue
				queue="short",
				method=frappe.sendmail,																						#frappe.sendmail
				recipients="gokulsng57760@gmail.com",
				sender="gokulsk.craftinterractive@gmail.com",
				cc="",
				subject="Send email function",
				message=msg,
				now=True,
				reference_name=doc.name,
				attachments = attachments
				# attachments=[{"file_url": "/private/files/ACC-SINV-2024-00004.pdf.crdownload"}],
			)

	# companies = frappe.get_all("Company")															#get_All
	# # frappe.errprint(companies)
	# doc.company = companies[0]['name']

	# doc.purchase_inv = frappe.db.get_value("Purchase Invoice",{"supplier": doc.person_name },"name")					#get_value

	# frappe.db.set_value("Test Doctype", doc.name, "posting_date",frappe.utils.now_datetime())							#set_value and utils.datetime_now
																			#delete_doc
	doc.save()
	frappe.reload_doc("Local App","Test Doctype",doc.name)