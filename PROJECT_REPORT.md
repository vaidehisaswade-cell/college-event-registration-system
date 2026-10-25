# DBMS TAE-2 Mini-Project Report
## College Event Registration and Management System

**Course:** Database Management Systems (DBMS)  
**Activity:** TAE-2 Mini-Project with Database Connectivity  
**Team size:** 3 students  
**Technology:** Python, Streamlit, SQLite

> Replace the team-member placeholders, college name, guide name, screenshots, and actual test results before submitting. Do not claim tests or screenshots you have not completed.

## 1. Abstract
The College Event Registration and Management System is a database-driven application designed to help a college maintain event details, student information, and event registrations. It provides a simple interface to add, view, update, and delete records. SQLite stores the data in related tables, while Python connects the application to the database. The system uses primary keys, foreign keys, uniqueness constraints, and validation to maintain data integrity.

## 2. Problem statement
Colleges conduct technical, cultural, sports, and social events. Maintaining event details and student registrations manually can lead to duplicate entries, difficulty tracking capacity, and time-consuming record searches. This project provides a centralized and easy-to-use system for maintaining event and registration records.

## 3. Objectives
1. Design a relational database for events, students, and registrations.
2. Connect a Python application to an SQLite database.
3. Implement Create, Read, Update, and Delete (CRUD) operations.
4. Use primary keys and foreign keys to maintain relationships.
5. Prevent duplicate student emails and duplicate registrations for the same event.
6. Display useful event and registration information through a dashboard.

## 4. Scope
The prototype supports local demonstration on one computer. It is suitable for academic demonstration and is not intended as a production system with authentication, online payments, or multi-user hosting.

## 5. Software and hardware requirements
- Operating system: Windows, Linux, or macOS
- Python 3.10 or newer
- Streamlit and pandas Python packages
- SQLite (included with Python)
- Browser such as Chrome or Edge
- Laptop/desktop with basic memory and storage

## 6. System architecture
User → Streamlit interface → Python application logic → SQLite database → results displayed in the interface.

## 7. Database design

### Table: events
| Field | Type | Constraint / purpose |
|---|---|---|
| event_id | INTEGER | Primary key, auto-increment |
| event_name | TEXT | Required event name |
| category | TEXT | Event category |
| event_date | TEXT | Date in YYYY-MM-DD format |
| venue | TEXT | Required venue |
| capacity | INTEGER | Must be greater than zero |
| description | TEXT | Optional description |

### Table: students
| Field | Type | Constraint / purpose |
|---|---|---|
| student_id | INTEGER | Primary key, auto-increment |
| full_name | TEXT | Required name |
| email | TEXT | Required, unique |
| department | TEXT | Department |
| year_of_study | INTEGER | Must be 1–4 |

### Table: registrations
| Field | Type | Constraint / purpose |
|---|---|---|
| registration_id | INTEGER | Primary key, auto-increment |
| student_id | INTEGER | Foreign key to students |
| event_id | INTEGER | Foreign key to events |
| registration_date | TEXT | Date registration was recorded |
| status | TEXT | Registered, Cancelled, or Attended |

### Relationships
- One student can register for many events.
- One event can have many student registrations.
- `registrations` resolves the many-to-many relationship between students and events.
- `UNIQUE(student_id, event_id)` prevents the same student from creating more than one registration record for the same event.

## 8. CRUD implementation
- **Create:** insert a new event, student, or registration.
- **Read:** display records in dashboard and management tables.
- **Update:** edit event details, student details, or registration status.
- **Delete:** remove a selected event, student, or registration.
- Foreign-key cascading removes registrations when their parent event or student is deleted.

## 9. Database connectivity
The application uses Python's built-in `sqlite3` module. It opens a connection to `college_events.db`, executes SQL statements with parameter placeholders, commits changes, and reads results for display. Parameterized queries reduce SQL injection risk. Foreign-key enforcement is enabled on each connection.

## 10. Testing plan
Run each test and record the actual result before submission.

| Test | Action | Expected result |
|---|---|---|
| T1 | Add a new event | Event appears in the event table |
| T2 | Update event venue | New venue is displayed |
| T3 | Delete a test event | Event is removed |
| T4 | Add a student | Student appears in the student table |
| T5 | Add a student using an existing email | Duplicate is rejected |
| T6 | Register a student for an event | Registration appears in the table |
| T7 | Register the same student for the same event again | Duplicate is rejected |
| T8 | Change registration status | New status is displayed |
| T9 | Delete a registration | Registration disappears |
| T10 | Register after capacity is reached | App rejects a new active registration |

**Actual results:** Fill this section after running the tests. Add screenshots of the dashboard, event CRUD, student CRUD, and registration table.

## 11. Limitations
- Local SQLite database; no remote or simultaneous multi-user deployment is configured.
- No login or role-based access.
- Email validation is basic and does not send confirmation emails.
- Event capacity is checked by the application; a production version should use stronger transactional controls for concurrent registrations.

## 12. Future enhancements
- Student and administrator login
- QR-code attendance
- Email confirmations
- Search, filtering, and downloadable reports
- MySQL server for multi-user deployment
- Event feedback and attendance analytics

## 13. Conclusion
The project demonstrates a database-connected application with related tables, primary and foreign keys, constraints, and CRUD operations. It shows how a user interface can interact with a relational database to maintain college event and student registration data.

## 14. Team contribution
- **Member 1 — Database design:** ER model, tables, keys, constraints, and SQL queries.
- **Member 2 — Application development:** Python–SQLite connectivity and CRUD logic.
- **Member 3 — Interface, testing, and documentation:** Streamlit interface, test execution, screenshots, report, and presentation.

All members should understand the full project and be ready to explain the database design and CRUD flow.
