import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.database.init_db import init_database
from src.database.init_content import init_content_database
from src.routes.auth import auth_bp
from src.routes.ai_coach import ai_coach_bp
from src.routes.progress import progress_bp
from src.routes.speaking_coach import speaking_coach_bp
from src.routes.content import content_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
CORS(app) # Enable CORS for all routes
app.config['SECRET_KEY'] = 'your_super_secret_key_here' # TODO: Change this to a strong, random key

# Initialize database on app startup
with app.app_context():
    init_database()
    init_content_database()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(ai_coach_bp, url_prefix='/api/ai')
app.register_blueprint(progress_bp, url_prefix='/api/progress')
app.register_blueprint(speaking_coach_bp, url_prefix='/api/speaking')
app.register_blueprint(content_bp)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    # Use 0.0.0.0 for Render deployment
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=False)



