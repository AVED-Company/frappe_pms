import frappe
from frappe.model.document import Document


class PMSTask(Document):
    def before_save(self):
        if self.status == "Completed" and not self.completed_date:
            self.completed_date = frappe.utils.today()
        elif self.status != "Completed":
            self.completed_date = None

    def before_save(self):
        self._sync_status_dates()
        self._recalc_actual_hours()

    def _sync_status_dates(self):
        if self.status == "Completed" and not self.completed_date:
            self.completed_date = frappe.utils.today()
        elif self.status != "Completed":
            self.completed_date = None

    def _recalc_actual_hours(self):
        result = frappe.db.sql(
            "SELECT IFNULL(SUM(hours),0) FROM `tabPMS Time Log` WHERE task=%s AND status IN ('Submitted','Approved')",
            self.name
        )
        self.actual_hours = result[0][0] if result else 0
