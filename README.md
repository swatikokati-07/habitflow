# HabitFlow - Habit Tracking Application

A full-stack habit and productivity tracking web application with Python Flask backend and HTML5 frontend.

## Features

- **To-Do List** - Create, manage, and organize tasks with priority levels
- **Calendar** - Schedule events and view them by day
- **Habits** - Track daily habits with streak counters
- **Progress Tracking** - Visualize weekly activity and habit progress
- **Timer & Stopwatch** - Built-in time tracking tools
- **Pomodoro Timer** - Productivity timer with work/break cycles
- **Quick Notes** - Color-coded note-taking system
- **Dark/Light Theme** - Toggle between themes

## Backend Architecture

### Technology Stack
- **Framework**: Flask 2.3.3
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **CORS**: Flask-CORS

### Database Models
- **Todo** - Tasks with priority and completion status
- **Event** - Calendar events with date and time
- **Habit** - Habits with streak tracking and completion history
- **Note** - Quick notes with color coding

### API Endpoints

#### Todos
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create new todo
- `PUT /api/todos/<id>` - Update todo
- `DELETE /api/todos/<id>` - Delete todo

#### Events
- `GET /api/events` - Get all events
- `POST /api/events` - Create new event
- `DELETE /api/events/<id>` - Delete event

#### Habits
- `GET /api/habits` - Get all habits
- `POST /api/habits` - Create new habit
- `PUT /api/habits/<id>` - Update habit
- `POST /api/habits/<id>/toggle` - Toggle habit day completion
- `DELETE /api/habits/<id>` - Delete habit

#### Notes
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create new note
- `DELETE /api/notes/<id>` - Delete note

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Navigate to the project directory:
```bash
cd "path/to/New folder"
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. The database will be created automatically on first run.

## Running the Application

### Start the Flask Server

1. Open PowerShell or Command Prompt
2. Navigate to the project directory
3. Run the Flask application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

4. Open your web browser and go to:
```
http://localhost:5000
```

### Frontend
The frontend is a single-page application (SPA) that automatically loads when you visit the server URL. It communicates with the backend API for all data operations.

## File Structure

```
New folder/
├── app.py                 # Flask application and API routes
├── models.py             # SQLAlchemy database models
├── requirements.txt      # Python dependencies
├── habbit.html           # Frontend (HTML/CSS/JavaScript)
├── habitflow.db          # SQLite database (auto-created)
└── README.md            # This file
```

## Development Notes

### Database
- Database file `habitflow.db` is automatically created in the project root
- Uses SQLite for simplicity and portability
- Data persists between server restarts

### Frontend-Backend Communication
- All data is fetched from the API endpoints
- Uses async/await for API calls
- CORS is enabled for cross-origin requests
- Error handling with user-friendly alerts

### Theme Support
- Dark theme (default)
- Light theme (toggle in UI)
- Theme preference is stored in browser only

## Troubleshooting

### Server won't start
- Ensure Python 3.8+ is installed
- Verify all packages installed: `pip install -r requirements.txt`
- Check if port 5000 is in use

### Data not persisting
- Ensure `habitflow.db` file has write permissions
- Check browser console for API errors
- Verify Flask server is running

### CORS errors
- May occur if frontend and backend are on different origins
- CORS is enabled in app.py with `CORS(app)`

## Future Enhancements

- User authentication and multi-user support
- Data backup and export features
- Advanced analytics and reports
- Mobile app version
- Recurring habits and task templates
- Integration with calendar services (Google Calendar, etc.)

## License

This project is provided as-is for educational and personal use.
