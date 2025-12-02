#--------------------------------------------------------------
# Dev Environment - Backend Configuration (Placeholder)
#--------------------------------------------------------------

# Local backend for development/testing
# Replace with remote backend (S3, Azure, GCS, Terraform Cloud) for production use

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

# Example: S3 Backend (uncomment and configure when ready)
# terraform {
#   backend "s3" {
#     bucket         = "morpheus-lab-tfstate"
#     key            = "dev/terraform.tfstate"
#     region         = "us-east-1"
#     encrypt        = true
#     dynamodb_table = "terraform-locks"
#   }
# }

# Example: Terraform Cloud Backend (uncomment and configure when ready)
# terraform {
#   cloud {
#     organization = "your-org"
#     workspaces {
#       name = "morpheus-lab-dev"
#     }
#   }
# }
