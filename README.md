# Morpheus Automation Lab

Infrastructure automation demo showcasing Morpheus CMP integration with:
- **Terraform** - VMware VM provisioning with reusable modules
- **Ansible** - Post-provisioning configuration management
- **GitLab CI/CD** - Multi-stage pipeline with security scanning
- **ServiceNow** - CMDB sync and approval workflows

## Repository Structure
```
morpheus-automation-lab/
├── terraform/
│   ├── modules/vmware-vm/    # Reusable VM module
│   └── environments/         # Dev/Prod configurations
├── ansible/
│   ├── roles/                # base-config, web-server
│   └── playbooks/            # Orchestration playbooks
├── scripts/                  # ServiceNow integration scripts
├── docs/                     # Documentation and screenshots
└── .gitlab-ci.yml            # CI/CD pipeline
```

## Prerequisites

- Terraform >= 1.0
- Ansible >= 2.9
- Python 3.x with requests library
- GitLab account
- ServiceNow Developer Instance
- Morpheus Data trial/license

## Author

Paul Harris
