#--------------------------------------------------------------
# VMware VM Module - Input Variables
#--------------------------------------------------------------

variable "vm_name" {
  description = "Name of the virtual machine"
  type        = string
}

variable "cpu_count" {
  description = "Number of vCPUs"
  type        = number
  default     = 2
}

variable "memory_mb" {
  description = "Memory in MB"
  type        = number
  default     = 4096
}

variable "disk_size_gb" {
  description = "Primary disk size in GB"
  type        = number
  default     = 50
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

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
  description = "VM template to clone from"
  type        = string
}

variable "vsphere_folder" {
  description = "vSphere folder path for the VM"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags to apply to the VM"
  type        = map(string)
  default     = {}
}