variable "project_id" {
  description = "The GCP project ID where all resources will be deployed."
  type        = string
}

variable "region" {
  description = "The GCP region for all resources. Defaults to Sydney for Australian data residency."
  type        = string
  default     = "australia-southeast1"
}

variable "database_url" {
  description = "JDBC connection URL for the Cloud SQL PostgreSQL instance (used by the backend service). Format: jdbc:postgresql://<host>:5432/recycling"
  type        = string
}

variable "database_password" {
  description = "Password for the recycling database user. Use Secret Manager in production."
  type        = string
  sensitive   = true
}

variable "anthropic_api_key" {
  description = "API key for Anthropic Claude — used by the backend for AI-powered recycling guidance."
  type        = string
  sensitive   = true
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
