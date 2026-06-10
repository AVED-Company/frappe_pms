import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now


class PMSPaymentRequest(Document):

    def validate(self):
        self.total_amount = sum(row.amount or 0 for row in self.items)

    # ── Workflow actions (called from JS via frm.call) ───────────

    @frappe.whitelist()
    def submit_to_manager(self):
        self._require("Draft")
        self.status = "Submitted"
        self.submitted_by = frappe.session.user
        self.submitted_on = now()
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Submitted by {frappe.session.user}")
        frappe.msgprint(_("Request submitted to manager for review."))

    @frappe.whitelist()
    def approve_dept(self):
        self._require("Submitted")
        self.status = "Department Review"
        self.dept_approved_by = frappe.session.user
        self.dept_approved_on = now()
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Approved by Department Manager: {frappe.session.user}")
        frappe.msgprint(_("Approved by Department Manager — forwarded to Finance."))

    @frappe.whitelist()
    def approve_finance(self):
        self._require("Department Review")
        self.status = "Finance Review"
        self.fin_approved_by = frappe.session.user
        self.fin_approved_on = now()
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Verified by Finance: {frappe.session.user}")
        frappe.msgprint(_("Verified by Finance Manager — awaiting final approval."))

    @frappe.whitelist()
    def final_approve(self):
        self._require("Finance Review")
        self.status = "Approved"
        self.final_approved_by = frappe.session.user
        self.final_approved_on = now()
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Finally approved by {frappe.session.user}")
        frappe.msgprint(_("Request approved."))

    @frappe.whitelist()
    def mark_paid(self):
        self._require("Approved")
        self.status = "Paid"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Marked as Paid by {frappe.session.user}")
        frappe.msgprint(_("Request marked as Paid."))

    @frappe.whitelist()
    def cancel_request(self):
        if self.status == "Paid":
            frappe.throw(_("Cannot cancel a Paid request."))
        self.status = "Cancelled"
        self.save(ignore_permissions=True)
        self.add_comment("Workflow", f"Cancelled by {frappe.session.user}")
        frappe.msgprint(_("Request cancelled."))

    def _require(self, expected):
        if self.status != expected:
            frappe.throw(_(
                f"Action requires status \'{expected}\'. Current: \'{self.status}\'"
            ))
