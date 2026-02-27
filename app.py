from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habitflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============ MODELS ============
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    priority = db.Column(db.String(20), default='medium')
    completed = db.Column(db.Boolean, default=False)
    date = db.Column(db.String(50))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(10))
    description = db.Column(db.String(500))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    color = db.Column(db.Integer, default=1)
    date = db.Column(db.String(50))

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    icon = db.Column(db.String(100))
    streak = db.Column(db.Integer, default=0)
    completedDays = db.Column(db.String(50), default='')

# ============ AUTH ENDPOINTS ============
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'user': {'id': user.id, 'email': user.email}}), 201
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        return jsonify({'user': {'id': user.id, 'email': user.email}}), 200
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

# ============ TODO ENDPOINTS ============
@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        user_id = request.args.get('user_id')
        todos = Todo.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': t.id, 'text': t.text, 'priority': t.priority,
            'completed': t.completed, 'date': t.date
        } for t in todos]), 200
    except Exception as e:
        print(f"Get todos error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos', methods=['POST'])
def create_todo():
    try:
        data = request.json
        todo = Todo(
            user_id=data['user_id'],
            text=data['text'],
            priority=data.get('priority', 'medium'),
            date=data.get('date')
        )
        db.session.add(todo)
        db.session.commit()
        return jsonify({'id': todo.id, 'text': todo.text, 'priority': todo.priority, 'completed': todo.completed, 'date': todo.date}), 201
    except Exception as e:
        print(f"Create todo error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    try:
        data = request.json
        todo = Todo.query.get(id)
        todo.text = data.get('text', todo.text)
        todo.priority = data.get('priority', todo.priority)
        todo.completed = data.get('completed', todo.completed)
        db.session.commit()
        return jsonify({'id': todo.id, 'text': todo.text, 'priority': todo.priority, 'completed': todo.completed, 'date': todo.date}), 200
    except Exception as e:
        print(f"Update todo error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        todo = Todo.query.get(id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204
    except Exception as e:
        print(f"Delete todo error: {e}")
        return jsonify({'error': str(e)}), 500

# ============ EVENT ENDPOINTS ============
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        user_id = request.args.get('user_id')
        events = Event.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': e.id, 'title': e.title, 'date': e.date,
            'time': e.time, 'description': e.description
        } for e in events]), 200
    except Exception as e:
        print(f"Get events error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['POST'])
def create_event():
    try:
        data = request.json
        event = Event(
            user_id=data['user_id'],
            title=data['title'],
            date=data['date'],
            time=data.get('time'),
            description=data.get('description')
        )
        db.session.add(event)
        db.session.commit()
        return jsonify({'id': event.id, 'title': event.title, 'date': event.date, 'time': event.time, 'description': event.description}), 201
    except Exception as e:
        print(f"Create event error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    try:
        event = Event.query.get(id)
        db.session.delete(event)
        db.session.commit()
        return '', 204
    except Exception as e:
        print(f"Delete event error: {e}")
        return jsonify({'error': str(e)}), 500

# ============ HABIT ENDPOINTS ============
@app.route('/api/habits', methods=['GET'])
def get_habits():
    try:
        user_id = request.args.get('user_id')
        habits = Habit.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': h.id, 'name': h.name, 'description': h.description,
            'icon': h.icon, 'streak': h.streak,
            'completedDays': [int(x) for x in h.completedDays.split(',') if x]
        } for h in habits]), 200
    except Exception as e:
        print(f"Get habits error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/habits', methods=['POST'])
def create_habit():
    try:
        data = request.json
        habit = Habit(
            user_id=data['user_id'],
            name=data['name'],
            description=data.get('description'),
            icon=data.get('icon'),
            streak=0
        )
        db.session.add(habit)
        db.session.commit()
        return jsonify({'id': habit.id, 'name': habit.name, 'description': habit.description, 'icon': habit.icon, 'streak': habit.streak, 'completedDays': []}), 201
    except Exception as e:
        print(f"Create habit error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/habits/<int:id>/toggle', methods=['POST'])
def toggle_habit(id):
    try:
        data = request.json
        day = data.get('day')
        habit = Habit.query.get(id)
        
        days = [int(x) for x in habit.completedDays.split(',') if x]
        if day in days:
            days.remove(day)
        else:
            days.append(day)
        
        habit.completedDays = ','.join(map(str, days))
        habit.streak = len(days)
        db.session.commit()
        
        return jsonify({'id': habit.id, 'name': habit.name, 'description': habit.description, 'icon': habit.icon, 'streak': habit.streak, 'completedDays': days}), 200
    except Exception as e:
        print(f"Toggle habit error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/habits/<int:id>', methods=['DELETE'])
def delete_habit(id):
    try:
        habit = Habit.query.get(id)
        db.session.delete(habit)
        db.session.commit()
        return '', 204
    except Exception as e:
        print(f"Delete habit error: {e}")
        return jsonify({'error': str(e)}), 500

# ============ NOTE ENDPOINTS ============
@app.route('/api/notes', methods=['GET'])
def get_notes():
    try:
        user_id = request.args.get('user_id')
        notes = Note.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': n.id, 'title': n.title, 'content': n.content,
            'color': n.color, 'date': n.date
        } for n in notes]), 200
    except Exception as e:
        print(f"Get notes error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes', methods=['POST'])
def create_note():
    try:
        data = request.json
        note = Note(
            user_id=data['user_id'],
            title=data['title'],
            content=data['content'],
            color=data.get('color', 1),
            date=data.get('date')
        )
        db.session.add(note)
        db.session.commit()
        return jsonify({'id': note.id, 'title': note.title, 'content': note.content, 'color': note.color, 'date': note.date}), 201
    except Exception as e:
        print(f"Create note error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    try:
        note = Note.query.get(id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        print(f"Delete note error: {e}")
        return jsonify({'error': str(e)}), 500

# ============ HEALTH CHECK ============
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

# ============ SERVE HTML ============
@app.route('/')
def index():
    return send_file('habbit.html', mimetype='text/html')

# ============ PWA FILES ============
@app.route('/manifest.json')
def manifest():
    return send_file('manifest.json', mimetype='application/json')

@app.route('/service-worker.js')
def service_worker():
    response = send_file('service-worker.js', mimetype='application/javascript')
    response.headers['Cache-Control'] = 'no-cache'
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
