frappe.query_reports["Project Hierarchy"] = {
    filters: [
        {fieldname: "project", label: __("Project"), fieldtype: "Link", options: "PMS Project"},
        {fieldname: "status",  label: __("Status"),  fieldtype: "Select",
         options: "\nPlanning\nActive\nOn Hold\nCompleted\nCancelled"},
    ],
    formatter(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        const typeColors  = {Project: "#5e64ff", Phase: "#2490ef", Milestone: "#f08700", Task: "#4bc0c8"};
        const statusClass = {Active: "green", Completed: "blue", "On Hold": "orange",
                             Cancelled: "red", Planning: "grey", Open: "grey",
                             "In Progress": "yellow", Review: "purple", Achieved: "blue", Pending: "grey"};
        if (column.fieldname === "type" && typeColors[data.type])
            return `<span style="color:${typeColors[data.type]};font-weight:600">${data.type}</span>`;
        if (column.fieldname === "status" && data.status)
            return `<span class="indicator-pill ${statusClass[data.status] || 'grey'}">${data.status}</span>`;
        return value;
    },
};
