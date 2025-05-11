from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from database import init_db, authenticate_user, register_user, create_note, get_user_notes

app = Flask(__name__)
app.secret_key = 'very_unsecure_secret_key'  # Insecure practice

# Initialize database
@app.before_first_request
def initialize():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success = register_user(username, password)
        
        if success:
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = authenticate_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('notes'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/notes')
def notes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_notes = get_user_notes(session['user_id'])
    return render_template('notes.html', notes=user_notes)

@app.route('/notes/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        create_note(session['user_id'], title, content)
        flash('Note created successfully!')
        return redirect(url_for('notes'))
    
    return render_template('create_note.html')

# VULNERABLE: Search function with potential XSS
@app.route('/search')
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    
    # Get all notes and filter on the application side
    all_notes = get_user_notes(session['user_id'])
    results = [note for note in all_notes if query.lower() in note['title'].lower() or query.lower() in note['content'].lower()]
    
    # Render the search query directly (vulnerable to XSS)
    return render_template('search.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')