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
# Cloud Run — Backend (Spring Boot)
# ---------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "backend" {
  name     = "recycling-backend"
  location = var.region

  template {
    service_account = google_service_account.cloud_run.email

    vpc_access {
      connector = google_vpc_access_connector.connector.id
      egress    = "PRIVATE_RANGES_ONLY"
    }

    containers {
      image = "${local.registry}/backend:${var.backend_image}"

      ports {
        container_port = 8080
      }

      env {
        name  = "DATABASE_URL"
        value = "jdbc:postgresql:///${google_sql_database.recycling.name}?cloudSqlInstance=${google_sql_database_instance.main.connection_name}&socketFactory=com.google.cloud.sql.postgres.SocketFactory&user=${google_sql_user.recycling.name}"
      }
      env {
        name  = "DATABASE_USERNAME"
        value = google_sql_user.recycling.name
      }
      env {
        name = "DATABASE_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_password.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "ANTHROPIC_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.anthropic_api_key.secret_id
            version = "latest"
          }
        }
      }
      env {
        name  = "SPRING_PROFILES_ACTIVE"
        value = "prod"
      }
      env {
        name  = "CORS_ALLOWED_ORIGINS"
        value = "https://${var.frontend_domain}"
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
      }

      startup_probe {
        http_get {
          path = "/actuator/health"
          port = 8080
        }
        initial_delay_seconds = 10
        period_seconds        = 10
        failure_threshold     = 12
        timeout_seconds       = 5
      }

      liveness_probe {
        http_get {
          path = "/actuator/health"
          port = 8080
        }
        period_seconds    = 30
        failure_threshold = 3
        timeout_seconds   = 5
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service_iam_member" "backend_public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ---------------------------------------------------------------------------
# Cloud Run — Frontend (Next.js)
# ---------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "frontend" {
  name     = "recycling-frontend"
  location = var.region

  template {
    service_account = google_service_account.cloud_run.email

    containers {
      image = "${local.registry}/frontend:${var.frontend_image}"

      ports {
        container_port = 3000
      }

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = "https://api.${var.dns_zone_name}"
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      liveness_probe {
        http_get {
          path = "/"
          port = 3000
        }
        period_seconds    = 30
        failure_threshold = 3
        timeout_seconds   = 5
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ---------------------------------------------------------------------------
# DNS — Managed Zone and Records
# ---------------------------------------------------------------------------
resource "google_dns_managed_zone" "recycling" {
  name        = "recycling-zone"
  dns_name    = "${var.dns_zone_name}."
  description = "Managed DNS zone for Australia Recycling"
}

resource "google_dns_record_set" "frontend" {
  name         = "${var.frontend_domain}."
  type         = "CNAME"
  ttl          = 300
  managed_zone = google_dns_managed_zone.recycling.name
  # Update after: gcloud beta run domain-mappings create --service recycling-frontend
  rrdatas = ["ghs.googlehosted.com."]
}

resource "google_dns_record_set" "backend_api" {
  name         = "api.${var.dns_zone_name}."
  type         = "CNAME"
  ttl          = 300
  managed_zone = google_dns_managed_zone.recycling.name
  # Update after: gcloud beta run domain-mappings create --service recycling-backend
  rrdatas = ["ghs.googlehosted.com."]
}
