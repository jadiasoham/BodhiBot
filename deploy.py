"""
This script is meant for deploying the chatbot service "BodhiBot".

Deployment Modes:
- Interactive:   python3 -m deploy <app-name>
- Non-Interactive: python3 -m deploy <app-name> --no-prompts
Options:
- --no-env-overwrite   Use existing .env without generating a new one.
- --dry-run            Simulate without executing Docker commands.
- -h / --help          Show this help message.
"""

import argparse
import os, sys
from pathlib import Path
import subprocess
from subprocess import CalledProcessError, PIPE
from datetime import datetime

def get_input(prompt, default):
    val = input(f"{prompt} [{default}]: ").strip()
    return val or default

def log_message(message, level="info", logfile="deployment_logs.log"):
    levels = {
        "info": "\033[94m[INFO]",
        "warn": "\033[93m[WARN]",
        "error": "\033[91m[ERROR]",
        "success": "\033[92m[SUCCESS]"
    }
    tag = levels.get(level.lower(), "[INFO]")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"{timestamp} {tag} {message}\033[0m"
    with open(logfile, "a") as f:
        f.write(f"{timestamp} [{level.upper()}] {message}\n")
    print(msg)

def get_defaults(app_name):
    return {
        "db_user": "postgres",
        "db_password": "postgres",
        "db_name": f"{app_name}_postgres",
        "backend_port": "8000",
        "celery_pool": "solo",
        "container_prefix": app_name,
        "auth_mode": "internal",
    }

def get_configs(defaults, *, interactive=True, args=None):
    if interactive:
        return {k: get_input(f"Enter {k.replace('_', ' ').capitalize()}", v) for k, v in defaults.items()}
    if not args:
        raise ValueError("args cannot be None if interactive is False")
    return {k: getattr(args, k, defaults[k]) or defaults[k] for k in defaults}

def parse_args(defaults):
    parser = argparse.ArgumentParser(description="Deploy your app with custom env vars and Docker setup.")

    parser.add_argument("-np", "--no-prompts", dest="no_prompts", action="store_true", help="Run in non-interactive mode.")
    parser.add_argument("--no-env-overwrite", action="store_true", help="Do not overwrite existing .env file.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the deployment without actually executing.")
    parser.add_argument("app_name", nargs="?", default="bodhibot", help="Application name (used as container prefix).")

    for key, default_val in defaults.items():
        parser.add_argument(f"--{key.replace('_', '-')}", dest=key, default=None, help=f"Set '{key}' (default: {default_val})")

    return parser.parse_args()

def write_env_file(config, env_path):
    env_lines = [
        f"POSTGRES_USER={config['db_user']}",
        f"POSTGRES_PASSWORD={config['db_password']}",
        f"POSTGRES_DB={config['db_name']}",
        f"BACKEND_PORT={config['backend_port']}",
        f"CELERY_POOL={config['celery_pool']}",
        f"CONTAINER_PREFIX={config['container_prefix']}",
        f"AUTH_MODE={config['auth_mode']}",
    ]
    env_path.write_text("\n".join(env_lines) + "\n")
    os.chmod(env_path, 0o600)

def run_command(command, dry_run=False):
    log_message(f"Executing: {' '.join(command)}")
    if dry_run:
        log_message("Dry-run mode: command not executed", level="warn")
        return 0

    try:
        result = subprocess.run(command, stdout=PIPE, stderr=PIPE, check=True)
        log_message(result.stdout.decode(), level="success")
        return 0
    except CalledProcessError as e:
        log_message(e.stderr.decode(), level="error")
        return 1

def cleanup():
    if os.path.exists(".env"):
        os.remove(".env")
        log_message("Cleaned up .env file", level="warn")

if __name__ == "__main__":
    log_message("======== STARTING DEPLOYMENT PROCESS ========")

    defaults = get_defaults(app_name="bodhibot")  # Will be overridden below if user passes app_name
    args = parse_args(defaults)

    app_name = args.app_name
    defaults = get_defaults(app_name)
    interactive = not args.no_prompts

    log_message(f"Deployment mode: {'Non-interactive' if not interactive else 'Interactive'}")
    configs = get_configs(defaults, interactive=interactive, args=args)

    env_path = Path(".env")

    if args.no_env_overwrite and env_path.exists():
        log_message(".env file exists. Skipping overwrite due to flag --no-env-overwrite", level="warn")
    else:
        log_message("Writing .env configuration...")
        write_env_file(configs, env_path)

    if args.dry_run:
        log_message("Dry-run mode active. No actual deployment will occur.", level="warn")

    log_message("Initializing Docker Swarm...")
    if run_command(["docker", "swarm", "init"], dry_run=args.dry_run):
        log_message("Swarm init failed. Aborting...", level="error")
        sys.exit(1)

    log_message(f"Deploying stack for app: {app_name}")
    if run_command(["docker", "stack", "deploy", "-c", "docker-compose.yml", app_name], dry_run=args.dry_run):
        log_message("Stack deployment failed. Aborting...", level="error")
        sys.exit(1)

    log_message("======== DEPLOYMENT COMPLETED SUCCESSFULLY ========", level="success")
