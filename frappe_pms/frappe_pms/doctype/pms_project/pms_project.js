frappe.ui.form.on("PMS Project", {

    refresh(frm) {
        _set_status_color(frm);
        if (!frm.is_new()) {
            _add_quick_actions(frm);
            _render_progress_bar(frm);
        }
    },
});

function _set_status_color(frm) {
    const map = {
        Planning: "blue", Active: "green", "On Hold": "orange",
        Completed: "green", Cancelled: "red"
    };
    frm.page.set_indicator(frm.doc.status, map[frm.doc.status] || "blue");
}

function _add_quick_actions(frm) {
    const go = (dt, field) => () =>
        frappe.set_route("List", dt, { [field]: frm.doc.name });

    frm.add_custom_button(__("Tasks"),    go("PMS Task",        "project"), __("View"));
    frm.add_custom_button(__("Timesheets"), go("PMS Time Log",  "project"), __("View"));
    frm.add_custom_button(__("Milestones"), go("PMS Milestone", "project"), __("View"));
    frm.add_custom_button(__("Expenses"),   go("PMS Expense",   "project"), __("View"));
    frm.add_custom_button(__("Payment Requests"),
        go("PMS Payment Request", "project"), __("View"));
}

function _render_progress_bar(frm) {
    const pct = frm.doc.progress_pct || 0;
    const color = pct >= 80 ? "#27ae60" : pct >= 40 ? "#f39c12" : "#e74c3c";
    const html = `
        <div style="margin:6px 0">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="font-size:12px;color:#555">${__("Completion")}</span>
                <span style="font-size:12px;font-weight:600">${pct}%</span>
            </div>
            <div style="background:#e9ecef;border-radius:4px;height:10px;overflow:hidden">
                <div style="width:${pct}%;background:${color};height:100%;
                     border-radius:4px;transition:width .4s ease"></div>
            </div>
        </div>`;
    frm.set_intro(html, false);
}
