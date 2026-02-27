# Database Setup Guide - HabitFlow

## ✅ Current Status

Your project **already has a SQL database configured** using:
- **Database**: SQLite (habitflow.db)
- **ORM**: Flask-SQLAlchemy (Python database library)
- **Framework**: Flask

## 📁 New Database Files Created

1. **database.py** - Database initialization and management
2. **db_utils.py** - Useful query functions and utilities
3. **db.bat** - Windows batch script for easy database commands
4. **DATABASE.md** - Complete database schema documentation

---

## 🚀 Quick Start

### 1. Initialize Database
```bash
# Option 1: Using batch file
db.bat init

# Option 2: Direct Python
python database.py init
```

### 2. Seed with Sample Data
```bash
db.bat seed
# or
python database.py seed
```

### 3. View Database Info
```bash
db.bat info
# Shows: table row counts, file size, and basic statistics
```

### 4. Start the Application
```bash
run.bat
# or
python app.py
```

---

## 📊 Database Structure

Your database has 4 tables:

| Table | Purpose | Records |
|-------|---------|---------|
| **todos** | Task management | Variable |
| **events** | Calendar events | Variable |
| **habits** | Habit tracking | Variable |
| **notes** | Note taking | Variable |

---

## 🔧 Common Tasks

### List All Database Commands
```bash
db.bat
```

### Back Up Your Data
```bash
db.bat export my_backup.json
```

### Clear All Data (Warning: Cannot undo)
```bash
db.bat clear
# or clear specific table:
db.bat clear todos
```

### Reset Database
```bash
db.bat reset
# Deletes all tables and recreates them
```

---

## 💻 Using Database in Python

### Get Database Statistics
```python
from db_utils import get_database_statistics
stats = get_database_statistics()
print(stats)
```

### Search Data
```python
from db_utils import search_todos, search_notes
todos = search_todos("exercise")
notes = search_notes("important")
```

### Get Filtered Data
```python
from db_utils import get_high_priority_todos, get_top_habits
urgent = get_high_priority_todos()
top_habits = get_top_habits(limit=5)
```

### Bulk Operations
```python
from db_utils import bulk_create_todos, bulk_delete_completed_todos
todos_data = [
    {'text': 'Task 1', 'priority': 'high'},
    {'text': 'Task 2', 'priority': 'medium'}
]
bulk_create_todos(todos_data)
deleted_count = bulk_delete_completed_todos()
```

---

## 🌐 API Endpoints

### Todos
```
GET    /api/todos              → Get all todos
POST   /api/todos              → Create todo
PUT    /api/todos/<id>         → Update todo
DELETE /api/todos/<id>         → Delete todo
```

### Events
```
GET    /api/events             → Get all events
POST   /api/events             → Create event
DELETE /api/events/<id>        → Delete event
```

### Habits
```
GET    /api/habits             → Get all habits
POST   /api/habits             → Create habit
PUT    /api/habits/<id>        → Update habit
POST   /api/habits/<id>/toggle → Toggle day completion
DELETE /api/habits/<id>        → Delete habit
```

### Notes
```
GET    /api/notes              → Get all notes
POST   /api/notes              → Create note
DELETE /api/notes/<id>         → Delete note
```

---

## 📝 Example API Requests

### Create a Todo
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Complete project\",\"priority\":\"high\"}"
```

### Get All Todos
```bash
curl http://localhost:5000/api/todos
```

### Create a Habit
```bash
curl -X POST http://localhost:5000/api/habits \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Morning Exercise\",\"description\":\"30 mins workout\"}"
```

### Create a Note
```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Project Ideas\",\"content\":\"Idea 1, Idea 2\",\"color\":1}"
```

---

## 🔍 View Database File

The database file `habitflow.db` is a SQLite database. You can open it with:

### SQLite Command Line
```bash
sqlite3 habitflow.db
sqlite> .tables
sqlite> SELECT COUNT(*) FROM todos;
sqlite> .quit
```

### SQLite Browser GUI
Download from: https://sqlitebrowser.org/

---

## ⚠️ Troubleshooting

### "Module 'Flask' not found"
```bash
pip install -r requirements.txt
```

### "database.db is locked"
```bash
db.bat reset
```

### Port 5000 Already in Use
Edit `app.py` and change:
```python
if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Change 5000 to 8000
```

---

## 📦 Dependencies

All dependencies are in `requirements.txt`:
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
python-dateutil==2.8.2
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🎯 Next Steps

1. ✅ Initialize database: `db.bat init`
2. ✅ Seed sample data: `db.bat seed`
3. ✅ Start app: `run.bat` or `python app.py`
4. ✅ Test API: Open http://localhost:5000
5. ✅ Check database: `db.bat info`

---

## 📚 Additional Resources

- See **DATABASE.md** for complete schema documentation
- Use **db_utils.py** for common database queries
- Check **app.py** for API endpoint implementations

---

## ✨ Features Included

✅ Full CRUD operations for Todo, Event, Habit, Note  
✅ SQLite database with automatic initialization  
✅ RESTful API endpoints  
✅ Database backup/export functionality  
✅ Sample data seeding  
✅ Database statistics and queries  
✅ Transaction support  
✅ CORS enabled for frontend access  

---

**Your database is ready to use!** 🎉
