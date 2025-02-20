from flask import Flask, jsonify, render_template
from flask_cors import CORS
from voice_ai import speech_to_text, generate_response  # Import ML functions

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")

@app.route("/start", methods=["GET"])
def start_voice_assistant():
    """Runs the full voice assistant loop."""
    user_query = speech_to_text()
    if not user_query:
        return jsonify({"message": "No speech detected. Please try again."})
    
    ai_response = generate_response(user_query)
    print(f"🤖 AI: {ai_response}")

    return jsonify({"message": ai_response})

if __name__ == "__main__":
    print("🚀 Voice Bridge AI Assistant is running on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
