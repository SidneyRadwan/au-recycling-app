variable "project_id" {
  description = "The GCP project ID where all resources will be deployed."
  type        = string
}

variable "region" {
  description = "The GCP region for all resources. Defaults to Sydney for Australian data residency."
  type        = string
  default     = "australia-southeast1"
}


variable "github_repo" {
  description = "GitHub repository in 'owner/repo' format, used to scope Workload Identity Federation (e.g. 'SidneyRadwan/au-recycling-app')."
  type        = string
}

variable "dns_zone_name" {
  description = "The DNS zone name (e.g. 'australiarecycling.com.au'). Used to create the Cloud DNS managed zone and DNS records."
  type        = string
  default     = "australiarecycling.com.au"
}

variable "frontend_domain" {
  description = "The fully-qualified domain name for the frontend (e.g. 'australiarecycling.com.au')."
  type        = string
  default     = "australiarecycling.com.au"
}
