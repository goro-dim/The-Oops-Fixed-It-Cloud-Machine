resource "google_storage_bucket_iam_binding" "remove_public_access" {
  for_each = toset(var.insecure_buckets)

  bucket = each.value
  role   = "roles/storage.objectViewer"

  members = []
}

resource "google_compute_firewall" "allow_ssh_everyone" { # change the resource name.
  name    = "allow-ssh-everyone"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["10.0.0.0/8"]
}
