#--------------------------------------------------------------
# Prod Environment - Backend Configuration (Placeholder)
#--------------------------------------------------------------

# Local backend for development/testing
# Replace with remote backend for production use

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

# Example: S3 Backend (uncomment and configure when ready)
# terraform {
#   backend "s3" {
#     bucket         = "morpheus-lab-tfstate"
#     key            = "prod/terraform.tfstate"
#     region         = "us-east-1"
#     encrypt        = true
#     dynamodb_table = "terraform-locks"
#   }
# }
