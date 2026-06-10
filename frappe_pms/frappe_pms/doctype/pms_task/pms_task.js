frappe.ui.form.on("PMS Task", {

    refresh(frm) {
        _status_color(frm);
        _deadline_warning(frm);
        if (!frm.is_new()) {
            frm.add_custom_button(__("Log Time"), () =>
                frappe.new_doc("PMS Time Log", {
                    project: frm.doc.project,
                    task: frm.doc.name,
                    logged_by: frappe.session.user,
                    date: frappe.datetime.get_today(),
                })
            );
        }
    },
});

function _status_color(frm) {
    const map = {
        Open: "blue", "In Progress": "orange", Review: "purple",
        Completed: "green", Cancelled: "red"
    };
    frm.page.set_indicator(frm.doc.status, map[frm.doc.status] || "blue");
}

function _deadline_warning(frm) {
    if (!frm.doc.due_date) return;
    const today = frappe.datetime.get_today();
    const overdue = frm.doc.due_date < today
        && !["Completed", "Cancelled"].includes(frm.doc.status);
    if (overdue) {
        frm.dashboard.set_headline_alert(
            `<span style="color:red">⚠ Overdue — due ${frm.doc.due_date}</span>`
        );
    }
}
