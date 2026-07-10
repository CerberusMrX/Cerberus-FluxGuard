<div align="center">
  <h1>🛡️ Cerberus FluxGuard</h1>
  <p><strong>WebSocket Security Intelligence Platform</strong></p>

  [![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://python.org)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
</div>

<br />

## 📖 About

**Cerberus FluxGuard** is a Python-based open-source tool designed for testing and monitoring WebSocket security. It empowers developers, penetration testers, and security researchers to identify common vulnerabilities, monitor live traffic, and generate comprehensive security reports.

---

## ✨ Features

- 🚀 **Easy-to-use** command-line interface
- 📦 **Automatic installation** of required Python packages
- 🔍 **Full WebSocket security scanning**
- ⚡ **Quick scan mode** for rapid testing
- 📡 **Live WebSocket traffic monitoring**
- 💣 **200+ built-in security payloads**
- 🎯 **Advanced Vulnerability Testing**:
  - Authentication Bypass
  - Cross-Site Scripting (XSS)
  - Server-Side Template Injection (SSTI)
  - SQL Injection (SQLi)
  - NoSQL Injection
  - Command Injection
  - Path Traversal
  - XML External Entity (XXE)
  - Deserialization
  - Denial of Service (DoS)
- 🕵️ **Finds sensitive data exposure**
- 🚨 **Detects WebSocket-specific security issues**
- 📊 **Generates comprehensive reports** in JSON and HTML
- 🎨 **Colorful and intuitive** terminal output
- 💻 **Cross-platform**: Works on Linux, Windows, and macOS

---

## 🛠️ Installation

Clone the repository and navigate into the directory:

```bash
git clone https://github.com/CerberusMrX/cerberus_fluxguard.git
cd cerberus_fluxguard
```

Run the tool directly. On the first run, FluxGuard automatically installs any missing Python packages:

```bash
python3 cerberus_fluxguard.py
```

---

## 🚀 Usage

Launch the interactive tool menu:

```bash
python3 cerberus_fluxguard.py
```

**Main Menu:**
```text
[1] Full Scan
[2] Quick Scan
[3] Live Monitor
[4] Payloads
[5] Scan History
[6] Export Report
[7] Help
[0] Exit
```

### Direct Commands
You can bypass the menu using direct command-line arguments:

```bash
# Full Scan
python3 cerberus_fluxguard.py scan ws://localhost:8080

# Quick Scan
python3 cerberus_fluxguard.py quick ws://localhost:8080

# Live Monitor
python3 cerberus_fluxguard.py monitor ws://localhost:8080
```

---

## 🔬 Scan Modules

FluxGuard performs deep inspections for the following weaknesses:

- WebSocket handshake issues
- Authentication bypass vulnerabilities
- Injection vulnerabilities
- Hidden endpoints discovery
- Rate limiting weaknesses
- DoS (Denial of Service) vulnerabilities
- Sensitive data exposure
- WebSocket-specific attacks
- Security headers evaluation
- SSL/TLS configuration flaws
- CORS misconfigurations

---

## 📈 Reports

After completing any scan, you can export the findings to analyze them or share them with your team. Supported formats:
- **JSON**
- **HTML**

---

## 📸 Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/cfba122a-d25f-409a-879c-58426136b291" width="85%" alt="Cerberus FluxGuard Screenshot">
</p>

---

## ⚙️ Requirements

- **Python 3.x**

Required libraries *(installed automatically by the tool)*:
- `websocket-client`
- `requests`
- `rich`
- `colorama`
- `pyfiglet`

---

## ⚠️ Disclaimer

**For authorized security testing only.** 

Use this tool only on systems you own, manage, or have explicit permission to test. The author is not responsible for any misuse, damage, or illegal activities caused by this software.

---

## 👨‍💻 Author

**Sudeepa Wanigarathna**  
*Powered by Serendibware*

**License:** MIT
