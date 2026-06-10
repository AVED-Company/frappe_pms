// Status colour map
const RFP_COLORS = {
    Draft: 'blue',
    Submitted: 'orange',
    'Department Review': 'orange',
    'Finance Review': 'purple',
    Approved: 'green',
    Paid: 'green',
    Cancelled: 'red',
};

frappe.ui.form.on('PMS Payment Request', {

    refresh(frm) {
        const s = frm.doc.status;
        frm.page.set_indicator(s, RFP_COLORS[s] || 'blue');
        _add_buttons(frm);
    },

    setup(frm) {
        frm.set_query('employee', () => ({ filters: { enabled: 1 } }));
    },
});

// ── Child table: live total recalculation ────────────────────────
frappe.ui.form.on('PMS Payment Request Item', {
    amount:       (frm) => _recalc(frm),
    items_remove: (frm) => _recalc(frm),
});

function _recalc(frm) {
    const total = (frm.doc.items || []).reduce((s, r) => s + (r.amount || 0), 0);
    frm.set_value('total_amount', total);
}

// ── Workflow buttons ─────────────────────────────────────────────
function _add_buttons(frm) {
    if (frm.is_new()) return;
    const s = frm.doc.status;

    if (s === 'Draft') {
        frm.add_custom_button(__('Submit to Manager'), () =>
            frappe.confirm(__('Submit this payment request to your manager?'), () =>
                _call(frm, 'submit_to_manager')
            ), __('Action'));
    }

    if (s === 'Submitted') {
        frm.add_custom_button(__('Approve — Dept. Manager'), () =>
            _call(frm, 'approve_dept'), __('Action'));
    }

    if (s === 'Department Review') {
        frm.add_custom_button(__('Approve — Finance'), () =>
            _call(frm, 'approve_finance'), __('Action'));
    }

    if (s === 'Finance Review') {
        frm.add_custom_button(__('Final Approve'), () =>
            _call(frm, 'final_approve'), __('Action'));
    }

    if (s === 'Approved') {
        frm.add_custom_button(__('Mark as Paid'), () =>
            _call(frm, 'mark_paid'), __('Action'));
    }

    if (!['Paid', 'Cancelled'].includes(s)) {
        frm.add_custom_button(__('Cancel Request'), () =>
            frappe.confirm(__('Cancel this request? This cannot be undone.'), () =>
                _call(frm, 'cancel_request')
            ), __('Action'));
    }
}

function _call(frm, method) {
    frm.call(method).then(() => frm.reload_doc());
}
