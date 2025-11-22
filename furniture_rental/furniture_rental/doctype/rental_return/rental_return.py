# Copyright (c) 2025, anjusha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentalReturn(Document):
	pass

class RentalReturn(Document):
    def on_submit(self):
        # Update Contract Status to Returned
        if self.rental_contract:
            contract = frappe.get_doc("Rental Contract", self.rental_contract)
            contract.status = "Returned"
            contract.save()

        # Update Serial Numbers back to Warehouse
        for d in self.return_items:
            if d.serial_no:
                serial = frappe.get_doc("Serial No", d.serial_no)
                serial.current_location = "Warehouse"
                serial.current_rental_contract = ""
                
                # Mark condition
                serial.condition_status = d.returned_condition
                serial.save()

                # Auto-create Maintenance Request if damaged
                if d.returned_condition in ["Damaged", "Needs Repair"]:
                    create_maintenance_request(d)

        # Check if all deliveries returned → mark Contract as Completed
        self.check_if_contract_completed()

    def check_if_contract_completed(self):
        contract = frappe.get_doc("Rental Contract", self.rental_contract)
        deliveries = contract.rental_items
        returns = self.return_items

        if len(returns) == len(deliveries):
            contract.status = "Completed"
            contract.save()


def create_maintenance_request(item_row):
    mr = frappe.new_doc("Maintenance Request")
    mr.item = item_row.item
    mr.serial_no = item_row.serial_no
    mr.issue_description = "Returned damaged from rental"
    mr.insert()
