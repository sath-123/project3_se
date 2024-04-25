from application import create_app  # Use the create_app method
from flask import jsonify

app = create_app()  # Create the Flask instance


# Define your endpoints
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
