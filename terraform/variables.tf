variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
  default     = "PROJECT ID" # Added a default value
}

variable "insecure_buckets" {
  description = "List of insecure bucket names"
  type        = list(string)
  default     = ["BUCKET NAME"] # Added a default value
}
