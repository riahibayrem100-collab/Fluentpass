
import os
import sys
from flask import Flask
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.routes.auth import auth_bp
from src.routes.content import content_bp
from src.routes.anki import anki_bp
from src.routes.speaking import speaking_bp
from src.routes.writing import writing_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(content_bp, url_prefix="/content")
app.register_blueprint(anki_bp, url_prefix="/anki")
app.register_blueprint(speaking_bp, url_prefix="/speaking")
app.register_blueprint(writing_bp, url_prefix="/writing")

@app.route("/")
def home():
    return "Welcome to FluentPass Backend!"

if __name__ == "__main__":
    print(sys.path)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


