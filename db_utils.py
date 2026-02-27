"""
SQL Query Examples and Database Utilities
Use these queries directly with SQLite or through the Python ORM
"""

# ============ USEFUL SQL QUERIES ============

# GET STATISTICS
"""
SELECT 
    'todos' as table_name, COUNT(*) as count FROM todos
UNION ALL
SELECT 'events', COUNT(*) FROM events
UNION ALL
SELECT 'habits', COUNT(*) FROM habits
UNION ALL
SELECT 'notes', COUNT(*) FROM notes;
"""

# GET ALL INCOMPLETE TODOS SORTED BY PRIORITY
"""
SELECT id, text, priority, date FROM todos 
WHERE completed = 0 
ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END,
         date ASC;
"""

# GET UPCOMING EVENTS (NEXT 7 DAYS)
"""
SELECT id, title, date, time, description FROM events
WHERE date >= datetime('now') AND date <= datetime('now', '+7 days')
ORDER BY date, time;
"""

# GET HABITS WITH LONGEST STREAK
"""
SELECT id, name, description, streak, created_at FROM habits
ORDER BY streak DESC
LIMIT 10;
"""

# GET RECENT NOTES (LAST 30 DAYS)
"""
SELECT id, title, content, color, date FROM notes
WHERE created_at >= datetime('now', '-30 days')
ORDER BY created_at DESC;
"""

# GET COMPLETED TODOS THIS MONTH
"""
SELECT id, text, priority, completed_at FROM todos
WHERE completed = 1 
AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
ORDER BY created_at DESC;
"""

# ============ PYTHON ORM EXAMPLES ============

from app import app, db
from models import Todo, Event, Habit, Note
from datetime import datetime, timedelta
from sqlalchemy import func

def get_high_priority_todos():
    """Get all high priority incomplete todos"""
    with app.app_context():
        todos = Todo.query.filter_by(priority='high', completed=False).all()
        return [todo.to_dict() for todo in todos]

def get_upcoming_events(days=7):
    """Get events in the next N days"""
    with app.app_context():
        future_date = datetime.now() + timedelta(days=days)
        events = Event.query.filter(Event.date <= future_date.strftime('%Y-%m-%d')).all()
        return [event.to_dict() for event in events]

def get_top_habits(limit=5):
    """Get top habits by streak"""
    with app.app_context():
        habits = Habit.query.order_by(Habit.streak.desc()).limit(limit).all()
        return [habit.to_dict() for habit in habits]

def get_todos_by_priority():
    """Get todos count by priority"""
    with app.app_context():
        results = db.session.query(
            Todo.priority,
            func.count(Todo.id).label('count')
        ).group_by(Todo.priority).all()
        return [{'priority': r[0], 'count': r[1]} for r in results]

def get_database_statistics():
    """Get overall database statistics"""
    with app.app_context():
        stats = {
            'total_todos': Todo.query.count(),
            'completed_todos': Todo.query.filter_by(completed=True).count(),
            'pending_todos': Todo.query.filter_by(completed=False).count(),
            'total_events': Event.query.count(),
            'total_habits': Habit.query.count(),
            'total_notes': Note.query.count(),
            'todos_by_priority': get_todos_by_priority()
        }
        return stats

def bulk_create_todos(todos_list):
    """Create multiple todos at once"""
    with app.app_context():
        todos = [
            Todo(text=t['text'], priority=t.get('priority', 'medium'))
            for t in todos_list
        ]
        db.session.add_all(todos)
        db.session.commit()
        return len(todos)

def bulk_delete_completed_todos():
    """Delete all completed todos"""
    with app.app_context():
        count = Todo.query.filter_by(completed=True).delete()
        db.session.commit()
        return count

def search_notes(query):
    """Search notes by title or content"""
    with app.app_context():
        results = Note.query.filter(
            (Note.title.ilike(f'%{query}%')) | 
            (Note.content.ilike(f'%{query}%'))
        ).all()
        return [note.to_dict() for note in results]

def search_todos(query):
    """Search todos by text"""
    with app.app_context():
        results = Todo.query.filter(Todo.text.ilike(f'%{query}%')).all()
        return [todo.to_dict() for todo in results]

# ============ COMMON PATTERNS ============

"""
Pattern 1: Pagination
"""
def get_todos_paginated(page=1, per_page=10):
    with app.app_context():
        paginated = Todo.query.paginate(page=page, per_page=per_page)
        return {
            'data': [t.to_dict() for t in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages
        }

"""
Pattern 2: Filtering and Sorting
"""
def get_filtered_events(date=None, sort_by='time'):
    with app.app_context():
        query = Event.query
        if date:
            query = query.filter_by(date=date)
        if sort_by == 'time':
            query = query.order_by(Event.time)
        elif sort_by == 'date':
            query = query.order_by(Event.date)
        return [e.to_dict() for e in query.all()]

"""
Pattern 3: Transactions
"""
def transfer_habit_notes(habit_id, new_description):
    try:
        with app.app_context():
            habit = Habit.query.get(habit_id)
            if habit:
                habit.description = new_description
                db.session.commit()
                return True
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

"""
Pattern 4: Relationships & Joins
Future: Add relationships between tables for cascading operations
Example: If you link Habits to Notes, you can fetch all notes for a habit
"""

if __name__ == '__main__':
    print("Database Utilities Module")
    print("\nImport this module to use the query functions:")
    print("from db_utils import *")
    print("\nAvailable functions:")
    print("- get_high_priority_todos()")
    print("- get_upcoming_events(days=7)")
    print("- get_top_habits(limit=5)")
    print("- get_todos_by_priority()")
    print("- get_database_statistics()")
    print("- bulk_create_todos(todos_list)")
    print("- bulk_delete_completed_todos()")
    print("- search_notes(query)")
    print("- search_todos(query)")
