import subprocess
import click
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel

# Import utilities to resolve service names to container names
from ..utils.docker_parser import find_docker_compose, load_compose_file, extract_services

console = Console()

def fetch_docker_logs(container_name: str, tail: int) -> str | None:
    """Executes docker logs command and captures the combined stdout/stderr."""
    try:
        # We capture output as text to easily pipe it to the LLM later
        result = subprocess.run(
            ["docker", "logs", f"--tail={tail}", container_name],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Alert:[/] Failed to extract telemetry for container '{container_name}'.", style="red")
        return e.stderr
    except FileNotFoundError:
        console.print("[bold red]Critical:[/] Docker executable not found on host system.", style="red")
        return None

@click.command(name="logs")
@click.argument("service_name", type=str)
@click.option("--tail", default=50, type=int, help="Limit output to the last N lines to conserve memory.")
def logs_command(service_name: str, tail: int) -> None:
    """Retrieves recent telemetry logs for a specified service node."""
    compose_path = find_docker_compose()
    
    if not compose_path:
        console.print("[bold red]Error:[/] Target sector missing. No docker-compose.yml found.")
        return

    # Map the requested service name to the actual container name
    compose_data = load_compose_file(compose_path)
    services = extract_services(compose_data)
    
    container_name = None
    for svc in services:
        if svc["name"] == service_name:
            # Fallback to the service name if container_name isn't explicitly set in yaml
            container_name = svc["container_name"] if svc["container_name"] != "N/A" else svc["name"]
            break
            
    if not container_name:
        console.print(f"[bold yellow]Warning:[/] Service node '{service_name}' not found in configuration.")
        return

    console.print(f"Opening secure channel to [cyan]{container_name}[/] (Last {tail} lines)...", style="bold green")
    
    log_data = fetch_docker_logs(container_name, tail)
    
    if log_data:
        # Wrap the logs in a neobrutalist panel for high-contrast readability
        console.print(Panel(
            Syntax(log_data, "bash", theme="ansi_dark", word_wrap=True),
            title=f"[bold]Logs: {service_name}[/]",
            border_style="cyan"
        ))
    else:
        console.print("[dim]No telemetry data returned.[/]")