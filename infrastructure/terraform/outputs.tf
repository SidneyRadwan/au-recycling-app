output "workload_identity_provider" {
  description = "Workload Identity Federation provider — set as GCP_WORKLOAD_IDENTITY_PROVIDER in GitHub Actions secrets."
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "cd_service_account" {
  description = "Service account email for the CD pipeline — set as GCP_SERVICE_ACCOUNT in GitHub Actions secrets."
  value       = google_service_account.cloud_run.email
}

output "artifact_registry" {
  description = "Artifact Registry base path for Docker images."
  value       = local.registry
}

output "cloud_sql_instance_connection_name" {
  description = "The connection name of the Cloud SQL instance (used with Cloud SQL Auth Proxy). Format: project:region:instance"
  value       = google_sql_database_instance.main.connection_name
}

output "dns_name_servers" {
  description = "The name servers for the Cloud DNS managed zone. Delegate these at your domain registrar."
  value       = google_dns_managed_zone.recycling.name_servers
}

output "backend_url" {
  description = "Cloud Run backend service URL."
  value       = google_cloud_run_v2_service.backend.uri
}

output "frontend_url" {
  description = "Cloud Run frontend service URL."
  value       = google_cloud_run_v2_service.frontend.uri
}
