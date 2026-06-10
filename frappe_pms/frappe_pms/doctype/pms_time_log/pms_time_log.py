import frappe
from frappe.model.document import Document


class PMSTimeLog(Document):
    def validate(self):
        if self.hours <= 0:
            frappe.throw("Hours must be greater than 0")

    def on_submit(self):
        self._update_task_hours()

    def on_cancel(self):
        self._update_task_hours()

    def _update_task_hours(self):
        if not self.task:
            return
        task = frappe.get_doc("PMS Task", self.task)
        task._recalc_actual_hours()
        task.db_update()
