#!/usr/bin/env python3
"""
Script to create a sample Git repository for testing git-taz.

This script creates a repository with:
- Main branch with several commits
- Feature branches with different features
- Version branches (release branches)
- One branch that doesn't have all features from main
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import List


def run_git_command(command: List[str], cwd: str) -> None:
    """Run a git command in the specified directory."""
    try:
        subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"✓ {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running {' '.join(command)}: {e.stderr}")
        raise


def create_file_with_content(repo_path: str, filename: str, content: str) -> None:
    """Create a file with specific content."""
    file_path = Path(repo_path) / filename
    file_path.write_text(content)
    print(f"Created {filename}")


def create_sample_repo(repo_path: str) -> None:
    """Create a sample Git repository with branches and commits."""
    print(f"Creating sample repository at: {repo_path}")

    # Initialize the repository
    run_git_command(["git", "init"], repo_path)
    run_git_command(["git", "config", "user.name", "Test User"], repo_path)
    run_git_command(["git", "config", "user.email", "test@example.com"], repo_path)

    # Create initial files on main branch
    print("\n=== Setting up main branch ===")
    create_file_with_content(
        repo_path,
        "README.md",
        """# Sample Project

This is a sample project for testing git-taz.

## Features
- Basic functionality
- User authentication
- Data processing
- API endpoints
- Dashboard UI
""",
    )

    create_file_with_content(
        repo_path,
        "main.py",
        """#!/usr/bin/env python3
\"\"\"Main application entry point.\"\"\"

def main():
    print("Hello, World!")
    
if __name__ == "__main__":
    main()
""",
    )

    create_file_with_content(
        repo_path,
        "requirements.txt",
        """requests>=2.25.0
flask>=2.0.0
""",
    )

    # Initial commit
    run_git_command(["git", "add", "."], repo_path)
    run_git_command(
        ["git", "commit", "-m", "Initial commit: Basic project structure"], repo_path
    )

    # Add authentication feature
    print("\n=== Adding authentication feature ===")
    create_file_with_content(
        repo_path,
        "auth.py",
        """\"\"\"Authentication module.\"\"\"

class AuthManager:
    def __init__(self):
        self.users = {}
    
    def login(self, username, password):
        return username in self.users and self.users[username] == password
    
    def register(self, username, password):
        self.users[username] = password
        return True
""",
    )

    # Update main.py to include auth
    create_file_with_content(
        repo_path,
        "main.py",
        """#!/usr/bin/env python3
\"\"\"Main application entry point.\"\"\"

from auth import AuthManager

def main():
    print("Hello, World!")
    auth = AuthManager()
    print("Authentication system initialized")
    
if __name__ == "__main__":
    main()
""",
    )

    run_git_command(["git", "add", "."], repo_path)
    run_git_command(
        ["git", "commit", "-m", "feat: Add user authentication system"], repo_path
    )

    # Add data processing feature
    print("\n=== Adding data processing feature ===")
    create_file_with_content(
        repo_path,
        "data_processor.py",
        """\"\"\"Data processing utilities.\"\"\"

import json
from typing import Dict, List, Any

class DataProcessor:
    def __init__(self):
        self.data = []
    
    def load_data(self, filename: str) -> None:
        with open(filename, 'r') as f:
            self.data = json.load(f)
    
    def process_data(self) -> List[Dict[str, Any]]:
        # Simple data transformation
        return [{'id': i, 'processed': True, **item}
                for i, item in enumerate(self.data)]
    
    def save_data(self, filename: str, data: List[Dict[str, Any]]) -> None:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
""",
    )

    run_git_command(["git", "add", "data_processor.py"], repo_path)
    run_git_command(
        ["git", "commit", "-m", "feat: Add data processing capabilities"], repo_path
    )

    # Add API endpoints
    print("\n=== Adding API endpoints ===")
    create_file_with_content(
        repo_path,
        "api.py",
        """\"\"\"REST API endpoints.\"\"\"

from flask import Flask, jsonify, request
from auth import AuthManager
from data_processor import DataProcessor

