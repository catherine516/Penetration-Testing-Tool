document.addEventListener('DOMContentLoaded', () => {
    // Ensure the backend is reachable
    fetch('/api/port-scan-results')
        .then(response => {
            if (!response.ok) throw new Error('Backend not reachable');
            return response.json();
        })
        .then(data => {
            const table = document.getElementById('port-scanner-table');
            table.innerHTML = ''; // Clear existing rows
            data.ports.forEach(port => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${port.port}</td>
                    <td>${port.status}</td>
                    <td>${port.service}</td>
                    <td>${port.vulnerabilities.join(', ')}</td>
                `;
                table.appendChild(row);
            });
        })
        .catch(error => logActivity(`Error: ${error.message}`));

    // Fetch and display brute-force results
    fetch('/api/brute-force-results')
        .then(response => response.json())
        .then(data => {
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
        })
        .catch(error => logActivity(`Error fetching brute-force results: ${error.message}`));
});

function startPortScan() {
    const target = document.getElementById('port-scan-target').value;
    const range = document.getElementById('port-range').value;

    if (!target || !range) {
        alert('Please enter both target and port range.');
        return;
    }

    logActivity(`Starting port scan on ${target} with range ${range}...`);

    fetch('/api/start-port-scan', {
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

    fetch('/api/start-brute-force', {
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

function logActivity(message) {
    const logList = document.getElementById('log-list');
    const logItem = document.createElement('li');
    logItem.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    logList.appendChild(logItem);
}
