# Database Schema Documentation

## Overview
This project uses **SQLite** database with **Flask-SQLAlchemy** ORM. The database file is stored as `habitflow.db`.

## Database Configuration
```python
Database Type: SQLite
File Location: habitflow.db
Framework: Flask-SQLAlchemy
ORM: SQLAlchemy
```

---

## Tables and Schema

### 1. **todos** Table
Stores to-do items/tasks

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| text | String(255) | NOT NULL | Task description |
| priority | String(20) | DEFAULT 'medium' | Priority level: low, medium, high |
| completed | Boolean | DEFAULT False | Task completion status |
| date | DateTime | DEFAULT utcnow() | Due date |
| created_at | DateTime | DEFAULT utcnow() | Creation timestamp |

**Sample Query:**
```sql
SELECT * FROM todos WHERE priority='high' AND completed=0;
```

---

### 2. **events** Table
Stores calendar events

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| title | String(255) | NOT NULL | Event title |
| date | String(10) | NOT NULL | Event date (YYYY-MM-DD format) |
| time | String(5) | DEFAULT '00:00' | Event time (HH:MM format) |
| description | Text | DEFAULT '' | Event details |
| created_at | DateTime | DEFAULT utcnow() | Creation timestamp |

**Sample Query:**
```sql
SELECT * FROM events WHERE date='2026-03-15' ORDER BY time;
```

---

### 3. **habits** Table
Stores habit tracking information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| name | String(255) | NOT NULL | Habit name |
| description | String(255) | DEFAULT '' | Habit description |
| icon | String(50) | DEFAULT 'fas fa-star' | FontAwesome icon class |
| streak | Integer | DEFAULT 0 | Current streak count |
| completed_days | String(255) | DEFAULT '' | CSV format of completed days |
| created_at | DateTime | DEFAULT utcnow() | Creation timestamp |

**Sample Query:**
```sql
SELECT * FROM habits WHERE streak > 7 ORDER BY streak DESC;
```

---

### 4. **notes** Table
Stores user notes

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| title | String(255) | NOT NULL | Note title |
| content | Text | NOT NULL | Note content |
| color | Integer | DEFAULT 1 | Color code (1-5) |
| date | String(10) | DEFAULT '' | Note date (MM/DD/YYYY format) |
| created_at | DateTime | DEFAULT utcnow() | Creation timestamp |

**Sample Query:**
```sql
SELECT * FROM notes WHERE color=5 ORDER BY created_at DESC;
```

---

## Database Management

### Initialize Database
```bash
python database.py init
```

### Seed with Sample Data
```bash
python database.py seed
```

### View Database Statistics
```bash
python database.py info
```

### Export Data to JSON
```bash
python database.py export backup.json
```

### Clear All Data
```bash
python database.py clear
```

### Reset Database (Delete All & Recreate)
```bash
python database.py reset
```

---

## Database Operations in Python

### Create Records
```python
from app import app, db
from models import Todo, Event, Habit, Note

with app.app_context():
    # Create a todo
    todo = Todo(text="My task", priority="high")
    db.session.add(todo)
    db.session.commit()
```

### Read Records
```python
with app.app_context():
    # Get all todos
    todos = Todo.query.all()
    
    # Get specific todo
    todo = Todo.query.get(1)
    
    # Filter todos
    high_priority = Todo.query.filter_by(priority='high').all()
```

### Update Records
```python
with app.app_context():
    todo = Todo.query.get(1)
    todo.text = "Updated task"
    todo.completed = True
    db.session.commit()
```

### Delete Records
```python
with app.app_context():
    todo = Todo.query.get(1)
    db.session.delete(todo)
    db.session.commit()
```

---

## API Endpoints

### Todos
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/<id>` - Update a todo
- `DELETE /api/todos/<id>` - Delete a todo

### Events
- `GET /api/events` - Get all events
- `POST /api/events` - Create a new event
- `DELETE /api/events/<id>` - Delete an event

### Habits
- `GET /api/habits` - Get all habits
- `POST /api/habits` - Create a new habit
- `PUT /api/habits/<id>` - Update a habit
- `POST /api/habits/<id>/toggle` - Toggle habit day completion
- `DELETE /api/habits/<id>` - Delete a habit

### Notes
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `DELETE /api/notes/<id>` - Delete a note

---

## Troubleshooting

### Database Locked Error
If you get "database is locked" error:
```bash
python database.py reset
```

### Missing Database File
If the database doesn't exist:
```bash
python database.py init
python database.py seed
```

### View Raw SQL Data
Using SQLite CLI:
```bash
sqlite3 habitflow.db
sqlite> .tables
sqlite> SELECT * FROM todos;
```

---

## Dependencies
- Flask==2.3.3
- Flask-SQLAlchemy==3.0.5
- Flask-CORS==4.0.0
- python-dateutil==2.8.2

---

## Performance Tips
1. **Indexing**: Add indexes for frequently queried columns
2. **Pagination**: Implement pagination for large datasets
3. **Caching**: Use Flask caching for read-heavy operations
4. **Backups**: Regularly export data using `python database.py export`
