import os
from flask import Flask, jsonify
from dotenv import load_dotenv
# from db import get_db  # Uncomment when Mongo is running

load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple endpoint for Vanguard CLI to ping."""
    return jsonify({
        "status": "SentryX Core Online",
        "version": "0.1.0"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    
    # remeber '0.0.0.0' ---> for Docker ##
    app.run(host='0.0.0.0', port=port, debug=True)