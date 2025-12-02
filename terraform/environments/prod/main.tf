#--------------------------------------------------------------
# Prod Environment - Main Configuration
#--------------------------------------------------------------

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    vsphere = {
      source  = "hashicorp/vsphere"
      version = ">= 2.0.0"
    }
  }
}

#--------------------------------------------------------------
# vSphere Provider Configuration
#--------------------------------------------------------------

provider "vsphere" {
  user                 = var.vsphere_user
  password             = var.vsphere_password
  vsphere_server       = var.vsphere_server
  allow_unverified_ssl = false  # Enforce SSL verification in production
}

#--------------------------------------------------------------
# Module Calls - Prod VMs
#--------------------------------------------------------------

module "web_server" {
  source = "../../modules/vmware-vm"

  vm_name            = "${var.environment}-web-01"
  cpu_count          = var.vm_cpu_count
  memory_mb          = var.vm_memory_mb
  disk_size_gb       = var.vm_disk_size_gb
  environment        = var.environment

  vsphere_datacenter = var.vsphere_datacenter
  vsphere_cluster    = var.vsphere_cluster
  vsphere_datastore  = var.vsphere_datastore
  vsphere_network    = var.vsphere_network
  vsphere_template   = var.vsphere_template
  vsphere_folder     = var.vsphere_folder

  tags = {
    Environment = var.environment
    Project     = "morpheus-lab"
    Owner       = "DevOps"
    ManagedBy   = "Terraform"
    CostCenter  = "Production"
  }
}

module "app_server" {
  source = "../../modules/vmware-vm"

  vm_name            = "${var.environment}-app-01"
  cpu_count          = var.vm_cpu_count
  memory_mb          = var.vm_memory_mb
  disk_size_gb       = var.vm_disk_size_gb
  environment        = var.environment

  vsphere_datacenter = var.vsphere_datacenter
  vsphere_cluster    = var.vsphere_cluster
  vsphere_datastore  = var.vsphere_datastore
  vsphere_network    = var.vsphere_network
  vsphere_template   = var.vsphere_template
  vsphere_folder     = var.vsphere_folder

  tags = {
    Environment = var.environment
    Project     = "morpheus-lab"
    Owner       = "DevOps"
    ManagedBy   = "Terraform"
    CostCenter  = "Production"
  }
}
