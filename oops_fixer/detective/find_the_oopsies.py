import json
import logging
import argparse
from google.cloud import storage
from googleapiclient import discovery
import google.auth
import os
import sys
import yaml
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_config(config_path="settings/config.yaml"):
    """Load and validate the config file."""
    if not os.path.exists(config_path):
        logging.error(f"Configuration file '{config_path}' is missing.")
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logging.error(f"'{config_path}' is not a valid YAML file: {e}")
        sys.exit(1)

    # Required base keys
    required_keys = ["cloud", "logging"] #changed to match config

    # Cloud-specific keys
    cloud_keys = {
        "gcp": ["project_id"], #changed to match config
        "aws": ["aws_account_id"],
        "azure": ["azure_subscription_id"]
    }

    # Validate required base keys
    for key in required_keys:
        if key not in config or not config[key]:
            logging.error(f"Missing required config key: '{key}'")
            sys.exit(1)

    # Validate cloud provider
    cloud_provider = config["cloud"]["provider"].lower() #changed to match config
    if cloud_provider not in cloud_keys:
        logging.error("Invalid 'cloud_provider'. Must be 'gcp', 'aws', or 'azure'.")
        sys.exit(1)

    # Validate cloud-specific keys
    for key in cloud_keys[cloud_provider]:
        if key not in config["cloud"] or not config["cloud"][key]: #changed to match config
            logging.error(f"Missing required key for {cloud_provider.upper()}: '{key}'")
            sys.exit(1)

    logging.info("✅ Config validation passed!")
    return config

# Load and validate config once
CONFIG = load_config()
CLOUD_PROVIDER = CONFIG["cloud"]["provider"]
OUTPUT_FILE = CONFIG["logging"]["output_file"]
PROJECT_ID = CONFIG["cloud"].get("project_id", "")

def check_public_buckets(project_id):
    """Scans all buckets in the GCP project and detects publicly accessible ones."""
    findings = {"public_buckets": []}
    try:
        client = storage.Client(project=project_id)
        buckets = client.list_buckets()
        logging.info("Checking for publicly accessible buckets...")

        for bucket in buckets:
            findings["public_buckets"].append(check_bucket_policy(bucket))

    except Exception as e:
        logging.exception(f"Error checking buckets: {e}") #log the full exception

    return findings

def check_bucket_policy(bucket):
    bucket_name = bucket.name
    policy = bucket.get_iam_policy(requested_policy_version=3)
    bucket_finding = {"name": bucket_name, "role": None, "members": []}
    for binding in policy.bindings:
        role = binding["role"]
        members = binding["members"]
        if "allUsers" in members or "allAuthenticatedUsers" in members:
            logging.warning(f"Bucket '{bucket_name}' is public!")
            bucket_finding["role"] = role
            bucket_finding["members"] = list(members)
            break
        else:
            bucket_finding["role"] = role
    return bucket_finding

def check_firewall_rules(project_id):
    """Scans firewall rules for misconfigurations, such as open SSH access."""
    findings = {"insecure_firewall_rules": []}

    try:
        credentials, _ = google.auth.default()
        service = discovery.build('compute', 'v1', credentials=credentials)
        request = service.firewalls().list(project=project_id)
        response = request.execute()
        logging.info("Checking for misconfigured firewall rules...")

        for firewall in response.get('items', []):
            rule_name = firewall.get('name', 'Unnamed Rule')
            allowed = firewall.get('allowed', [])
            source_ranges = list(firewall.get('sourceRanges', []))
            target_tags = firewall.get('targetTags', [])

            for allow in allowed:
                if allow.get('IPProtocol', '').lower() == 'tcp':
                    ports = allow.get('ports', [])

                    for port in ports:
                        if (port == "22" or ("-" in port and 22 in range(int(port.split('-')[0]), int(port.split('-')[1]) + 1))) and "0.0.0.0/0" in source_ranges:
                            logging.warning(f"Firewall rule '{rule_name}' allows SSH (port 22) from anywhere!")
                            # Explicitly convert nested lists
                            findings["insecure_firewall_rules"].append({
                                "rule": rule_name,
                                "ports": ports,
                                "source_ranges": list(source_ranges),
                                "target_tags": target_tags
                            })

    except Exception as e:
        logging.error(f"Error checking firewall rules: {e}")

    return findings

def save_findings(findings):
    """Save findings to a JSON file."""
    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(findings, f, indent=4)
        logging.info(f"Findings saved to {OUTPUT_FILE}") #Removed the json content from the log.
    except Exception as e:
        logging.error(f"Error saving findings: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cloud Security Misconfiguration Scanner")
    parser.add_argument("--project", help="Specify the GCP project ID", default=PROJECT_ID)
    args = parser.parse_args()

    if CLOUD_PROVIDER == "gcp":
        all_findings = {}
        all_findings.update(check_public_buckets(args.project))
        all_findings.update(check_firewall_rules(args.project))
        save_findings(all_findings)
    else:
        logging.error("Currently, only GCP is supported. AWS and Azure support coming soon!")
