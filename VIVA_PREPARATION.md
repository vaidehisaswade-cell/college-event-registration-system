# DBMS TAE-2 Viva Preparation
## Short questions and answers

**1. What is the aim of this project?**  
To manage college events, student records, and registrations using a database-connected application.

**2. What is DBMS?**  
A Database Management System is software used to create, store, organize, retrieve, and manage data.

**3. Which database have you used?**  
SQLite, a lightweight relational database that stores data in a local file.

**4. Why did you choose SQLite?**  
It is easy to set up, comes with Python, and does not need a separate database server for this small academic project.

**5. What is database connectivity?**  
It is the link between an application and a database that allows the application to send SQL queries and receive results.

**6. Which Python module connects to SQLite?**  
The built-in `sqlite3` module.

**7. What does CRUD stand for?**  
Create, Read, Update, and Delete.

**8. What is a primary key?**  
A column or set of columns that uniquely identifies each row in a table. For example, `event_id`.

**9. What is a foreign key?**  
A column that refers to a key in another table. Here, `registrations.student_id` refers to `students.student_id`.

**10. Why are there three tables?**  
Events, students, and registrations represent different entities. Separating them reduces repeated data and makes relationships clearer.

**11. What is a many-to-many relationship in this project?**  
A student can register for many events, and an event can have many students. The registrations table links them.

**12. Why is `UNIQUE(student_id, event_id)` used?**  
To prevent the same student from registering for the same event more than once.

**13. What is normalization?**  
Organizing data into related tables to reduce unnecessary duplication and update anomalies.

**14. What is SQL?**  
Structured Query Language, used to define, query, and manipulate relational databases.

**15. Give an INSERT example.**  
`INSERT INTO events (event_name, category, event_date, venue, capacity) VALUES (?, ?, ?, ?, ?);`

**16. Give an UPDATE example.**  
`UPDATE events SET venue = ? WHERE event_id = ?;`

**17. Give a DELETE example.**  
`DELETE FROM registrations WHERE registration_id = ?;`

**18. Give a SELECT example.**  
`SELECT * FROM events;`

**19. Why use parameterized queries?**  
They safely pass values separately from SQL text and help reduce SQL injection risk.

**20. What is a JOIN?**  
A JOIN combines related rows from multiple tables. The registration report joins registrations, students, and events.

**21. What does `ON DELETE CASCADE` do?**  
It automatically removes child registration rows when their referenced student or event is deleted.

**22. What is Streamlit?**  
A Python framework for creating interactive web applications, including forms, tables, and buttons.

**23. How is event capacity handled?**  
The app counts active registrations and blocks a new active registration if the event has reached its capacity.

**24. What is a constraint?**  
A database rule that protects data validity, such as `NOT NULL`, `UNIQUE`, `CHECK`, or a foreign key.

**25. What are the limitations?**  
This is a local prototype without authentication or production-grade multi-user hosting.

## Demonstration sequence
1. Open the dashboard and explain the three tables.
2. Add an event and show it in the event list.
3. Update its venue and show the changed value.
4. Add a student.
5. Register that student for an event.
6. Show the registration and change its status.
7. Try a duplicate registration to demonstrate the constraint.
8. Delete the test registration.
9. Explain primary key, foreign key, JOIN, and parameterized queries.

## Team presentation split
- **Member 1:** Problem statement, objectives, schema, primary/foreign keys.
- **Member 2:** Python–SQLite connectivity, CRUD operations, SQL queries.
- **Member 3:** Interface, test cases, limitations, conclusion.
- Everyone should practice answering the viva questions above.
