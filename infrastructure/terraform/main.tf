terraform {
  required_version = ">= 1.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    # bucket is set via -backend-config or terraform.tfbackend (never commit bucket name here)
    prefix = "au-recycling/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ---------------------------------------------------------------------------
# Artifact Registry — Docker image repository
# ---------------------------------------------------------------------------
resource "google_artifact_registry_repository" "app" {
  repository_id = "au-recycling"
  format        = "DOCKER"
  location      = var.region
  description   = "Docker images for Australia Recycling app"
}

locals {
  registry = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.app.repository_id}"
}

# ---------------------------------------------------------------------------
# Secret Manager — sensitive values
# ---------------------------------------------------------------------------
resource "google_secret_manager_secret" "db_password" {
  secret_id = "recycling-db-password"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "anthropic_api_key" {
  secret_id = "recycling-anthropic-api-key"
  replication {
    auto {}
  }
}

# ---------------------------------------------------------------------------
# Service Account — Cloud Run services identity
# ---------------------------------------------------------------------------
resource "google_service_account" "cloud_run" {
  account_id   = "recycling-cloud-run"
  display_name = "Australia Recycling Cloud Run"
}

resource "google_secret_manager_secret_iam_member" "cloud_run_db_password" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run.email}"
}

resource "google_secret_manager_secret_iam_member" "cloud_run_anthropic" {
  secret_id = google_secret_manager_secret.anthropic_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run.email}"
}

resource "google_artifact_registry_repository_iam_member" "cloud_run_reader" {
  repository = google_artifact_registry_repository.app.name
  location   = var.region
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.cloud_run.email}"
}

# ---------------------------------------------------------------------------
# Workload Identity Federation — keyless GitHub Actions auth
# ---------------------------------------------------------------------------
data "google_project" "project" {}

resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "gh-actions"
  display_name              = "GitHub Actions"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  display_name                       = "GitHub"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }

  attribute_condition = "assertion.repository == '${var.github_repo}'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Grant GitHub Actions the ability to impersonate the Cloud Run service account
resource "google_service_account_iam_member" "github_wif" {
  service_account_id = google_service_account.cloud_run.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.github_repo}"
}

# Roles needed by the CD pipeline
resource "google_project_iam_member" "cloud_run_developer" {
  project = var.project_id
  role    = "roles/run.developer"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

resource "google_project_iam_member" "artifact_registry_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

resource "google_project_iam_member" "service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

resource "google_project_iam_member" "cloud_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

# ---------------------------------------------------------------------------
# VPC Peering — required for Cloud SQL private IP
# ---------------------------------------------------------------------------
resource "google_compute_global_address" "private_ip" {
  name          = "recycling-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = "projects/${var.project_id}/global/networks/default"
}

resource "google_service_networking_connection" "private_vpc" {
  network                 = "projects/${var.project_id}/global/networks/default"
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip.name]
}

# ---------------------------------------------------------------------------
# VPC Connector — private Cloud SQL access from Cloud Run
# ---------------------------------------------------------------------------
resource "google_vpc_access_connector" "connector" {
  name          = "recycling-connector"
  region        = var.region
  ip_cidr_range = "10.8.0.0/28"
  network       = "default"
}

# ---------------------------------------------------------------------------
# Cloud SQL — PostgreSQL with pgvector extension
# ---------------------------------------------------------------------------
resource "google_sql_database_instance" "main" {
  name             = "recycling-db"
  database_version = "POSTGRES_16"
  region           = var.region

  depends_on = [google_service_networking_connection.private_vpc]

  settings {
    tier              = "db-g1-small"
    availability_type = "ZONAL"

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      backup_retention_settings {
        retained_backups = 7
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = "projects/${var.project_id}/global/networks/default"
    }
  }

  deletion_protection = true
}

resource "google_sql_database" "recycling" {
  name     = "recycling"
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "recycling" {
  name     = "recycling"
  instance = google_sql_database_instance.main.name
  password_policy {
    enable_failed_attempts_check = false
  }
}

# ---------------------------------------------------------------------------
# Cloud Run services are deployed and managed by the CD pipeline.
# See .github/workflows/deploy.yml — gcloud run deploy creates/updates them.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# DNS — Managed Zone and Records
# ---------------------------------------------------------------------------
resource "google_dns_managed_zone" "recycling" {
  name        = "recycling-zone"
  dns_name    = "${var.dns_zone_name}."
  description = "Managed DNS zone for Australia Recycling"
}

# Note: apex domain A records are added after Cloud Run domain mapping.
# The mapping provides IP addresses: gcloud beta run domain-mappings create ...

resource "google_dns_record_set" "backend_api" {
  name         = "api.${var.dns_zone_name}."
  type         = "CNAME"
  ttl          = 300
  managed_zone = google_dns_managed_zone.recycling.name
  # Update after: gcloud beta run domain-mappings create --service recycling-backend
  rrdatas = ["ghs.googlehosted.com."]
}
