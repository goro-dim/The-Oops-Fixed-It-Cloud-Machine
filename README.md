
# The 'Oops Fixed It' Cloud Machine

## 📌 Overview

This project automates security checks in **Google Cloud (GCP)** to detect common misconfigurations, now with enhanced configuration and a foundation for future automated fixes.

### 🔍 Features:

✅ Check for **publicly exposed** cloud storage buckets  
✅ Detect misconfigured **firewall rules (open SSH)** ✅ **Configurable** project and logging settings  
✅ **JSON output** for easy parsing and automation  
✅ Foundation for **Terraform integration** for automated fixes (coming soon!)

---

## 🚀 Getting Started

### 1️⃣ **Prerequisites**

- **Google Cloud SDK** installed ([Install Guide](https://cloud.google.com/sdk/docs/install))
- **Python 3.x** installed
- A Google Cloud **project** with `Owner` or `Editor` permissions
- **Terraform** installed (for future automated fixes)

### 2️⃣ **Authentication Setup**

Run the following commands to authenticate:

```sh
# Log in to Google Cloud
gcloud auth login

# Set your project (replace PROJECT_ID with your project ID)
gcloud config set project PROJECT_ID

# Authenticate application default credentials (for Python scripts)
gcloud auth application-default login
```

### 3️⃣ **Configuration Setup**

1.  Create a `config.json` file in the same directory as the script.
2.  Populate it with your settings:

    ```json
    {
        "cloud_provider": "gcp",
        "project_id": "YOUR_PROJECT_ID",
        "aws_account_id": "123456789012", 
        "azure_subscription_id": "your-azure-subscription-id",
        "log_level": "INFO", 
        "output_file": "oopsie_findings.json"
    }
    ```

    * Replace `YOUR_PROJECT_ID` with your actual GCP project ID.
    * AWS id and Azure id are here for future updates for complate multicloud integration. Currently the tool is working only with GCP
    * Adjust `log_level` as needed. 
    Available Log Levels:
         *  DEBUG: Detailed information, typically used for diagnosing problems.
         *  INFO: General information about the script's execution.
         *  WARNING: Indicates potential issues or unexpected events.
         *  ERROR: Signals that an error has occurred, but the script may continue.
         *  CRITICAL: A severe error that may cause the script to terminate.

---

## ▶️ Running the Script

To execute the script and check for security misconfigurations:

```sh
python find_the_oopsies.py
```

Or, to override the project ID from the command line:

```sh
python find_the_oopsies.py --project YOUR_PROJECT_ID
```

The script will:

-   Scan your GCP project for public buckets and open SSH firewall rules.
-   Save the findings to `oopsie_findings.json`.

---

## 🛠️ Useful GCloud Commands

### **Storage Buckets**

**Make a bucket public:**

```sh
gcloud storage buckets add-iam-policy-binding gs://YOUR_BUCKET_NAME \
    --member="allUsers" --role="roles/storage.objectViewer"
```

**Make a bucket private:**

```sh
gcloud storage buckets remove-iam-policy-binding gs://YOUR_BUCKET_NAME \
    --member="allUsers" --role="roles/storage.objectViewer"
```

### **Firewall Rules** (SSH Access)

**Open SSH (Port 22) to the internet:**

```sh
gcloud compute firewall-rules create allow-ssh-everyone \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:22 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=allow-ssh
```

**Close SSH (Port 22) to the internet:**

```sh
gcloud compute firewall-rules delete allow-ssh-everyone
```

---

## ⚠️ Security Warning

These commands **open your cloud resources to the public** for testing purposes. Always revert changes after testing to keep your cloud environment secure.

---

## 🚀 What's Next?

We're gearing up to integrate **Terraform**! This will enable automated fixes for the security misconfigurations detected by the script. Stay tuned for updates!

---

🎭 Final Thoughts

"With great cloud power comes great misconfiguration responsibility." Use this tool wisely! 😉
