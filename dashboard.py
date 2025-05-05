from flask import Flask, render_template_string, request, jsonify
import subprocess

app = Flask(__name__)

# HTML Template for the Dashboard
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Penetration Testing Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .container { max-width: 800px; margin: auto; }
        .section { margin-bottom: 30px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        table, th, td { border: 1px solid #ccc; }
        th, td { padding: 8px; text-align: left; }
        .log { background: #f9f9f9; padding: 10px; border: 1px solid #ccc; height: 150px; overflow-y: auto; }
        button { padding: 10px 15px; background: #007BFF; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Penetration Testing Dashboard</h1>

        <div class="section">
            <h2>Port Scanner</h2>
            <label>Target: <input type="text" id="port-scan-target"></label>
            <label>Port Range: <input type="text" id="port-range"></label>
            <button onclick="startPortScan()">Run Port Scan</button>
            <table id="port-scanner-table">
                <thead>
                    <tr>
                        <th>Port</th>
                        <th>Status</th>
                        <th>Service</th>
                        <th>Vulnerabilities</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>

        <div class="section">
            <h2>Brute-Force Tester</h2>
            <label>Target: <input type="text" id="brute-force-target"></label>
            <label>Username: <input type="text" id="username"></label>
            <label>Wordlist: <input type="text" id="wordlist"></label>
            <button onclick="startBruteForce()">Run Brute Force</button>
            <canvas id="brute-force-chart" width="400" height="200"></canvas>
        </div>

        <div class="section">
            <h2>Activity Log</h2>
            <div class="log" id="log-list"></div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        function logActivity(message) {
            const logList = document.getElementById('log-list');
            const logItem = document.createElement('div');
            logItem.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            logList.appendChild(logItem);
        }

        function startPortScan() {
            const target = document.getElementById('port-scan-target').value;
            const range = document.getElementById('port-range').value;

            if (!target || !range) {
                alert('Please enter both target and port range.');
                return;
            }

            logActivity(`Starting port scan on ${target} with range ${range}...`);

            fetch('/start-port-scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target, range })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    logActivity(`Error: ${data.error}`);
                    return;
                }

                const tableBody = document.querySelector('#port-scanner-table tbody');
                tableBody.innerHTML = ''; // Clear previous results
                data.ports.forEach(port => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${port.port}</td>
                        <td>${port.status}</td>
                        <td>${port.service}</td>
                        <td>${port.vulnerabilities.join(', ')}</td>
                    `;
                    tableBody.appendChild(row);
                });
                logActivity('Port scan completed.');
            })
            .catch(error => logActivity(`Error during port scan: ${error.message}`));
        }

        function startBruteForce() {
            const target = document.getElementById('brute-force-target').value;
            const username = document.getElementById('username').value;
            const wordlist = document.getElementById('wordlist').value;

            if (!target || !username || !wordlist) {
                alert('Please enter target, username, and wordlist.');
                return;
            }

            logActivity(`Starting brute-force attack on ${target} with username ${username}...`);

            fetch('/start-brute-force', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target, username, wordlist })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    logActivity(`Error: ${data.error}`);
                    return;
                }

                const ctx = document.getElementById('brute-force-chart').getContext('2d');
                const successCount = data.attempts.filter(attempt => attempt.success).length;
                const failureCount = data.attempts.length - successCount;

                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Success', 'Failure'],
                        datasets: [{
                            label: 'Brute-Force Results',
                            data: [successCount, failureCount],
                            backgroundColor: ['green', 'red']
                        }]
                    }
                });
                logActivity('Brute-force attack completed.');
            })
            .catch(error => logActivity(`Error during brute-force attack: ${error.message}`));
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(dashboard_html)

@app.route('/start-port-scan', methods=['POST'])
def start_port_scan():
    data = request.json
    target = data.get('target')
    port_range = data.get('range')

    if not target or not port_range:
        return jsonify({'error': 'Target and port range are required'}), 400

    try:
        result = subprocess.run(
            ['python', 'port_scanner.py', target, port_range],
            capture_output=True, text=True
        )
        return jsonify({'ports': eval(result.stdout)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start-brute-force', methods=['POST'])
def start_brute_force():
    data = request.json
    target = data.get('target')
    username = data.get('username')
    wordlist = data.get('wordlist')

    if not target or not username or not wordlist:
        return jsonify({'error': 'Target, username, and wordlist are required'}), 400

    try:
        result = subprocess.run(
            ['python', 'brute_force.py', target, username, wordlist],
            capture_output=True, text=True
        )
        return jsonify({'attempts': eval(result.stdout)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
