"""
Database initialization and management module
This file handles database creation, seeding, and utilities
"""

from app import app, db
from models import Todo, Event, Habit, Note
from datetime import datetime
import os

# Database file location
DATABASE_PATH = 'habitflow.db'

def init_database():
    """Initialize the database and create all tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print(f"✓ Database tables created successfully at '{DATABASE_PATH}'")
        
def reset_database():
    """Drop all tables and recreate them (WARNING: This deletes all data)"""
    with app.app_context():
        db.drop_all()
        print("✓ All tables dropped")
        db.create_all()
        print("✓ Database reset and recreated")

def seed_database():
    """Seed the database with sample data"""
    with app.app_context():
        # Check if data already exists
        if Todo.query.first() is not None:
            print("⚠ Database already contains data. Skipping seed.")
            return
        
        # Create sample todos
        todos = [
            Todo(text="Complete project documentation", priority="high"),
            Todo(text="Review pull requests", priority="medium"),
            Todo(text="Plan next sprint", priority="medium"),
        ]
        
        # Create sample events
        events = [
            Event(title="Team Meeting", date="2026-03-05", time="10:00", description="Weekly sync"),
            Event(title="Project Deadline", date="2026-03-15", time="23:59", description="Final submission"),
        ]
        
        # Create sample habits
        habits = [
            Habit(name="Morning Exercise", description="30 minutes workout", icon="fas fa-running"),
            Habit(name="Read", description="Read 30 pages", icon="fas fa-book"),
            Habit(name="Meditation", description="10 minutes meditation", icon="fas fa-spa"),
        ]
        
        # Create sample notes
        notes = [
            Note(title="Project Ideas", content="1. Feature A\n2. Feature B\n3. Feature C", color=1),
            Note(title="Important", content="Remember to backup data regularly", color=5),
        ]
        
        # Add all to session
        db.session.add_all(todos + events + habits + notes)
        db.session.commit()
        
        print("✓ Sample data seeded successfully")
        print(f"  - Added {len(todos)} todos")
        print(f"  - Added {len(events)} events")
        print(f"  - Added {len(habits)} habits")
        print(f"  - Added {len(notes)} notes")

def get_database_info():
    """Get information about the database"""
    with app.app_context():
        print("\n" + "="*50)
        print("DATABASE INFORMATION")
        print("="*50)
        
        if os.path.exists(DATABASE_PATH):
            size_mb = os.path.getsize(DATABASE_PATH) / (1024 * 1024)
            print(f"Database File: {DATABASE_PATH}")
            print(f"File Size: {size_mb:.2f} MB")
        else:
            print(f"Database File: {DATABASE_PATH} (not yet created)")
        
        print("\nTable Statistics:")
        print(f"  - Todos: {Todo.query.count()}")
        print(f"  - Events: {Event.query.count()}")
        print(f"  - Habits: {Habit.query.count()}")
        print(f"  - Notes: {Note.query.count()}")
        print("="*50 + "\n")

def export_data(filename='backup.json'):
    """Export all database data to JSON"""
    import json
    
    with app.app_context():
        data = {
            'todos': [todo.to_dict() for todo in Todo.query.all()],
            'events': [event.to_dict() for event in Event.query.all()],
            'habits': [habit.to_dict() for habit in Habit.query.all()],
            'notes': [note.to_dict() for note in Note.query.all()],
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Data exported to {filename}")

def clear_data(table_name=None):
    """Clear all data from a specific table or all tables"""
    with app.app_context():
        if table_name:
            if table_name.lower() == 'todos':
                Todo.query.delete()
            elif table_name.lower() == 'events':
                Event.query.delete()
            elif table_name.lower() == 'habits':
                Habit.query.delete()
            elif table_name.lower() == 'notes':
                Note.query.delete()
            db.session.commit()
            print(f"✓ Cleared all data from {table_name} table")
        else:
            Todo.query.delete()
            Event.query.delete()
            Habit.query.delete()
            Note.query.delete()
            db.session.commit()
            print("✓ Cleared all data from all tables")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'init':
            init_database()
        elif command == 'reset':
            if input("⚠ This will delete all data. Continue? (yes/no): ").lower() == 'yes':
                reset_database()
        elif command == 'seed':
            init_database()
            seed_database()
        elif command == 'info':
            get_database_info()
        elif command == 'export':
            filename = sys.argv[2] if len(sys.argv) > 2 else 'backup.json'
            export_data(filename)
        elif command == 'clear':
            table = sys.argv[2] if len(sys.argv) > 2 else None
            if input("⚠ This will delete data. Continue? (yes/no): ").lower() == 'yes':
                clear_data(table)
        else:
            print("Available commands:")
            print("  python database.py init    - Initialize database")
            print("  python database.py reset   - Reset database (deletes all data)")
            print("  python database.py seed    - Seed with sample data")
            print("  python database.py info    - Show database statistics")
            print("  python database.py export [filename] - Export data to JSON")
            print("  python database.py clear [table] - Clear data from table or all tables")
    else:
        print("Database Management System")
        print("Run: python database.py [command]")
        print("\nAvailable commands:")
        print("  init    - Initialize database")
        print("  reset   - Reset database (deletes all data)")
        print("  seed    - Seed with sample data")
        print("  info    - Show database statistics")
        print("  export  - Export data to JSON")
        print("  clear   - Clear data from tables")
