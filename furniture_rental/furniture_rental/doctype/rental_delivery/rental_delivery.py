# Copyright (c) 2025, anjusha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentalDelivery(Document):
	pass


class RentalDelivery(Document):
    def on_submit(self):
        # Update Contract Status
        if self.rental_contract:
            contract = frappe.get_doc("Rental Contract", self.rental_contract)
            contract.status = "Delivered"
            contract.save()

        # Update Serial Number Location
        for d in self.delivery_items:
            if d.serial_no:
                serial = frappe.get_doc("Serial No", d.serial_no)
                serial.current_location = "Customer"
                serial.current_rental_contract = self.rental_contract
                serial.save()
