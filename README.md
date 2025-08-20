#  Python Remote Infra Orchestrator
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Paramiko](https://img.shields.io/badge/Paramiko-green.svg)](http://www.paramiko.org/)
[![YAML](https://img.shields.io/badge/YAML-black.svg)](https://yaml.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool that automates health checks and restarts for services on remote servers. It uses a centralized YAML configuration, logs results, and sends notifications.

---

##  Features
* **Configurable**: Manages servers and services via a central YAML file.
* **Automated Checks**: Performs SSH health checks using `curl`.
* **Service Restart**: Automatically restarts unhealthy services to ensure availability.
* **Comprehensive Logging**: Logs all activity and errors to a local file.
* **API Notifications**: Sends real-time alerts to communication platforms like Slack or Discord.
* **Secure**: Connects securely via SSH with `paramiko`.

---

##  Setup Guide
* **Prerequisites**: Python 3.8+ and SSH key-based access to your servers.
1.  **Clone Repo**:
    ```bash
    git clone [https://github.com/Bakr-619/python-orchestrator.git](https://github.com/Bakr-619/python-orchestrator.git)
    cd python-orchestrator
    ```
2.  **Set up environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Create a `requirements.txt` with `paramiko`, `PyYAML`, and `requests`)*.

---

## 📝 Usage
1.  **Configure**: Create a `config.yml` file to define your servers and services.

    ```yaml
    servers:
      - hostname: web-server-1
        ip: 10.0.0.1
        user: ubuntu
        private_key: ~/.ssh/id_rsa
        services:
          - name: nginx-proxy
            health_check_path: /status
            restart_cmd: sudo systemctl restart nginx
    ```

2.  **Run**:
    ```bash
    python3 orchestrator.py config.yml --webhook "YOUR_SLACK_OR_DISCORD_WEBHOOK_URL"
    ```

---

## 🤝 Contribution
Contributions are welcome! Please open a pull request or an issue.

