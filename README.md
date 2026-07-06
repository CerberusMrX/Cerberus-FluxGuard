# Cerberus FluxGuard

## WebSocket Security Intelligence Platform

**Cerberus FluxGuard** is an advanced, open-source Python-based tool designed for comprehensive security analysis and penetration testing of WebSocket connections. It provides a robust framework to identify vulnerabilities, monitor real-time traffic, and exploit weaknesses in WebSocket implementations. Built with a focus on ease of use and powerful capabilities, FluxGuard assists developers and security professionals in securing their WebSocket-enabled applications.

## Features

-   **Automated Dependency Management**: Automatically installs all required Python packages upon initial execution, ensuring a smooth setup process.
-   **Interactive Command-Line Interface (CLI)**: Offers a user-friendly interface for initiating security scans, real-time monitoring, and comprehensive report management.
-   **Multi-Phase Scanning Engine**: Employs a 7-phase scanning methodology to cover a wide array of attack vectors pertinent to WebSocket protocols.
-   **Extensive Payload Database**: Incorporates over 200 pre-defined payloads categorized for various attack types, including:
    -   Authentication Bypass (50+ payloads)
    -   Cross-Site Scripting (XSS) (30 payloads)
    -   Server-Side Template Injection (SSTI) (25 payloads)
    -   SQL Injection (20 payloads)
    -   NoSQL Injection (15 payloads)
    -   Command Injection (20 payloads)
    -   Path Traversal (15 payloads)
    -   XML External Entity (XXE) (3 payloads)
    -   Deserialization (5 payloads)
    -   Denial of Service (DoS) (6 payloads)
-   **Real-time WebSocket Traffic Monitoring**: Provides live observation of WebSocket communications, featuring automated detection of sensitive data and highlighting of potential errors.
-   **Comprehensive Reporting**: Generates detailed security assessment reports in both JSON and HTML formats for easy analysis and archival.
-   **Enhanced Console Output**: Utilizes a complete color system for improved readability and clarity of console output.
-   **Graceful Application Shutdown**: Ensures proper termination and resource cleanup upon exit.

## Installation

Cerberus FluxGuard is designed for straightforward deployment. It is a self-contained Python script that manages its own dependencies.

1.  **Obtain the script:**

    Clone the repository from GitHub:

    ```bash
    git clone https://github.com/your-repo/cerberus_fluxguard.git
    cd cerberus_fluxguard
    ```

    Alternatively, download the `cerberus_fluxguard.py` file directly.

2.  **Execute the script:**

    ```bash
    python3 cerberus_fluxguard.py
    ```

    Upon its first execution, the script will automatically identify and install any missing Python packages, such as `websocket-client`, `colorama`, `requests`, `rich`, and `pyfiglet`.

## Usage

Upon execution, the script presents an interactive menu. Direct commands are also available for quick operations.

```
Cerberus FluxGuard - WebSocket Security Intelligence Platform

[1] Full Scan
[2] Quick Scan
[3] Monitor / Live
[4] Payloads / Arsenal
[5] History / Past
[6] Export / Report
[7] Help / ?
[0] Exit / Quit / Q

Quick Commands:
  scan ws://localhost:8080     (Run full scan directly)
  quick ws://localhost:8080    (Run quick scan directly)
  monitor ws://localhost:8080  (Start monitoring directly)
```

### Full Scan

Initiates a comprehensive 7-phase security scan against the specified WebSocket URL.

```bash
python3 cerberus_fluxguard.py
> 1
> ws://localhost:8080
```

Alternatively, use the direct command:

```bash
python3 cerberus_fluxguard.py scan ws://localhost:8080
```

### Quick Scan

Performs an expedited scan, focusing primarily on WebSocket handshake analysis and authentication bypass vulnerabilities.

```bash
python3 cerberus_fluxguard.py
> 2
> ws://localhost:8080
```

Alternatively, use the direct command:

```bash
python3 cerberus_fluxguard.py quick ws://localhost:8080
```

### Live Monitoring

Enables real-time observation of WebSocket traffic, with alerts for sensitive data exposure and error conditions.

```bash
python3 cerberus_fluxguard.py
> 3
> ws://localhost:8080
```

Alternatively, use the direct command:

```bash
python3 cerberus_fluxguard.py monitor ws://localhost:8080
```

### Viewing Payloads

Provides access to the integrated payload database for review.

```bash
python3 cerberus_fluxguard.py
> 4
```

### Exporting Reports

Following a scan, users are prompted to export the generated report in either JSON or HTML format. Past reports can also be accessed and exported from the main menu.

## Scan Phases Overview

Cerberus FluxGuard employs a structured, multi-phase scanning methodology to ensure thorough vulnerability detection:

1.  **Handshake & Protocol Analysis**: Detailed examination of the WebSocket handshake process and adherence to protocol specifications.
2.  **Authentication Bypass Testing**: Probing for weaknesses in authentication mechanisms using a variety of bypass techniques.
3.  **Injection & Fuzzing**: Comprehensive testing for common injection vulnerabilities, including XSS, SSTI, SQLi, NoSQLi, Command Injection, Path Traversal, XXE, and Deserialization.
4.  **Channel/Endpoint Discovery**: Identification of potentially hidden or undocumented WebSocket channels and communication endpoints.
5.  **Rate Limiting & DoS Resilience**: Assessment of the WebSocket server's robustness against rate limiting and Denial of Service attacks.
6.  **Sensitive Data Exposure**: Detection of sensitive information transmitted over WebSocket connections that should be protected.
7.  **WebSocket-Specific Attacks**: Exploration of vulnerabilities unique to the WebSocket protocol and its implementations.
8.  **Security Header Analysis**: Evaluation of HTTP headers for adherence to security best practices.
9.  **SSL/TLS Configuration**: Verification of proper SSL/TLS configuration to ensure secure communication.
10. **CORS Misconfiguration**: Identification of Cross-Origin Resource Sharing (CORS) misconfigurations that could lead to security bypasses.

## 🖼️ Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/cfba122a-d25f-409a-879c-58426136b291" width="48%" />
</p>

<br/>


## Technical Specifications

-   **Programming Language**: Python 3.x
-   **Key Libraries**: `websocket-client`, `colorama`, `requests`, `rich`, `pyfiglet`
-   **Operating System Compatibility**: Cross-platform (tested on Linux, macOS, Windows)
-   **Reporting Formats**: JSON, HTML

## Disclaimer

**⚠️ AUTHORIZED TESTING ONLY ⚠️**

This tool is provided for **ethical hacking and authorized security testing purposes exclusively**. The author and contributors disclaim all responsibility for any unauthorized use, misuse, or damages incurred through the application of this software. By utilizing Cerberus FluxGuard, you acknowledge and agree to employ it responsibly and solely on systems for which you possess explicit authorization for security testing.

## Author & License

-   **Author**: Sudeepa Wanigarathna
-   **Organization**: Serendibware
-   **Version**: 1.0

This project is open-source and distributed under the [MIT License](LICENSE).
