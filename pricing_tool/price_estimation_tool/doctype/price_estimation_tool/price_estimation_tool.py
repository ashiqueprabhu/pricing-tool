# Copyright (c) 2024, Ashique Prabhu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PriceEstimationTool(Document):
	def on_update (self) :
		if self.quantity:
			self.vendor_total_price = self.quantity * self.vendor_list_price
			self.vendor_net_price = self.vendor_total_price - (self.vendor_total_price * self.discountcommission) / 100
			self.sub_total = self.vendor_net_price * self.conversion_rate
			self.total_extra_cost = self.installation + self.training + self.packing + self.saber + self.freight_cost + self.customs_duty_cd + self.miscellaneous_costs_mc
	# pass

@frappe.whitelist()
def generate_quotation(docname):
	estimation_doc = frappe.get_doc('Price Estimation Tool', docname)
	quotation = frappe.new_doc('Quotation')
	quotation.customer = estimation_doc.customer
	unit_selling_price = find_unit_selling_price(estimation_doc.sub_total, estimation_doc.markup_percentage, estimation_doc.total_extra_cost, estimation_doc.quantity)
	quotation.taxes_and_charges = estimation_doc.taxes_and_charges

	quotation.set_taxes()

	quotation.append('items', {
		'item_code': estimation_doc.item,
		'item_name': estimation_doc.item_name,
		'qty': estimation_doc.quantity,
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
