terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0" # or "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
}
