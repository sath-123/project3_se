# run.py
from application import create_app
from flask import jsonify
app = create_app()

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)