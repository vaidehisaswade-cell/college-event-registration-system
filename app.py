import sqlite3
from datetime import date
import pandas as pd
import streamlit as st

DB_PATH = "college_events.db"

st.set_page_config(page_title="College Event Registration System", page_icon="🎓", layout="wide")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            category TEXT NOT NULL,
            event_date TEXT NOT NULL,
            venue TEXT NOT NULL,
            capacity INTEGER NOT NULL CHECK(capacity > 0),
            description TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            year_of_study INTEGER NOT NULL CHECK(year_of_study BETWEEN 1 AND 4)
        );

        CREATE TABLE IF NOT EXISTS registrations (
            registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            registration_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Registered'
                CHECK(status IN ('Registered', 'Cancelled', 'Attended')),
            FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY(event_id) REFERENCES events(event_id) ON DELETE CASCADE,
            UNIQUE(student_id, event_id)
        );
        """)
        # Add sample records only when the database is empty.
        event_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        if event_count == 0:
            conn.executemany(
                """INSERT INTO events
                   (event_name, category, event_date, venue, capacity, description)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                [
                    ("TechNova Hackathon", "Technical", "2026-11-20", "Computer Lab 2", 80, "A team-based coding and innovation challenge."),
                    ("Rhythm Night", "Cultural", "2026-11-25", "College Auditorium", 150, "Music, dance and performances."),
                    ("Campus Clean-Up", "Social", "2026-12-02", "Main Campus", 60, "A student-led campus cleanliness drive.")
                ]
            )
        student_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        if student_count == 0:
            conn.executemany(
                """INSERT INTO students
                   (full_name, email, department, year_of_study)
                   VALUES (?, ?, ?, ?)""",
                [
                    ("Aarav Patil", "aarav@example.com", "AI & Data Science", 3),
                    ("Mira Deshmukh", "mira@example.com", "Computer Engineering", 2)
                ]
            )

def query_df(sql, params=()):
    with get_connection() as conn:
        return pd.read_sql_query(sql, conn, params=params)

def execute(sql, params=()):
    with get_connection() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid

def event_label(row):
    return f"{row['event_id']} — {row['event_name']} ({row['event_date']})"

init_db()

st.title("🎓 College Event Registration System")
st.caption("DBMS TAE-2 Mini-Project | Python + Streamlit + SQLite")
st.info("Demo data is included so you can explore the app immediately. Replace it with your own records during evaluation.")

events = query_df("""
    SELECT e.event_id, e.event_name, e.category, e.event_date, e.venue, e.capacity,
           COUNT(CASE WHEN r.status != 'Cancelled' THEN 1 END) AS registered_count
    FROM events e
    LEFT JOIN registrations r ON e.event_id = r.event_id
    GROUP BY e.event_id
""")
students = query_df("SELECT * FROM students")
registrations = query_df("""
    SELECT r.registration_id, s.full_name, s.email, e.event_name,
           r.registration_date, r.status, r.student_id, r.event_id
    FROM registrations r
    JOIN students s ON r.student_id = s.student_id
    JOIN events e ON r.event_id = e.event_id
    ORDER BY r.registration_id DESC
""")

m1, m2, m3 = st.columns(3)
m1.metric("Total Events", len(events))
m2.metric("Total Students", len(students))
m3.metric("Active Registrations", int((registrations["status"] == "Registered").sum()) if not registrations.empty else 0)

tab_dashboard, tab_events, tab_students, tab_reg = st.tabs(
    ["🏠 Dashboard", "📅 Manage Events", "👩‍🎓 Manage Students", "📝 Registrations"]
)

with tab_dashboard:
    st.subheader("Upcoming Events")
    if events.empty:
        st.write("No events yet. Add an event in Manage Events.")
    else:
        display = events.copy()
        display["Seats Left"] = (display["capacity"] - display["registered_count"]).clip(lower=0)
        display = display.rename(columns={
            "event_name": "Event", "category": "Category", "event_date": "Date",
            "venue": "Venue", "capacity": "Capacity", "registered_count": "Registrations"
        })
        st.dataframe(display[["Event", "Category", "Date", "Venue", "Capacity", "Registrations", "Seats Left"]],
                     use_container_width=True, hide_index=True)
    st.subheader("Database design")
    st.markdown("""
    - **events** stores event details.
    - **students** stores student details.
    - **registrations** connects students to events using foreign keys.
    - A unique constraint on `(student_id, event_id)` prevents the same student registering for the same event twice.
    """)

