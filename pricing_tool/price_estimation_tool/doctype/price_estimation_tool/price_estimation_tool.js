// Copyright (c) 2024, Ashique Prabhu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Price Estimation Tool', {
	currency: function (frm) {
		if (frm.doc.currency) {
			frappe.db.get_value('Currency Exchange', {from_currency: frm.doc.currency}, 'exchange_rate')
				.then(r => {
					if (r.message.exchange_rate) {
						frm.set_value('conversion_rate', r.message.exchange_rate)
					}
				})
		}
	},
	refresh: function (frm) {
		frm.add_custom_button(__('Generate Quotation'), function() {
			frappe.call({
				'method': 'pricing_tool.price_estimation_tool.doctype.price_estimation_tool.price_estimation_tool.generate_quotation',
				'args': {
					'docname' : frm.doc.name
				}, callback: function (r) {
					if (r.message) {
						frappe.show_alert ({
							message: __('Quotation {0} created', [r.message]),
							indicator: 'green'
						});
						frappe.set_route('Form', 'Quotation', r.message);
					}
				}
			});
		});
	}
});
