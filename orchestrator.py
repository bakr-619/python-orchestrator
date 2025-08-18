import yaml
import paramiko
import requests
import datetime
import os
from typing import Dict, List

def load_config(file_path: str) -> Dict:
    """Load configuration from YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_health(client: paramiko.SSHClient, service: Dict) -> bool:
    """Check service health via SSH."""
    stdin, stdout, stderr = client.exec_command(f"curl -s {service['health_check_path']}")
    output = stdout.read().decode().strip()
    return "healthy" in output.lower()

def restart_service(client: paramiko.SSHClient, service_name: str) -> None:
    """Restart the service via SSH."""
    client.exec_command(f"sudo systemctl restart {service_name}")

def log_results(server: Dict, service: Dict, status: str, timestamp: str) -> None:
    """Log results to a file."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "orchestrator.log")
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - {server['hostname']} - {service['name']} - {status}\n")

def send_notification(service: Dict, status: str) -> None:
    """Send API notification to Slack (example webhook)."""
    webhook_url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
    payload = {
        "text": f"Service {service['name']} on {service['hostname']} is {status}. "
                f"Health check: {service['health_check_path']}"
    }
    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f"Failed to send notification: {e}")

def orchestrate(config_file: str) -> None:
    """Main orchestration logic."""
    config = load_config(config_file)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for server in config.get('servers', []):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(server['ip'], username='ubuntu', password=server['password'])
            for service in server.get('services', []):
                if check_health(client, service):
                    status = "healthy"
                else:
                    status = "unhealthy"
                    restart_service(client, service['name'])
                    status = "restarted"
                log_results(server, service, status, timestamp)
                send_notification(service, status)
        except Exception as e:
            log_results(server, {'name': 'connection'}, f"failed - {str(e)}", timestamp)
        finally:
            client.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python orchestrator.py <config_file>")
        sys.exit(1)
    orchestrate(sys.argv[1])