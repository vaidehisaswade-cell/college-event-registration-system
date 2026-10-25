## Live Demo
[Open College Event Registration System](https://college-event-registration-system.streamlit.app/)

## GitHub Repository
[View Source Code](https://github.com/vaidehisaswade-cell/college-event-registration-system)
# College Event Registration System (DBMS TAE-2)

## Tech stack
- Python
- Streamlit (web interface)
- SQLite (relational database)
- pandas (tables in the interface)

## Features
- Event CRUD: create, view, update, delete events
- Student CRUD: create, view, update, delete student records
- Registration CRUD: create, view, update status, delete registrations
- Three related tables with primary keys and foreign keys
- Unique student email and unique `(student_id, event_id)` registration pair
- Event capacity check and duplicate-registration prevention
- Dashboard with event, student and active-registration counts
- Sample data inserted automatically on first run

## Requirements
Install Python 3.10 or newer. Internet is needed only to install the packages.

## Run on Windows
1. Extract this ZIP into a folder.
2. Open that folder in File Explorer.
3. Click the address bar, type `cmd`, and press Enter.
4. Create a virtual environment (recommended):
   `py -m venv .venv`
5. Activate it:
   `.venv\Scripts\activate`
6. Install packages:
   `python -m pip install -r requirements.txt`
7. Start the app:
   `python -m streamlit run app.py`
8. A browser tab opens. If not, visit `http://localhost:8501`.

If `py` does not work, try `python` instead. If Streamlit is not recognized, use
`python -m streamlit run app.py`.

## Database file
The app creates `college_events.db` in the same folder on first run. It is a local SQLite database file. Do not delete it if you want to keep your records.

## Reset demo data
Close the app, delete `college_events.db`, then start the app again. The sample data will be recreated. This permanently removes records stored in that database file.

## CRUD mapping
- Create: Add event, Add student, Save registration
- Read: Dashboard tables and management tables
- Update: Update event, Update student, Update registration status
- Delete: Delete selected event/student/registration

## Important demo tip
Before evaluation, add one event and one student, register the student, change the registration status, and delete a test registration. Show the teacher that the rows update in the app and are stored in SQLite.
