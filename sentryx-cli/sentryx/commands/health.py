import subprocess
import requests
import click
from rich.console import Console
from rich.panel import Panel

console = Console()

def check_docker_daemon() -> bool:
    """Verifies if the Docker daemon is active on the host machine."""
    try:
        # Suppress output; we only care about the return code (0 = success)
        subprocess.run(
            ["docker", "info"], 
            capture_output=True, 
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_sentryx_core(url: str = "http://localhost:5000/health") -> bool:
    """Pings the Flask backend core to ensure it is responsive."""
    try:
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False