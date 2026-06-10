import frappe
from frappe.model.document import Document


class PMSExpense(Document):
    def validate(self):
        if self.amount <= 0:
            frappe.throw("Amount must be greater than 0")

    def on_update(self):
        if self.status == "Approved" and self.approved_by is None:
            self.approved_by = frappe.session.user
            self.db_update()
        self._refresh_project_budget()

    def _refresh_project_budget(self):
        if not self.project:
            return
        project = frappe.get_doc("PMS Project", self.project)
        project.before_save()
        project.db_update()
