# 🚀 The Oops Fixed It - Cloud Machine ☁️

## 🔍 Overview
`find_the_oopsies.py` scans Google Cloud Platform (GCP) for:  
✅ Publicly accessible storage buckets  
✅ Firewall rules that expose SSH (port 22) to the internet  

## 🚨 Why?
This script helps prevent common **security misconfigurations** in GCP, ensuring that your cloud environment stays **secure**.  

## 📦 Requirements
- Python 3.x
- Google Cloud SDK installed and authenticated

## 🔧 Installation & Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/YOUR_USERNAME/The-Oops-Fixed-It-Cloud-Machine.git
   cd The-Oops-Fixed-It-Cloud-Machine```

2. Install dependencies
```sh
pip install -r requirements.txt
```
3. Authenticate with Google Cloud
```
gcloud auth application-default login

```
4. Run the script:
```
python find_the_oopsies.py
```

