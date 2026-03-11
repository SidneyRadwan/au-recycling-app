terraform {
  required_version = ">= 1.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # TODO: Configure remote state backend, e.g.:
  # backend "gcs" {
  #   bucket = "your-terraform-state-bucket"
  #   prefix = "au-recycling/state"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ---------------------------------------------------------------------------
# Cloud SQL — PostgreSQL with pgvector extension
# ---------------------------------------------------------------------------
resource "google_sql_database_instance" "main" {
  name             = "recycling-db"
  database_version = "POSTGRES_16"
  region           = var.region

  settings {
    tier              = "db-g1-small" # TODO: scale up for production
    availability_type = "ZONAL"       # TODO: use REGIONAL for HA in production

    backup_configuration {
      enabled = true
      # TODO: configure point-in-time recovery and backup window
    }

    ip_configuration {
      # TODO: set to false and use private IP + VPC connector for production
      ipv4_enabled = true

      # TODO: restrict authorized networks to known CIDR ranges
      # authorized_networks {
      #   value = "0.0.0.0/0"
      # }
    }
  }

  deletion_protection = true # Set to false to allow `terraform destroy`
}

resource "google_sql_database" "recycling" {
  name     = "recycling"
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "recycling" {
  name     = "recycling"
  instance = google_sql_database_instance.main.name
  password = var.database_password # TODO: use Secret Manager reference instead
}

# ---------------------------------------------------------------------------
# Cloud Run — Backend (Spring Boot)
# ---------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "backend" {
  name     = "recycling-backend"
  location = var.region

  template {
    containers {
      # TODO: replace with your actual container image URI
      # e.g. australia-southeast1-docker.pkg.dev/<project>/recycling/backend:latest
      image = "gcr.io/${var.project_id}/recycling-backend:latest"

      ports {
        container_port = 8080
      }

      env {
        name  = "DATABASE_URL"
        value = var.database_url
      }
      env {
        name  = "DATABASE_USERNAME"
        value = "recycling"
      }
      env {
        name  = "DATABASE_PASSWORD"
        value = var.database_password
        # TODO: replace with Secret Manager secret version reference:
        # value_source {
        #   secret_key_ref {
        #     secret  = google_secret_manager_secret.db_password.secret_id
        #     version = "latest"
        #   }
        # }
      }
      env {
        name  = "ANTHROPIC_API_KEY"
        value = var.anthropic_api_key
        # TODO: replace with Secret Manager secret version reference
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
          memory = "512Mi"
        }
      }
    }

    # TODO: configure VPC connector for private Cloud SQL access
    # vpc_access {
    #   connector = google_vpc_access_connector.connector.id
    #   egress    = "PRIVATE_RANGES_ONLY"
    # }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# Allow unauthenticated access to the backend Cloud Run service
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
    containers {
      # TODO: replace with your actual container image URI
      # e.g. australia-southeast1-docker.pkg.dev/<project>/recycling/frontend:latest
      image = "gcr.io/${var.project_id}/recycling-frontend:latest"

      ports {
        container_port = 3000
      }

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = "https://${google_cloud_run_v2_service.backend.uri}"
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# Allow unauthenticated access to the frontend Cloud Run service
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

  # TODO: delegate NS records at your domain registrar to the name servers
  # returned by this resource (google_dns_managed_zone.recycling.name_servers)
}

resource "google_dns_record_set" "frontend" {
  name         = "${var.frontend_domain}."
  type         = "CNAME"
  ttl          = 300
  managed_zone = google_dns_managed_zone.recycling.name

  # TODO: replace with the actual Cloud Run custom domain mapping CNAME target
  # after running: gcloud beta run domain-mappings create --service recycling-frontend ...
  rrdatas = ["ghs.googlehosted.com."]
}

resource "google_dns_record_set" "backend_api" {
  name         = "api.${var.dns_zone_name}."
  type         = "CNAME"
  ttl          = 300
  managed_zone = google_dns_managed_zone.recycling.name

  # TODO: replace with the actual Cloud Run custom domain mapping CNAME target
  rrdatas = ["ghs.googlehosted.com."]
}
