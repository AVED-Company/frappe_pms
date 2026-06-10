import frappe
from frappe.model.document import Document


class PMSProject(Document):

    def after_save(self):
        self._update_progress()

    def _update_progress(self):
        total = frappe.db.count("PMS Task", {"project": self.name})
        if not total:
            if self.progress_pct != 0:
                frappe.db.set_value("PMS Project", self.name, "progress_pct", 0)
            return
        done = frappe.db.count("PMS Task", {"project": self.name, "status": "Completed"})
        pct = round(done / total * 100, 1)
        if pct != self.progress_pct:
            frappe.db.set_value("PMS Project", self.name, "progress_pct", pct)
