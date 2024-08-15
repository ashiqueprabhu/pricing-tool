# Copyright (c) 2024, Ashique Prabhu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PriceEstimationTool(Document):
	def validate (self) :
		self.total_extra_cost = self.installation + self.training + self.packing + self.saber + self.freight_cost + self.customs_duty_cd + self.miscellaneous_costs_mc
	
		for item in self.items:
			item.vendor_total_price = item.quantity * item.vendor_list_price
			item.vendor_net_price = item.vendor_total_price - (item.vendor_total_price * item.discount__commission) / 100
			item.sub_total = item.vendor_net_price * self.conversion_rate

@frappe.whitelist()
def generate_quotation(docname):
	estimation_doc = frappe.get_doc('Price Estimation Tool', docname)
	quotation = frappe.new_doc('Quotation')
	quotation.customer = estimation_doc.customer
	quotation.taxes_and_charges = estimation_doc.taxes_and_charges

	quotation.set_taxes()

	for item in estimation_doc.items:
		unit_selling_price = find_unit_selling_price(item.sub_total,estimation_doc.markup_percentage,estimation_doc.total_extra_cost,item.quantity)

		quotation.append('items', {
			'item_code': item.item_code,
			'item_name': item.item_name,
			'qty': item.quantity,
			'rate': unit_selling_price
		})

	quotation.insert()
	frappe.db.commit()
	return quotation.name

@frappe.whitelist()
def find_unit_selling_price(sub_total,markup_percentage,total_extra_cost,quantity):
	markup_percentage_value = markup_percentage / 100
	x = 1 - markup_percentage_value
	y = sub_total / x
	z = y + total_extra_cost
	result = z / quantity
	return round(result)
