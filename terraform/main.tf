
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = "None"
  region  = "us-central1"
}


resource "google_compute_firewall" "allow_ssh_everyone" {
  name    = "allow-ssh-everyone"
  network = "default"
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  source_ranges = ["10.0.0.0/16"] # change the source ranges to a more secure value.
  target_tags = ["allow-ssh"]
}
