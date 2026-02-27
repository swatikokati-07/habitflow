"""
Database Schema Visualization and Analysis Tool
"""

from app import app, db
from models import Todo, Event, Habit, Note

def print_schema():
    """Print the complete database schema in a readable format"""
    
    print("\n" + "="*80)
    print("DATABASE SCHEMA - HabitFlow")
    print("="*80)
    
    with app.app_context():
        # Get all models
        models = [Todo, Event, Habit, Note]
        
        for model in models:
            print(f"\n📋 TABLE: {model.__tablename__.upper()}")
            print("-" * 80)
            
            # Print columns
            columns = model.__table__.columns
            print(f"{'Column':<20} {'Type':<20} {'Nullable':<12} {'Default':<20}")
            print("-" * 80)
            
            for column in columns:
                col_type = str(column.type)
                nullable = "✓ Yes" if column.nullable else "✗ No"
                default = str(column.default.arg) if column.default else "-"
                
                print(f"{column.name:<20} {col_type:<20} {nullable:<12} {default:<20}")
            
            # Print sample data
            count = model.query.count()
            print(f"\nRows in Table: {count}")
            
            if count > 0:
                print("Sample Data (first row):")
                sample = model.query.first()
                sample_dict = sample.to_dict()
                for key, value in sample_dict.items():
                    print(f"  • {key}: {value}")

def print_relationships():
    """Print model relationships (future enhancement)"""
    print("\n" + "="*80)
    print("MODEL RELATIONSHIPS")
    print("="*80)
    print("""
Currently, models are independent. Consider adding relationships:

Example Future Enhancement:
  - Habit can have many Notes
  - Todo can be linked to Events
  - User table to own multiple records

To implement:
  1. Add User table with id, email, password
  2. Add user_id foreign key to each table
  3. Define relationships in models.py
  4. Update database.py to handle migrations
""")

def print_statistics():
    """Print database statistics"""
    from datetime import datetime, timedelta
    
    print("\n" + "="*80)
    print("DATABASE STATISTICS")
    print("="*80)
    
    with app.app_context():
        print(f"\n📊 Total Records: {Todo.query.count() + Event.query.count() + Habit.query.count() + Note.query.count()}")
        
        print(f"\n📝 Todos:")
        print(f"  • Total: {Todo.query.count()}")
        print(f"  • Completed: {Todo.query.filter_by(completed=True).count()}")
        print(f"  • Pending: {Todo.query.filter_by(completed=False).count()}")
        
        high = Todo.query.filter_by(priority='high').count()
        medium = Todo.query.filter_by(priority='medium').count()
        low = Todo.query.filter_by(priority='low').count()
        print(f"  • By Priority: High({high}) Medium({medium}) Low({low})")
        
        print(f"\n📅 Events:")
        print(f"  • Total: {Event.query.count()}")
        
        print(f"\n🎯 Habits:")
        print(f"  • Total: {Habit.query.count()}")
        if Habit.query.count() > 0:
            max_streak = max([h.streak for h in Habit.query.all()])
            print(f"  • Max Streak: {max_streak}")
        
        print(f"\n📌 Notes:")
        print(f"  • Total: {Note.query.count()}")
        
        print(f"\n⏰ Database Last Modified:")
        import os
        if os.path.exists('habitflow.db'):
            last_modified = os.path.getmtime('habitflow.db')
            last_modified_date = datetime.fromtimestamp(last_modified)
            print(f"  • {last_modified_date}")

def print_quick_reference():
    """Print quick reference guide"""
    print("\n" + "="*80)
    print("QUICK REFERENCE GUIDE")
    print("="*80)
    
    guide = """
DATABASE COMMANDS:
  db.bat init           Initialize database
  db.bat seed           Add sample data
  db.bat info           Show statistics
  db.bat export         Backup data to JSON
  db.bat reset          Reset database
  db.bat clear          Clear all data

PYTHON QUERIES:
  from db_utils import *
  
  get_high_priority_todos()          Get urgent tasks
  get_upcoming_events(days=7)         Get next week's events
  get_top_habits(limit=5)            Get best performing habits
  get_database_statistics()          Get all stats
  search_todos('keyword')            Find todos
  search_notes('keyword')            Find notes

API ENDPOINTS:
  GET  /api/todos                    List all todos
  POST /api/todos                    Create todo
  PUT  /api/todos/<id>               Update todo
  DELETE /api/todos/<id>             Delete todo
  
  GET  /api/events                   List all events
  POST /api/events                   Create event
  
  GET  /api/habits                   List all habits
  POST /api/habits                   Create habit
  POST /api/habits/<id>/toggle       Toggle habit day
  
  GET  /api/notes                    List all notes
  POST /api/notes                    Create note

KEY FILES:
  app.py            Main Flask application
  models.py         Data models (tables)
  database.py       DB management utilities
  db_utils.py       Query utilities
  habitflow.db      SQLite database file
  DATABASE.md       Schema documentation
"""
    print(guide)

def export_schema_sql():
    """Export the schema as SQL CREATE statements"""
    with app.app_context():
        print("\n" + "="*80)
        print("SQL CREATE STATEMENTS")
        print("="*80)
        
        # Get the SQL that created these tables
        from sqlalchemy.schema import CreateTable
        
        models = [Todo, Event, Habit, Note]
        for model in models:
            create_stmt = CreateTable(model.__table__)
            print(f"\n{create_stmt.compile(dialect=None)}\n")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'schema':
            print_schema()
        elif command == 'relationships':
            print_relationships()
        elif command == 'statistics':
            print_statistics()
        elif command == 'reference':
            print_quick_reference()
        elif command == 'sql':
            export_schema_sql()
        else:
            print("Database Analysis Tool")
            print("\nAvailable commands:")
            print("  python db_analysis.py schema         Show complete schema")
            print("  python db_analysis.py statistics     Show database stats")
            print("  python db_analysis.py relationships  Show model relationships")
            print("  python db_analysis.py reference      Show quick reference guide")
            print("  python db_analysis.py sql            Export SQL statements")
    else:
        # Show everything
        print_schema()
        print_statistics()
        print_quick_reference()
