# run.py
from application import create_app, db
from application import models
from flask import jsonify
# from flask_migrate import Migrate

app = create_app()
# migrate = Migrate(app, db)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
