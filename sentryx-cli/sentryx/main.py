import click
from rich.console import Console
from rich.table import Table
# from .utils.docker_parser import find_docker_compose, load_compose_file, extract_services

from .utils.docker_parser import find_docker_compose, load_compose_file, extract_services
from .commands.health import status_command

console = Console()

@click.group()
def cli():
    """🛡️ SentryX: Autonomous Observer & Mission Control."""
    pass

@cli.command()
def scout():
    """Scans the local environment for Docker services."""
    compose_path = find_docker_compose()
    
    if not compose_path:
        console.print("[bold red]Alert:[/] Could not locate docker-compose.yml.", style="red")
        return

    console.print(f"Scanning sector: [cyan]{compose_path.parent}[/]...", style="bold green")
    
    compose_data = load_compose_file(compose_path)
    services = extract_services(compose_data)
    
    if not services:
        console.print("[yellow]No services found in configuration.[/]")
        return

    # Render a high-contrast terminal table
    table = Table(title="📡 SentryX Scout: Detected Services", show_header=True, header_style="bold magenta")
    table.add_column("Service Node", style="cyan", no_wrap=True)
    table.add_column("Container ID", style="green")
    table.add_column("Uplink (Ports)", style="yellow")
    
    for svc in services:
        table.add_row(svc["name"], svc["container_name"], svc["ports"])
        
    console.print(table)
    console.print("\n[bold green]SentryX Core:[/] Standing by for logs.")

# Register the new status command
cli.add_command(status_command, name="status")

if __name__ == '__main__':
    cli()