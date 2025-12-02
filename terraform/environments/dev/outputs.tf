#--------------------------------------------------------------
# Dev Environment - Outputs
#--------------------------------------------------------------

output "web_server_ip" {
  description = "IP address of the web server"
  value       = module.web_server.vm_default_ip_address
}

output "web_server_name" {
  description = "Name of the web server"
  value       = module.web_server.vm_name
}

output "app_server_ip" {
  description = "IP address of the app server"
  value       = module.app_server.vm_default_ip_address
}

output "app_server_name" {
  description = "Name of the app server"
  value       = module.app_server.vm_name
}

output "environment" {
  description = "Environment name"
  value       = var.environment
}
