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
    

    
@click.command(name="status")
def status_command():
    """Checks the health of the Docker Daemon and SentryX Core."""
    console.print("Running SentryX diagnostics...", style="bold cyan")
    
    # 1. Check Docker
    docker_ok = check_docker_daemon()
    docker_status = "[bold green]ONLINE[/]" if docker_ok else "[bold red]OFFLINE[/]"
    docker_msg = f"Docker Daemon: {docker_status}"
    
    # 2. Check Flask Core
    core_ok = check_sentryx_core()
    core_status = "[bold green]ONLINE[/]" if core_ok else "[bold red]OFFLINE[/]"
    core_msg = f"SentryX Core : {core_status}"
    
    # Render a Neobrutalist-style status panel
    panel_content = f"{docker_msg}\n{core_msg}"
    border_color = "green" if (docker_ok and core_ok) else "red"
    
    console.print(Panel(
        panel_content, 
        title="[bold]System Status[/]", 
        border_style=border_color,
        expand=False
    ))

    if not docker_ok:
        console.print("[dim]Hint: Is Docker Desktop running?[/]")
    elif not core_ok:
        console.print("[dim]Hint: Did you run 'make up' to start the backend?[/]")