Cerberus FluxGuard

WebSocket Security Intelligence Platform

Cerberus FluxGuard is a Python-based open-source tool for testing and monitoring WebSocket security. It helps developers, penetration testers, and security researchers find common vulnerabilities, monitor live traffic, and generate security reports.

Features

- Easy to use command-line interface
- Automatic installation of required Python packages
- Full WebSocket security scanning
- Quick scan mode for fast testing
- Live WebSocket traffic monitoring
- 200+ built-in security payloads
- Tests for:
   - Authentication Bypass
   - XSS
   - SSTI
   - SQL Injection
   - NoSQL Injection
   - Command Injection
   - Path Traversal
   - XXE
   - Deserialization
   - DoS
- Finds sensitive data exposure
- Detects WebSocket security issues
- Generates JSON and HTML reports
- Colorful terminal output
- Works on Linux, Windows, and macOS

---

Installation

Clone the repository:

git clone https://github.com/CerberusMrX/cerberus_fluxguard.git
cd cerberus_fluxguard

Run the tool:

python3 cerberus_fluxguard.py

On the first run, FluxGuard automatically installs any missing Python packages.

---

Usage

Launch the tool:

python3 cerberus_fluxguard.py

Menu:

[1] Full Scan
[2] Quick Scan
[3] Live Monitor
[4] Payloads
[5] Scan History
[6] Export Report
[7] Help
[0] Exit

You can also use direct commands:

python3 cerberus_fluxguard.py scan ws://localhost:8080
python3 cerberus_fluxguard.py quick ws://localhost:8080
python3 cerberus_fluxguard.py monitor ws://localhost:8080

---

Scan Modules

FluxGuard checks for:

- WebSocket handshake issues
- Authentication bypass
- Injection vulnerabilities
- Hidden endpoints
- Rate limiting
- DoS weaknesses
- Sensitive data exposure
- WebSocket-specific attacks
- Security headers
- SSL/TLS configuration
- CORS misconfiguration

---

Reports

After every scan, you can export the results as:

- JSON
- HTML

---

Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/cfba122a-d25f-409a-879c-58426136b291" width="85%">
</p>---

Requirements

- Python 3.x

Required libraries (installed automatically):

- websocket-client
- requests
- rich
- colorama
- pyfiglet

---

Disclaimer

For authorized security testing only.

Use this tool only on systems you own or have permission to test. The author is not responsible for any misuse or damage caused by this software.

---

Author

Sudeepa Wanigarathna

Powered by Serendibware

License: MIT