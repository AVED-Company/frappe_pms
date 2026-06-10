import frappe


def execute(filters=None):
    return get_columns(), get_data(filters or {})


def get_columns():
    return [
        {"label": "ID",           "fieldname": "name",            "fieldtype": "Data",  "width": 160},
        {"label": "Title",        "fieldname": "title",           "fieldtype": "Data",  "width": 260},
        {"label": "Type",         "fieldname": "type",            "fieldtype": "Data",  "width": 90},
        {"label": "Status",       "fieldname": "status",          "fieldtype": "Data",  "width": 110},
        {"label": "Assigned To",  "fieldname": "assigned_to",     "fieldtype": "Data",  "width": 140},
        {"label": "Start Date",   "fieldname": "start_date",      "fieldtype": "Date",  "width": 110},
        {"label": "Due Date",     "fieldname": "due_date",        "fieldtype": "Date",  "width": 110},
        {"label": "Est. Hours",   "fieldname": "estimated_hours", "fieldtype": "Float", "width": 100},
        {"label": "Actual Hours", "fieldname": "actual_hours",    "fieldtype": "Float", "width": 110},
    ]


def get_data(filters):
    rows = []
    proj_cond = "AND p.name = %(project)s" if filters.get("project") else ""
    stat_cond = "AND p.status = %(status)s"  if filters.get("status")  else ""

    projects = frappe.db.sql(
        f"SELECT name, project_name, status, project_manager, start_date, expected_end_date "
        f"FROM `tabPMS Project` p WHERE 1=1 {proj_cond} {stat_cond} ORDER BY name",
        filters, as_dict=True,
    )

    for proj in projects:
        rows.append({"name": proj.name, "title": proj.project_name,
                     "type": "Project", "status": proj.status,
                     "assigned_to": proj.project_manager,
                     "start_date": proj.start_date, "due_date": proj.expected_end_date,
                     "estimated_hours": 0, "actual_hours": 0, "indent": 0})

        for phase in frappe.db.sql(
            "SELECT name, phase_name, status, start_date, end_date FROM `tabPMS Phase` "
            "WHERE project=%s ORDER BY start_date", proj.name, as_dict=True
        ):
            rows.append({"name": phase.name, "title": f"  ↳ {phase.phase_name}",
                         "type": "Phase", "status": phase.status, "assigned_to": "",
                         "start_date": phase.start_date, "due_date": phase.end_date,
                         "estimated_hours": 0, "actual_hours": 0, "indent": 1})

            for ms in frappe.db.sql(
                "SELECT name, milestone_name, status, due_date FROM `tabPMS Milestone` "
                "WHERE project=%s AND phase=%s ORDER BY due_date",
                (proj.name, phase.name), as_dict=True
            ):
                rows.append({"name": ms.name, "title": f"    ↳ {ms.milestone_name}",
                             "type": "Milestone", "status": ms.status, "assigned_to": "",
                             "start_date": None, "due_date": ms.due_date,
                             "estimated_hours": 0, "actual_hours": 0, "indent": 2})

                for t in frappe.db.sql(
                    "SELECT name, task_name, status, assigned_to, start_date, due_date, "
                    "estimated_hours, actual_hours FROM `tabPMS Task` "
                    "WHERE project=%s AND milestone=%s ORDER BY due_date",
                    (proj.name, ms.name), as_dict=True
                ):
                    rows.append({"name": t.name, "title": f"      ↳ {t.task_name}",
                                 "type": "Task", "status": t.status,
                                 "assigned_to": t.assigned_to,
                                 "start_date": t.start_date, "due_date": t.due_date,
                                 "estimated_hours": t.estimated_hours or 0,
                                 "actual_hours": t.actual_hours or 0, "indent": 3})

        # Tasks not under any milestone
        for t in frappe.db.sql(
            "SELECT name, task_name, status, assigned_to, start_date, due_date, "
            "estimated_hours, actual_hours FROM `tabPMS Task` "
            "WHERE project=%s AND (milestone IS NULL OR milestone='') ORDER BY due_date",
            proj.name, as_dict=True
        ):
            rows.append({"name": t.name, "title": f"  ↳ {t.task_name}",
                         "type": "Task", "status": t.status, "assigned_to": t.assigned_to,
                         "start_date": t.start_date, "due_date": t.due_date,
                         "estimated_hours": t.estimated_hours or 0,
                         "actual_hours": t.actual_hours or 0, "indent": 1})

    return rows
