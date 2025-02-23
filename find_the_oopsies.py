from google.cloud import storage
from googleapiclient import discovery
import google.auth

# Set your GCP Project ID
PROJECT_ID = "cloudsec-automation"  # Replace with your actual project ID

def check_public_buckets():
    """
    Scans all buckets in the GCP project and detects publicly accessible ones.
    """
    client = storage.Client(project=PROJECT_ID)  # Explicitly set the project
    buckets = client.list_buckets()
    
    print("\n🔍 Checking for publicly accessible buckets...\n")
    
    for bucket in buckets:
        bucket_name = bucket.name
        policy = bucket.get_iam_policy(requested_policy_version=3)
        
        for binding in policy.bindings:
            role = binding["role"]
            members = binding["members"]

            # Check if any public access exists
            if "allUsers" in members or "allAuthenticatedUsers" in members:
                print(f"⚠️ WARNING: Bucket '{bucket_name}' is public!")
                print(f"   Role: {role}")
                print(f"   Public Access: {members}\n")
                break  # No need to continue once public access is detected
    
    print("✅ Bucket scan complete.\n")

def check_firewall_rules():
    """
    Scans firewall rules for misconfigurations, such as open SSH access (port 22) from anywhere.
    """
    # Authenticate and set project
    credentials, _ = google.auth.default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    
    # Retrieve all firewall rules for the project
    request = service.firewalls().list(project=PROJECT_ID)
    response = request.execute()
    
    print("\n🔍 Checking for misconfigured firewall rules...\n")
    
    for firewall in response.get('items', []):
        rule_name = firewall.get('name', 'Unnamed Rule')
        allowed = firewall.get('allowed', [])
        source_ranges = firewall.get('sourceRanges', [])
        
        for allow in allowed:
            if allow.get('IPProtocol', '').lower() == 'tcp':
                ports = allow.get('ports', [])
                for port in ports:
                    if '-' in port:
                        start, end = port.split('-')
                        if int(start) <= 22 <= int(end) and "0.0.0.0/0" in source_ranges:
                            print(f"⚠️ WARNING: Firewall rule '{rule_name}' allows SSH (port 22) from anywhere!")
                    else:
                        if int(port) == 22 and "0.0.0.0/0" in source_ranges:
                            print(f"⚠️ WARNING: Firewall rule '{rule_name}' allows SSH (port 22) from anywhere!")
    
    print("✅ Firewall rule scan complete.\n")

if __name__ == "__main__":
    check_public_buckets()
    check_firewall_rules()