with tab_events:
    st.subheader("Create an event")
    with st.form("create_event", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Event name *")
        category = c2.selectbox("Category *", ["Technical", "Cultural", "Sports", "Workshop", "Social", "Other"])
        event_date = c1.date_input("Event date *", value=date.today())
        venue = c2.text_input("Venue *")
        capacity = c1.number_input("Capacity *", min_value=1, max_value=100000, value=50, step=1)
        description = c2.text_area("Description")
        submitted = st.form_submit_button("Add event")
        if submitted:
            if not name.strip() or not venue.strip():
                st.error("Event name and venue are required.")
            else:
                execute("""INSERT INTO events(event_name, category, event_date, venue, capacity, description)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        (name.strip(), category, event_date.isoformat(), venue.strip(), int(capacity), description.strip()))
                st.success("Event added successfully.")
                st.rerun()

    st.divider()
    st.subheader("View, update or delete events")
    events_all = query_df("SELECT * FROM events ORDER BY event_date")
    if events_all.empty:
        st.write("No events available.")
    else:
        st.dataframe(events_all, use_container_width=True, hide_index=True)
        chosen_event_id = st.selectbox("Select event to manage", events_all["event_id"].tolist(),
                                       format_func=lambda x: f"{x} — {events_all.loc[events_all.event_id == x, 'event_name'].iloc[0]}",
                                       key="manage_event_id")
        chosen = events_all[events_all["event_id"] == chosen_event_id].iloc[0]
        with st.form("update_event"):
            u1, u2 = st.columns(2)
            new_name = u1.text_input("Event name", value=chosen["event_name"])
            new_category = u2.selectbox("Category", ["Technical", "Cultural", "Sports", "Workshop", "Social", "Other"],
                                        index=["Technical", "Cultural", "Sports", "Workshop", "Social", "Other"].index(chosen["category"])
                                        if chosen["category"] in ["Technical", "Cultural", "Sports", "Workshop", "Social", "Other"] else 5)
            try:
                default_date = date.fromisoformat(chosen["event_date"])
            except ValueError:
                default_date = date.today()
            new_date = u1.date_input("Event date", value=default_date)
            new_venue = u2.text_input("Venue", value=chosen["venue"])
            new_capacity = u1.number_input("Capacity", min_value=1, max_value=100000, value=int(chosen["capacity"]))
            new_description = u2.text_area("Description", value=chosen["description"] or "")
            update_event = st.form_submit_button("Update event")
            if update_event:
                if not new_name.strip() or not new_venue.strip():
                    st.error("Event name and venue are required.")
                else:
                    execute("""UPDATE events SET event_name=?, category=?, event_date=?, venue=?, capacity=?, description=?
                               WHERE event_id=?""",
                            (new_name.strip(), new_category, new_date.isoformat(), new_venue.strip(),
                             int(new_capacity), new_description.strip(), int(chosen_event_id)))
                    st.success("Event updated.")
                    st.rerun()
        if st.button("Delete selected event", type="secondary"):
            execute("DELETE FROM events WHERE event_id=?", (int(chosen_event_id),))
            st.warning("Event deleted. Its registrations were also deleted.")
            st.rerun()

with tab_students:
    st.subheader("Add a student")
    with st.form("create_student", clear_on_submit=True):
        s1, s2 = st.columns(2)
        full_name = s1.text_input("Full name *")
        email = s2.text_input("Email *")
        department = s1.selectbox("Department", ["AI & Data Science", "Computer Engineering", "Information Technology", "Electronics", "Mechanical", "Other"])
        year = s2.selectbox("Year of study", [1, 2, 3, 4], index=2)
        add_student = st.form_submit_button("Add student")
        if add_student:
            if not full_name.strip() or not email.strip() or "@" not in email:
                st.error("Enter a name and a valid-looking email address.")
            else:
                try:
                    execute("INSERT INTO students(full_name, email, department, year_of_study) VALUES (?, ?, ?, ?)",
                            (full_name.strip(), email.strip().lower(), department, int(year)))
                    st.success("Student added.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("That email is already in the student table. Use a unique email.")

    st.divider()
    st.subheader("View, update or delete students")
    students_all = query_df("SELECT * FROM students ORDER BY full_name")
    if students_all.empty:
        st.write("No students available.")
    else:
        st.dataframe(students_all, use_container_width=True, hide_index=True)
        chosen_student_id = st.selectbox("Select student to manage", students_all["student_id"].tolist(),
                                         format_func=lambda x: f"{x} — {students_all.loc[students_all.student_id == x, 'full_name'].iloc[0]}",
                                         key="manage_student_id")
        chosen_s = students_all[students_all["student_id"] == chosen_student_id].iloc[0]
        with st.form("update_student"):
            edit_name = st.text_input("Full name", value=chosen_s["full_name"])
            edit_email = st.text_input("Email", value=chosen_s["email"])
            edit_department = st.text_input("Department", value=chosen_s["department"])
            edit_year = st.selectbox("Year", [1, 2, 3, 4], index=int(chosen_s["year_of_study"]) - 1)
            update_student = st.form_submit_button("Update student")
            if update_student:
                if not edit_name.strip() or not edit_email.strip() or "@" not in edit_email:
                    st.error("Enter a name and a valid-looking email address.")
                else:
                    try:
                        execute("UPDATE students SET full_name=?, email=?, department=?, year_of_study=? WHERE student_id=?",
                                (edit_name.strip(), edit_email.strip().lower(), edit_department.strip(), int(edit_year), int(chosen_student_id)))
                        st.success("Student updated.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("That email belongs to another student.")
        if st.button("Delete selected student", type="secondary"):
            execute("DELETE FROM students WHERE student_id=?", (int(chosen_student_id),))
            st.warning("Student deleted. Their registrations were also deleted.")
            st.rerun()

with tab_reg:
    st.subheader("Register a student for an event")
    current_students = query_df("SELECT student_id, full_name, email FROM students ORDER BY full_name")
    current_events = query_df("SELECT event_id, event_name, event_date, capacity FROM events ORDER BY event_date")
    current_regs = query_df("""
        SELECT r.student_id, r.event_id, r.status
        FROM registrations r
    """)
    if current_students.empty or current_events.empty:
        st.warning("Add at least one student and one event before registering.")
    else:
        with st.form("create_registration", clear_on_submit=True):
            selected_student = st.selectbox("Student", current_students["student_id"].tolist(),
                                            format_func=lambda x: f"{current_students.loc[current_students.student_id == x, 'full_name'].iloc[0]} — {current_students.loc[current_students.student_id == x, 'email'].iloc[0]}")
            selected_event = st.selectbox("Event", current_events["event_id"].tolist(),
                                          format_func=lambda x: f"{current_events.loc[current_events.event_id == x, 'event_name'].iloc[0]} — {current_events.loc[current_events.event_id == x, 'event_date'].iloc[0]}")
            reg_status = st.selectbox("Status", ["Registered", "Cancelled", "Attended"])
            create_reg = st.form_submit_button("Save registration")
            if create_reg:
                try:
                    event_row = current_events[current_events["event_id"] == selected_event].iloc[0]
                    active_count = query_df("SELECT COUNT(*) AS n FROM registrations WHERE event_id=? AND status='Registered'", (int(selected_event),)).iloc[0]["n"]
                    if reg_status == "Registered" and active_count >= int(event_row["capacity"]):
                        st.error("This event is full.")
                    else:
                        execute("""INSERT INTO registrations(student_id, event_id, registration_date, status)
                                   VALUES (?, ?, ?, ?)""",
                                (int(selected_student), int(selected_event), date.today().isoformat(), reg_status))
                        st.success("Registration saved.")
                        st.rerun()
                except sqlite3.IntegrityError:
                    st.error("This student already has a registration record for this event. Update the existing record instead.")

    st.divider()
    st.subheader("View, update or delete registrations")
    regs_all = query_df("""
        SELECT r.registration_id, r.student_id, s.full_name, e.event_name,
               r.event_id, r.registration_date, r.status
        FROM registrations r
        JOIN students s ON r.student_id=s.student_id
        JOIN events e ON r.event_id=e.event_id
        ORDER BY r.registration_id DESC
    """)
    if regs_all.empty:
        st.write("No registrations yet.")
    else:
        st.dataframe(regs_all[["registration_id", "full_name", "event_name", "registration_date", "status"]],
                     use_container_width=True, hide_index=True)
        selected_reg = st.selectbox("Select registration", regs_all["registration_id"].tolist(),
                                    format_func=lambda x: f"#{x} — {regs_all.loc[regs_all.registration_id == x, 'full_name'].iloc[0]} / {regs_all.loc[regs_all.registration_id == x, 'event_name'].iloc[0]}")
        reg_row = regs_all[regs_all["registration_id"] == selected_reg].iloc[0]
        new_status = st.selectbox("Change status", ["Registered", "Cancelled", "Attended"],
                                  index=["Registered", "Cancelled", "Attended"].index(reg_row["status"]))
        if st.button("Update registration status"):
            execute("UPDATE registrations SET status=? WHERE registration_id=?", (new_status, int(selected_reg)))
            st.success("Registration status updated.")
            st.rerun()
        if st.button("Delete selected registration", type="secondary"):
            execute("DELETE FROM registrations WHERE registration_id=?", (int(selected_reg),))
            st.warning("Registration deleted.")
            st.rerun()

st.divider()
st.caption("Academic demonstration project. Use fictional student data during testing.")
