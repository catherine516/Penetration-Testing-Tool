from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/start-port-scan', methods=['POST'])
def start_port_scan():
    data = request.json
    target = data.get('target')
    port_range = data.get('range')

    if not target or not port_range:
        return jsonify({'error': 'Target and port range are required'}), 400

    try:
        # Simulate running a port scan script
        result = subprocess.run(
            ['python', 'port_scanner.py', target, port_range],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return jsonify({'error': result.stderr.strip()}), 500

        # Ensure the output is valid JSON
        ports = json.loads(result.stdout)
        return jsonify({'ports': ports})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start-brute-force', methods=['POST'])
def start_brute_force():
    data = request.json
    target = data.get('target')
    username = data.get('username')
    wordlist = data.get('wordlist')

    if not target or not username or not wordlist:
        return jsonify({'error': 'Target, username, and wordlist are required'}), 400

    try:
        # Simulate running a brute-force script
        result = subprocess.run(
            ['python', 'brute_force.py', target, username, wordlist],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return jsonify({'error': result.stderr.strip()}), 500

        # Ensure the output is valid JSON
        attempts = json.loads(result.stdout)
        return jsonify({'attempts': attempts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/port-scan-results', methods=['GET'])
def get_port_scan_results():
    # Simulate fetching port scan results
    return jsonify({'ports': [{'port': 80, 'status': 'open', 'service': 'http', 'vulnerabilities': []}]})

@app.route('/api/brute-force-results', methods=['GET'])
def get_brute_force_results():
    # Simulate fetching brute-force results
    return jsonify({'attempts': [{'success': True}, {'success': False}, {'success': False}]})

if __name__ == '__main__':
    app.run(debug=True)
