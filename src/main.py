
import os
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_compress import Compress
from flask_caching import Cache

app = Flask(__name__, static_folder='../assets', static_url_path='/assets')
CORS(app)

# Enable compression for all responses
compress = Compress(app)

# Configure caching
cache_config = {
    'CACHE_TYPE': 'simple',  # Use simple in-memory cache for now
    'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes default timeout
}
app.config.update(cache_config)
cache = Cache(app)

# Performance optimizations
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year cache for static files

@app.route("/")
@cache.cached(timeout=3600)  # Cache for 1 hour
def home():
    return send_from_directory('../', 'index.html')

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "message": "FluentPass Backend is running!"})

# Serve static assets with proper caching headers
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    response = send_from_directory('../assets', filename)
    # Set aggressive caching for assets (they have hashed names)
    response.cache_control.max_age = 31536000  # 1 year
    response.cache_control.public = True
    return response

# Add security headers for better performance and security
@app.after_request
def after_request(response):
    # Enable GZIP compression
    response.headers['Vary'] = 'Accept-Encoding'
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Performance hints
    if request.endpoint == 'home':
        response.headers['Link'] = '</assets/index-ChLEs4-J.js>; rel=preload; as=script, </assets/index-IlUsjxHz.css>; rel=preload; as=style'
    
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


