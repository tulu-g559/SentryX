import yaml
from pathlib import Path

def find_docker_compose() -> Path | None:
    """Locates docker-compose.yml in the current or parent directory."""
    cwd = Path.cwd()
    
    # Check current directory
    compose_path = cwd / "docker-compose.yml"
    if compose_path.exists():
        return compose_path
        
    # Check parent directory (useful if running from inside sentryx-cli folder)
    parent_compose = cwd.parent / "docker-compose.yml"
    if parent_compose.exists():
        return parent_compose
        
    return None

def load_compose_file(file_path: Path) -> dict:
    """Safely loads the docker-compose YAML file."""
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return {}

def extract_services(compose_data: dict) -> list[dict]:
    """Extracts service names, container names, and exposed ports."""
    services = compose_data.get("services", {})
    extracted = []
    
    for name, config in services.items():
        ports = config.get("ports", [])
        port_str = ", ".join(ports) if ports else "Internal Only"
        
        extracted.append({
            "name": name,
            "container_name": config.get("container_name", "N/A"),
            "ports": port_str
        })
    return extracted