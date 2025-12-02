# Morpheus CMP Automation Lab

[![Infrastructure CI/CD Pipeline](https://github.com/YOUR_USERNAME/morpheus-cmp-lab/actions/workflows/infrastructure.yml/badge.svg)](https://github.com/YOUR_USERNAME/morpheus-cmp-lab/actions/workflows/infrastructure.yml)

A comprehensive infrastructure automation lab demonstrating enterprise-grade practices for Cloud Management Platform (CMP) integration, Infrastructure as Code (IaC), and DevOps workflows.

---

## Overview

This lab showcases end-to-end automation capabilities for hybrid cloud infrastructure management, specifically designed to integrate with **Morpheus Data (HPE)** Cloud Management Platform. The project demonstrates proficiency in:

- **Infrastructure as Code** using Terraform
- **Configuration Management** using Ansible
- **CI/CD Pipelines** using GitHub Actions
- **ITSM Integration** with ServiceNow
- **Security Scanning** and compliance validation

---

## Architecture
```
┌─────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions CI/CD                         │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────────────┐ │
│  │ Validate  │→ │ Security  │→ │   Plan    │→ │ Approve → Apply   │ │
│  │           │  │   Scan    │  │           │  │                   │ │
│  └───────────┘  └───────────┘  └───────────┘  └───────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Morpheus CMP                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│  │  Instances  │  │  Workflows  │  │   Policies  │                  │
│  └─────────────┘  └─────────────┘  └─────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
         │                   │                    │
         ▼                   ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    VMware       │  │   ServiceNow    │  │    Ansible      │
│    vSphere      │  │     CMDB        │  │  Configuration  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Repository Structure
```
morpheus-cmp-lab/
├── .github/
│   └── workflows/
│       ├── infrastructure.yml    # Main CI/CD pipeline
│       ├── deploy.yml            # Deployment with approval gates
│       └── pr-check.yml          # Pull request validation
├── terraform/
│   ├── modules/
│   │   └── vmware-vm/            # Reusable VM provisioning module
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── outputs.tf
│   └── environments/
│       ├── dev/                  # Development environment
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── terraform.tfvars
│       │   ├── backend.tf
│       │   └── outputs.tf
│       └── prod/                 # Production environment
│           ├── main.tf
│           ├── variables.tf
│           ├── terraform.tfvars
│           ├── backend.tf
│           └── outputs.tf
├── ansible/
│   ├── ansible.cfg               # Ansible configuration
│   ├── roles/
│   │   ├── base-config/          # Base system configuration
│   │   │   ├── tasks/main.yml
│   │   │   ├── handlers/main.yml
│   │   │   ├── defaults/main.yml
│   │   │   └── templates/
│   │   │       ├── sshd_config.j2
│   │   │       └── motd.j2
│   │   └── web-server/           # Nginx web server deployment
│   │       ├── tasks/main.yml
│   │       ├── handlers/main.yml
│   │       ├── defaults/main.yml
│   │       └── templates/
│   │           ├── nginx.conf.j2
│   │           ├── default-site.conf.j2
│   │           └── index.html.j2
│   └── playbooks/
│       ├── site.yml              # Main orchestration playbook
│       └── inventory.example     # Example inventory file
├── scripts/
│   └── servicenow_cmdb_sync.py   # CMDB validation script
└── docs/                         # Additional documentation
```

---

## Components

### Terraform - Infrastructure as Code

**VMware VM Module** (`terraform/modules/vmware-vm/`)

Reusable module for provisioning virtual machines on VMware vSphere:

- Configurable CPU, memory, and disk sizing
- Template-based cloning
- Environment tagging
- Network configuration

**Environment Configurations** (`terraform/environments/`)

Separate configurations for dev and prod with:

- Environment-specific sizing (dev: 2 CPU/2GB, prod: 4 CPU/8GB)
- Isolated state management
- Variable inheritance from modules
```hcl
# Example module usage
module "web_server" {
  source = "../../modules/vmware-vm"

  vm_name            = "${var.environment}-web-01"
  cpu_count          = var.vm_cpu_count
  memory_mb          = var.vm_memory_mb
  environment        = var.environment
  vsphere_datacenter = var.vsphere_datacenter
  vsphere_cluster    = var.vsphere_cluster
  vsphere_template   = var.vsphere_template
}
```

---

### Ansible - Configuration Management

**Base Configuration Role** (`ansible/roles/base-config/`)

- System package installation
- SSH hardening
- Time synchronization (NTP/Chrony)
- User and group management
- Security baseline configuration

**Web Server Role** (`ansible/roles/web-server/`)

- Nginx installation and configuration
- SSL/TLS support (self-signed certificates)
- Security headers implementation
- Health check endpoints
- Firewall configuration
```yaml
# Example playbook execution
- name: Configure web servers
  hosts: webservers
  become: yes
  roles:
    - role: base-config
    - role: web-server
      vars:
        web_server_type: nginx
        enable_ssl: true
```

---

### CI/CD Pipeline - GitHub Actions

**Pipeline Stages:**

| Stage | Jobs | Purpose |
|-------|------|---------|
| **Validate** | terraform-validate-dev, terraform-validate-prod, ansible-lint | Syntax and format validation |
| **Security Scan** | tfsec-scan, checkov-scan, secrets-scan, sast-scan | Security vulnerability detection |
| **Plan** | terraform-plan-dev, terraform-plan-prod | Generate execution plans |
| **Approve** | Manual approval gate | Human review before deployment |
| **Apply** | terraform-apply, ansible-configure | Deploy and configure infrastructure |

**Security Scanning Tools:**

- **TFSec** - Terraform security scanner
- **Checkov** - Infrastructure policy compliance
- **TruffleHog** - Secrets detection
- **Bandit** - Python SAST scanning

---

### ServiceNow Integration

**CMDB Validation Script** (`scripts/servicenow_cmdb_sync.py`)

Validates that provisioned VMs are properly synchronized to ServiceNow CMDB:
```bash
# Run validation
python scripts/servicenow_cmdb_sync.py \
  --vm-name dev-web-01 \
  --environment dev \
  --expected-cpu 2 \
  --expected-memory 4096

# Demo mode (no API calls)
python scripts/servicenow_cmdb_sync.py \
  --vm-name dev-web-01 \
  --environment dev \
  --demo
```

**Features:**

- CMDB record lookup and validation
- Automated incident creation on sync failures
- Configurable validation rules
- JSON output for CI/CD integration

---

## Morpheus CMP Integration

This lab is designed to integrate with Morpheus Data (HPE) Cloud Management Platform:

**Planned Integration Points:**

| Feature | Description |
|---------|-------------|
| **Cloud Integration** | VMware vSphere cloud connection |
| **Instance Types** | Custom VM instance type definitions |
| **Workflows** | Provisioning and operational workflows |
| **Policies** | Approval, naming, and governance policies |
| **RBAC** | Role-based access control configuration |
| **ServiceNow Plugin** | CMDB sync and service catalog integration |

**Terraform Integration:**
```hcl
# Morpheus provider configuration
terraform {
  required_providers {
    morpheus = {
      source  = "gomorpheus/morpheus"
      version = ">= 0.9.0"
    }
  }
}

provider "morpheus" {
  url      = var.morpheus_url
  username = var.morpheus_username
  password = var.morpheus_password
}
```

---

## Getting Started

### Prerequisites

- Terraform >= 1.6.0
- Ansible >= 2.15
- Python >= 3.10
- Git

### Local Development
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/morpheus-cmp-lab.git
cd morpheus-cmp-lab

# Validate Terraform
cd terraform/environments/dev
terraform init -backend=false
terraform validate

# Check Ansible syntax
cd ../../../ansible
ansible-playbook --syntax-check playbooks/site.yml

# Test ServiceNow script
cd ../scripts
python servicenow_cmdb_sync.py --vm-name test-vm --environment dev --demo
```

### Environment Variables

For production use, configure the following:
```bash
# vSphere
export TF_VAR_vsphere_password="your-password"

# ServiceNow
export SNOW_INSTANCE="your-instance.service-now.com"
export SNOW_USERNAME="admin"
export SNOW_PASSWORD="your-password"
```

---

## CI/CD Workflows

### Automatic Pipeline (Push/PR)

Triggered on push to `main` or `develop` branches:

1. Validates all Terraform configurations
2. Lints Ansible playbooks
3. Runs security scans
4. Generates Terraform plans

### Manual Deployment

To deploy infrastructure:

1. Go to **Actions** → **Deploy Infrastructure**
2. Click **Run workflow**
3. Select environment (`dev` or `prod`)
4. Select action (`apply` or `destroy`)
5. For production: Approve deployment in environment protection

---

## Security Considerations

- Credentials stored in GitHub Secrets (never in code)
- Security scanning on every pipeline run
- Manual approval gates for production deployments
- SSH hardening in base configuration
- TLS/SSL support for web servers
- Secrets scanning with TruffleHog

---

## Skills Demonstrated

| Skill | Implementation |
|-------|----------------|
| Cloud Management Platform | Morpheus integration architecture |
| Infrastructure as Code | Terraform modules and environments |
| Configuration Management | Ansible roles with Jinja2 templates |
| CI/CD Pipelines | GitHub Actions multi-stage workflow |
| ITSM Integration | ServiceNow CMDB validation |
| VMware vSphere | VM provisioning via Terraform |
| Security Automation | TFSec, Checkov, SAST scanning |
| Python Scripting | ServiceNow API integration |
| API Integration | RESTful services with error handling |
| DevOps Practices | GitOps, automated testing, approval gates |

---

## Future Enhancements

- [ ] Morpheus CMP live integration (pending Community Edition)
- [ ] Dynamic Ansible inventory from Terraform outputs
- [ ] Kubernetes deployment options
- [ ] Cost management and reporting
- [ ] Multi-cloud provider support (AWS, Azure)
- [ ] Expanded ServiceNow integration (Change Management)

---

## Author

Built as a technical demonstration for CMP Automation Engineer capabilities.

---

## License

This project is for demonstration purposes.