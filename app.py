from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# When a client sends an SDP offer or ICE candidate, broadcast it
@socketio.on("signal")
def handle_signal(data):
    print("Received signaling message:", data.keys())
    emit("signal", data, broadcast=True)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
