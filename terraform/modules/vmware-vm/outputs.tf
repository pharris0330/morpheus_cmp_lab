#--------------------------------------------------------------
# VMware VM Module - Outputs
#--------------------------------------------------------------

output "vm_id" {
  description = "The UUID of the virtual machine"
  value       = vsphere_virtual_machine.vm.id
}

output "vm_name" {
  description = "The name of the virtual machine"
  value       = vsphere_virtual_machine.vm.name
}

output "vm_default_ip_address" {
  description = "The default IP address of the virtual machine"
  value       = vsphere_virtual_machine.vm.default_ip_address
}

output "vm_guest_ip_addresses" {
  description = "All IP addresses of the virtual machine"
  value       = vsphere_virtual_machine.vm.guest_ip_addresses
}

output "vm_moid" {
  description = "The managed object reference ID of the VM"
  value       = vsphere_virtual_machine.vm.moid
}

output "vm_cpu" {
  description = "Number of vCPUs"
  value       = vsphere_virtual_machine.vm.num_cpus
}

output "vm_memory" {
  description = "Memory in MB"
  value       = vsphere_virtual_machine.vm.memory
}