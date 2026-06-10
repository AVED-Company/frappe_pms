import frappe
from frappe.model.document import Document


class PMSProject(Document):
    def before_save(self):
        self.budget_used = frappe.db.sql(
            "SELECT IFNULL(SUM(amount),0) FROM `tabPMS Expense` WHERE project=%s AND status='Approved'",
            self.name
        )[0][0]
        if self.status == "Completed" and not self.actual_end_date:
            self.actual_end_date = frappe.utils.today()