app = Flask(__name__)
auth_manager = AuthManager()
data_processor = DataProcessor()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    success = auth_manager.login(data['username'], data['password'])
    return jsonify({'success': success})

@app.route('/api/data', methods=['GET'])
def get_data():
    processed = data_processor.process_data()
    return jsonify(processed)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)
""",
    )

    run_git_command(["git", "add", "api.py"], repo_path)
    run_git_command(["git", "commit", "-m", "feat: Add REST API endpoints"], repo_path)

    # Create feature branch: dashboard-ui
    print("\n=== Creating feature/dashboard-ui branch ===")
    run_git_command(["git", "checkout", "-b", "feature/dashboard-ui"], repo_path)

    create_file_with_content(
        repo_path,
        "dashboard.py",
        """\"\"\"Web dashboard interface.\"\"\"

from flask import Flask, render_template_string
from api import app

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sample Project Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; }
        .status { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Project Dashboard</h1>
    <div class="card">
        <h3>System Status</h3>
        <p class="status">All systems operational</p>
    </div>
    <div class="card">
        <h3>Quick Actions</h3>
        <button onclick="alert('Login feature')">Login</button>
        <button onclick="alert('Data processing')">Process Data</button>
    </div>
</body>
</html>
'''

@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)
""",
    )

    run_git_command(["git", "add", "dashboard.py"], repo_path)
    run_git_command(
        ["git", "commit", "-m", "feat: Add web dashboard interface"], repo_path
    )

    # Create feature branch: advanced-auth
    print("\n=== Creating feature/advanced-auth branch ===")
    run_git_command(["git", "checkout", "main"], repo_path)
    run_git_command(["git", "checkout", "-b", "feature/advanced-auth"], repo_path)

    # Update auth.py with advanced features
    create_file_with_content(
        repo_path,
        "auth.py",
        """\"\"\"Advanced authentication module.\"\"\"

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional

class AuthManager:
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.failed_attempts = {}
    
    def _hash_password(self, password: str, salt: str) -> str:
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        
        salt = secrets.token_hex(16)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = {
            'password_hash': hashed_password,
            'salt': salt,
            'created_at': datetime.now()
        }
        return True
    
    def login(self, username: str, password: str) -> Optional[str]:
        # Check failed attempts (simple rate limiting)
        if username in self.failed_attempts:
            if self.failed_attempts[username] >= 5:
                return None
        
        if username not in self.users:
            self._record_failed_attempt(username)
            return None
        
        user_data = self.users[username]
        hashed_password = self._hash_password(password, user_data['salt'])
        
        if hashed_password == user_data['password_hash']:
            # Clear failed attempts on successful login
            if username in self.failed_attempts:
                del self.failed_attempts[username]
            
            # Create session
            session_token = secrets.token_urlsafe(32)
            self.sessions[session_token] = {
                'username': username,
                'created_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(hours=24)
            }
            return session_token
        else:
            self._record_failed_attempt(username)
            return None
    
    def _record_failed_attempt(self, username: str) -> None:
        if username not in self.failed_attempts:
            self.failed_attempts[username] = 0
        self.failed_attempts[username] += 1
    
    def validate_session(self, session_token: str) -> Optional[str]:
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        if datetime.now() > session['expires_at']:
            del self.sessions[session_token]
            return None
        
        return session['username']
    
    def logout(self, session_token: str) -> bool:
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
""",
    )

    run_git_command(["git", "add", "auth.py"], repo_path)
    run_git_command(
        [
            "git",
            "commit",
            "-m",
            "feat: Add advanced authentication with sessions and rate limiting",
        ],
        repo_path,
    )

    # Create feature branch: data-analytics (incomplete)
    print("\n=== Creating feature/data-analytics branch (incomplete) ===")
    run_git_command(["git", "checkout", "main"], repo_path)
    # Go back to an earlier commit to simulate incomplete branch
    run_git_command(["git", "checkout", "HEAD~2"], repo_path)  # Before API was added
    run_git_command(["git", "checkout", "-b", "feature/data-analytics"], repo_path)

    create_file_with_content(
        repo_path,
        "analytics.py",
        """\"\"\"Data analytics module (work in progress).\"\"\"

import statistics
from typing import List, Dict, Any

class Analytics:
    def __init__(self):
        self.metrics = {}
    
    def calculate_basic_stats(self, data: List[float]) -> Dict[str, float]:
        if not data:
            return {}
        
        return {
            'mean': statistics.mean(data),
            'median': statistics.median(data),
            'std_dev': statistics.stdev(data) if len(data) > 1 else 0,
            'min': min(data),
            'max': max(data)
        }
    
    # TODO: Add more advanced analytics
    # TODO: Add visualization capabilities
    # TODO: Add export functionality
""",
    )

    run_git_command(["git", "add", "analytics.py"], repo_path)
    run_git_command(
        ["git", "commit", "-m", "wip: Start data analytics module (incomplete)"],
        repo_path,
    )

    # Create version branches
    print("\n=== Creating version branches ===")

    # v1.0.0 - Basic version
    run_git_command(["git", "checkout", "main"], repo_path)
    run_git_command(["git", "checkout", "HEAD~2"], repo_path)  # Before API was added
    run_git_command(["git", "checkout", "-b", "release/v1.0.0"], repo_path)

    create_file_with_content(repo_path, "VERSION", "1.0.0")
    run_git_command(["git", "add", "VERSION"], repo_path)
    run_git_command(
        ["git", "commit", "-m", "release: v1.0.0 - Basic functionality with auth"],
        repo_path,
    )
    run_git_command(["git", "tag", "v1.0.0"], repo_path)

    # v1.1.0 - With data processing
    run_git_command(["git", "checkout", "main"], repo_path)
    run_git_command(["git", "checkout", "HEAD~1"], repo_path)  # Before API was added
    run_git_command(["git", "checkout", "-b", "release/v1.1.0"], repo_path)

    create_file_with_content(repo_path, "VERSION", "1.1.0")
    run_git_command(["git", "add", "VERSION"], repo_path)
    run_git_command(
        ["git", "commit", "-m", "release: v1.1.0 - Add data processing capabilities"],
        repo_path,
    )
    run_git_command(["git", "tag", "v1.1.0"], repo_path)

    # v2.0.0 - Latest with API
    run_git_command(["git", "checkout", "main"], repo_path)
    run_git_command(["git", "checkout", "-b", "release/v2.0.0"], repo_path)

    create_file_with_content(repo_path, "VERSION", "2.0.0")
    run_git_command(["git", "add", "VERSION"], repo_path)
    run_git_command(
        ["git", "commit", "-m", "release: v2.0.0 - Full API support"], repo_path
    )
    run_git_command(["git", "tag", "v2.0.0"], repo_path)

    # Go back to main
    run_git_command(["git", "checkout", "main"], repo_path)

    print(f"\n✅ Sample repository created successfully at: {repo_path}")
    print("\nBranches created:")
    print("  - main (latest with all features)")
    print("  - feature/dashboard-ui (adds web dashboard)")
    print("  - feature/advanced-auth (advanced authentication)")
    print("  - feature/data-analytics (incomplete, missing some main features)")
    print("  - release/v1.0.0 (basic version)")
    print("  - release/v1.1.0 (with data processing)")
    print("  - release/v2.0.0 (with API)")
    print("\nTags created: v1.0.0, v1.1.0, v2.0.0")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create a sample Git repository for testing"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="./sample-repo",
        help="Path where to create the sample repository (default: ./sample-repo)",
    )
    parser.add_argument(
        "--temp", action="store_true", help="Create repository in a temporary directory"
    )

    args = parser.parse_args()

    if args.temp:
        repo_path = tempfile.mkdtemp(prefix="git-taz-sample-")
    else:
        repo_path = os.path.abspath(args.path)

        # Create directory if it doesn't exist
        os.makedirs(repo_path, exist_ok=True)

    try:
        create_sample_repo(repo_path)
    except Exception as e:
        print(f"\n❌ Error creating repository: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
