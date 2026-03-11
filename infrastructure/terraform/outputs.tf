output "backend_service_url" {
  description = "The URL of the backend Cloud Run service."
  value       = google_cloud_run_v2_service.backend.uri
}

output "frontend_service_url" {
  description = "The URL of the frontend Cloud Run service."
  value       = google_cloud_run_v2_service.frontend.uri
}

output "cloud_sql_instance_connection_name" {
  description = "The connection name of the Cloud SQL instance (used with Cloud SQL Auth Proxy). Format: project:region:instance"
  value       = google_sql_database_instance.main.connection_name
}

output "cloud_sql_public_ip" {
  description = "The public IP address of the Cloud SQL instance. Restrict access via authorized_networks in production."
  value       = google_sql_database_instance.main.public_ip_address
}

output "dns_name_servers" {
  description = "The name servers for the Cloud DNS managed zone. Delegate these at your domain registrar."
  value       = google_dns_managed_zone.recycling.name_servers
}
