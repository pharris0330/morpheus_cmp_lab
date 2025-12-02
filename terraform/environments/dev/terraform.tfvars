#--------------------------------------------------------------
# Dev Environment - Variable Values
#--------------------------------------------------------------

# Environment
environment = "dev"

# vSphere Connection (update with your values)
vsphere_server = "vcenter.lab.local"
vsphere_user   = "administrator@vsphere.local"
# vsphere_password = "set via TF_VAR_vsphere_password or prompt"

# vSphere Infrastructure (update with your values)
vsphere_datacenter = "Datacenter"
vsphere_cluster    = "Cluster"
vsphere_datastore  = "datastore1"
vsphere_network    = "VM Network"
vsphere_template   = "ubuntu-22.04-template"
vsphere_folder     = "Development"

# VM Sizing - Dev (smaller resources)
vm_cpu_count   = 2
vm_memory_mb   = 2048
vm_disk_size_gb = 40
