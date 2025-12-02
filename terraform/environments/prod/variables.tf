#--------------------------------------------------------------
# Prod Environment - Variable Definitions
#--------------------------------------------------------------

# vSphere Connection
variable "vsphere_server" {
  description = "vSphere server address"
  type        = string
}

variable "vsphere_user" {
  description = "vSphere username"
  type        = string
}

variable "vsphere_password" {
  description = "vSphere password"
  type        = string
  sensitive   = true
}

# vSphere Infrastructure
variable "vsphere_datacenter" {
  description = "vSphere Datacenter name"
  type        = string
}

variable "vsphere_cluster" {
  description = "vSphere Cluster name"
  type        = string
}

variable "vsphere_datastore" {
  description = "vSphere Datastore name"
  type        = string
}

variable "vsphere_network" {
  description = "vSphere Network name"
  type        = string
}

variable "vsphere_template" {
  description = "VM template to clone"
  type        = string
}

variable "vsphere_folder" {
  description = "vSphere folder for VMs"
  type        = string
  default     = ""
}

# VM Configuration
variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vm_cpu_count" {
  description = "Number of vCPUs per VM"
  type        = number
  default     = 4
}

variable "vm_memory_mb" {
  description = "Memory in MB per VM"
  type        = number
  default     = 8192
}

variable "vm_disk_size_gb" {
  description = "Disk size in GB per VM"
  type        = number
  default     = 100
}
