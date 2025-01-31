from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
socketio = SocketIO(app)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Socket.IO event for handling messages
@socketio.on('message')
def handle_message(msg):
    username = session.get('username', 'Anonymous')  # Get the username from the session
    formatted_message = f"{username}: {msg}"  # Prepend the username to the message
    print(f"Message: {formatted_message}")
    send(formatted_message, broadcast=True)  # Broadcast the message to all connected clients

# Socket.IO event for setting the username
@socketio.on('set_username')
def set_username(username):
    session['username'] = username  # Store the username in the session
    send(f"{username} has joined the chat!", broadcast=True)  # Notify all users

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')  # Run the app on all available interfaces