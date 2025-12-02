#--------------------------------------------------------------
# Prod Environment - Variable Values
#--------------------------------------------------------------

# Environment
environment = "prod"

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
vsphere_folder     = "Production"

# VM Sizing - Prod (larger resources)
vm_cpu_count    = 4
vm_memory_mb    = 8192
vm_disk_size_gb = 100
