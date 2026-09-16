from flask import Flask
from config import Config
from flask_cors import CORS
from routes.ml_routes import ml_bp
from routes.auth_routes import auth_bp
from routes.booking_routes import booking_bp
from routes.resource_routes import resource_bp
from routes.analytics_routes import analytics_bp
from utils.db import init_db_pool, get_connection, release_connection

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(resource_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(ml_bp)

CORS(app)

init_db_pool()
app.register_blueprint(auth_bp)


@app.route("/")
def health_check():
    return {"status": "ok", "service": "smart-campus-backend"}, 200


@app.route("/test-db")
def test_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM resources")
    result = cursor.fetchone()
    cursor.close()
    release_connection(conn)
    return {"resources_count": result[0]}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=(Config.FLASK_ENV == "development"))
