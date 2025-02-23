# The Oops Fixed It Cloud Machine

## 📌 Overview
This project automates security checks in **Google Cloud (GCP)** to detect common misconfigurations.

### 🔍 Features:
✅ Check for **publicly exposed** cloud storage buckets  
✅ Audit IAM roles & permissions  
✅ Detect misconfigured **firewall rules (open SSH)**  

---

## 🚀 Getting Started
### 1️⃣ **Prerequisites**
- **Google Cloud SDK** installed ([Install Guide](https://cloud.google.com/sdk/docs/install))
- **Python 3.x** installed
- A Google Cloud **project** with `Owner` or `Editor` permissions

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

---

## ▶️ Running the Script
To execute the script and check for security misconfigurations:
```sh
python find_the_oopsies.py
```

If everything is set up correctly, it will scan your GCP project for:
- Publicly accessible storage buckets
- Open SSH firewall rules

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

🎭 Final Thoughts

"With great cloud power comes great misconfiguration responsibility." Use this tool wisely! 😉
