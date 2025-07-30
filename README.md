
# Help Desk System

This project is a simple Help Desk system built with Flask. It simulates a technical support system for a small organization, allowing users to create and manage service tickets.

## Database Schema

The database schema is defined in `database/schema.sql` and consists of three tables:

*   **users**: Stores user information (employees and technicians).
*   **tickets**: Stores service call information.
*   **ticket_comments**: Stores comments on tickets.

### `users` table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('employee', 'technician'))
);
```

### `tickets` table

```sql
CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'New' CHECK(status IN ('New', 'In Progress', 'Resolved', 'Closed')),
    urgency TEXT NOT NULL CHECK(urgency IN ('Low', 'Medium', 'High')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### `ticket_comments` table

```sql
CREATE TABLE ticket_comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## How to Run

1.  **Install dependencies:**

    ```bash
    pip install Flask Werkzeug
    ```

2.  **Initialize the database:**

    ```bash
    flask --app app initdb
    ```

3.  **Run the application:**

    ```bash
    flask --app app run
    ```

## Reports

The following functions can be used to generate reports:

*   `get_open_tickets_by_technician(technician_id)`
*   `calculate_average_resolution_time()`
*   `get_tickets_by_urgency_report()`
