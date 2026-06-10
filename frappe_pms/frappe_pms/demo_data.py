"""
Demo data loader.
Usage:  bench --site aved-pms.frappe.cloud execute frappe_pms.frappe_pms.demo_data.load
"""
import frappe
from frappe.utils import add_days, today


def load():
    frappe.set_user("Administrator")

    # ── Users ──────────────────────────────────────────────────────
    for u in [
        ("pm@example.com",   "Alice",  "Manager",   "PMS Manager"),
        ("dev1@example.com", "Bob",    "Developer", "PMS Member"),
        ("dev2@example.com", "Carol",  "Designer",  "PMS Member"),
    ]:
        if not frappe.db.exists("User", u[0]):
            frappe.get_doc({
                "doctype": "User", "email": u[0],
                "first_name": u[1], "last_name": u[2],
                "send_welcome_email": 0,
                "roles": [{"role": u[3]}],
            }).insert(ignore_permissions=True)
    frappe.db.commit()
    print("  users ok")

    # ── Project 1: Website Redesign ────────────────────────────────
    if not frappe.db.exists("PMS Project", {"project_name": "Website Redesign"}):
        p1 = frappe.get_doc({
            "doctype": "PMS Project",
            "project_name": "Website Redesign",
            "status": "Active",
            "project_manager": "pm@example.com",
            "start_date": add_days(today(), -30),
            "expected_end_date": add_days(today(), 60),
            "total_budget": 50000,
            "description": "Full redesign of company website with new branding.",
            "team_members": [
                {"user": "pm@example.com",   "role_in_project": "Project Manager", "allocation_pct": 50},
                {"user": "dev1@example.com", "role_in_project": "Developer",       "allocation_pct": 100},
                {"user": "dev2@example.com", "role_in_project": "Designer",        "allocation_pct": 80},
            ],
        }).insert(ignore_permissions=True)
        pn = p1.name

        ph1 = frappe.get_doc({"doctype":"PMS Phase","phase_name":"Discovery & Planning",
            "project":pn,"status":"Completed",
            "start_date":add_days(today(),-30),"end_date":add_days(today(),-15)}).insert(ignore_permissions=True)
        ph2 = frappe.get_doc({"doctype":"PMS Phase","phase_name":"Design",
            "project":pn,"status":"Active",
            "start_date":add_days(today(),-14),"end_date":add_days(today(),14)}).insert(ignore_permissions=True)
        ph3 = frappe.get_doc({"doctype":"PMS Phase","phase_name":"Development",
            "project":pn,"status":"Planning",
            "start_date":add_days(today(),15),"end_date":add_days(today(),55)}).insert(ignore_permissions=True)
        frappe.db.commit()

        ms1 = frappe.get_doc({"doctype":"PMS Milestone","milestone_name":"Requirements Sign-off",
            "project":pn,"phase":ph1.name,"status":"Achieved","due_date":add_days(today(),-15)}).insert(ignore_permissions=True)
        ms2 = frappe.get_doc({"doctype":"PMS Milestone","milestone_name":"Design Approval",
            "project":pn,"phase":ph2.name,"status":"Pending","due_date":add_days(today(),14)}).insert(ignore_permissions=True)
        ms3 = frappe.get_doc({"doctype":"PMS Milestone","milestone_name":"MVP Launch",
            "project":pn,"phase":ph3.name,"status":"Pending","due_date":add_days(today(),55)}).insert(ignore_permissions=True)
        frappe.db.commit()

        for tn, ph, ms, usr, st, sd, dd, est, act in [
            ("Stakeholder interviews",  ph1.name, ms1.name, "dev1@example.com", "Completed", -28,-20,  8, 10),
            ("Competitor analysis",     ph1.name, ms1.name, "dev2@example.com", "Completed", -25,-18,  6,  5),
            ("Wireframes",              ph2.name, ms2.name, "dev2@example.com", "In Progress",-14,  7, 20, 12),
            ("Visual design system",    ph2.name, ms2.name, "dev2@example.com", "Open",        -5, 14, 24,  0),
            ("Frontend development",    ph3.name, ms3.name, "dev1@example.com", "Open",        15, 50, 80,  0),
            ("CMS integration",         ph3.name, ms3.name, "dev1@example.com", "Open",        25, 50, 40,  0),
            ("UAT & QA",                ph3.name, ms3.name, "pm@example.com",   "Open",        50, 55, 16,  0),
        ]:
            t = frappe.get_doc({
                "doctype":"PMS Task","task_name":tn,"project":pn,"phase":ph,"milestone":ms,
                "assigned_to":usr,"status":st,
                "start_date":add_days(today(),sd),"due_date":add_days(today(),dd),
                "estimated_hours":est,
            }).insert(ignore_permissions=True)
            if act:
                frappe.get_doc({
                    "doctype":"PMS Time Log","project":pn,"task":t.name,
                    "logged_by":"dev1@example.com","date":add_days(today(),-10),
                    "hours":act,"status":"Approved","description":"Work logged",
                }).insert(ignore_permissions=True)

        frappe.get_doc({
            "doctype":"PMS Expense","project":pn,
            "expense_date":add_days(today(),-20),"category":"Software License",
            "amount":1200,"status":"Approved","approved_by":"pm@example.com",
            "description":"Figma annual subscription",
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"  project 1 created: {pn}")

    # ── Project 2: ERP Implementation ─────────────────────────────
    if not frappe.db.exists("PMS Project", {"project_name": "ERP Implementation"}):
        p2 = frappe.get_doc({
            "doctype": "PMS Project",
            "project_name": "ERP Implementation",
            "status": "Planning",
            "project_manager": "pm@example.com",
            "start_date": add_days(today(), 5),
            "expected_end_date": add_days(today(), 120),
            "total_budget": 150000,
            "description": "Full ERPNext implementation for the organization.",
            "team_members": [
                {"user": "pm@example.com",   "role_in_project": "Project Manager",  "allocation_pct": 100},
                {"user": "dev1@example.com", "role_in_project": "Technical Lead",   "allocation_pct": 100},
            ],
        }).insert(ignore_permissions=True)
        pn = p2.name

        ph_a = frappe.get_doc({"doctype":"PMS Phase","phase_name":"Analysis",
            "project":pn,"status":"Planning",
            "start_date":add_days(today(),5),"end_date":add_days(today(),30)}).insert(ignore_permissions=True)
        frappe.get_doc({"doctype":"PMS Phase","phase_name":"Configuration",
            "project":pn,"status":"Planning",
            "start_date":add_days(today(),31),"end_date":add_days(today(),80)}).insert(ignore_permissions=True)
        frappe.db.commit()

        ms_a = frappe.get_doc({"doctype":"PMS Milestone","milestone_name":"Business Process Documentation",
            "project":pn,"phase":ph_a.name,"status":"Pending","due_date":add_days(today(),30)}).insert(ignore_permissions=True)

        for tn, est in [("As-Is process mapping",12),("Gap analysis",10),("System requirements spec",20)]:
            frappe.get_doc({
                "doctype":"PMS Task","task_name":tn,"project":pn,
                "phase":ph_a.name,"milestone":ms_a.name,
                "assigned_to":"dev1@example.com","status":"Open",
                "start_date":add_days(today(),5),"due_date":add_days(today(),30),"estimated_hours":est,
            }).insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"  project 2 created: {pn}")

    print("\nDemo data loaded successfully!")
