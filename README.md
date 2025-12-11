# Morpheus CMP Automation Lab

[![Infrastructure CI/CD Pipeline](https://github.com/your-actual-github-username/morpheus-cmp-lab/actions/workflows/infrastructure.yml/badge.svg)](https://github.com/your-actual-github-username/morpheus-cmp-lab/actions/workflows/infrastructure.yml)

A comprehensive infrastructure automation lab demonstrating enterprise-grade Cloud Management Platform (CMP) integration, Infrastructure as Code (IaC), and DevOps workflows using **HPE Morpheus Enterprise**.

---

## Executive Summary

This lab demonstrates end-to-end automation capabilities for hybrid cloud infrastructure management. Using Morpheus Community Edition, I successfully:

- **Integrated AWS Cloud** and resolved IAM provisioning issues
- **Provisioned EC2 instances** through Morpheus CMP
- **Built automation workflows** with script and REST tasks
- **Created CI/CD pipelines** with security scanning
- **Developed ServiceNow CMDB integration** for ITSM workflows

> "Using Morpheus Community Edition, I integrated AWS, resolved IAM provisioning failures, built automation tasks and workflows, and successfully provisioned EC2 instances through Morpheus while documenting CE limitations that prevent agent-based lifecycle automation."

---

## Architecture Overview
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions CI/CD                              │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────────────────┐ │
│  │ Validate  │→ │ Security  │→ │   Plan    │→ │ Approve → Apply       │ │
│  │ TF + Ans  │  │ TFSec     │  │ TF Plan   │  │ Manual Gate           │ │
│  └───────────┘  └───────────┘  └───────────┘  └───────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      HPE Morpheus Enterprise CMP                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Clouds    │  │   Groups    │  │   Tasks     │  │  Workflows  │    │
│  │   AWS-Lab   │  │ Automation  │  │ Nginx/REST  │  │ Provisioning│    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐
│    AWS EC2      │  │   ServiceNow    │  │    Ansible Configuration   │
│  Ubuntu 20.04   │  │   CMDB Sync     │  │    Nginx + Security        │
└─────────────────┘  └─────────────────┘  └─────────────────────────────┘
```

---

## Lab Accomplishments

### ☁️ Cloud Integration (AWS)

| Component | Status | Details |
|-----------|--------|---------|
| AWS Cloud Added | ✅ Complete | `AWS-Lab` integrated with Morpheus |
| Group Created | ✅ Complete | `Automation-Lab` for resource scoping |
| EC2 Sync | ✅ Complete | Instance types, networks, subnets, security groups |
| IAM Permissions | ✅ Resolved | Fixed `DescribeInstanceTypes` and `RunInstances` |
| EC2 Provisioning | ✅ Success | Ubuntu 20.04 instance deployed |

![Morpheus Dashboard](docs/screenshots/morpheus-dashboard.png)

### ⚙️ Automation Components

| Component | Name | Purpose |
|-----------|------|---------|
| Script Task | `Install-Nginx` | Installs Nginx, writes marker file |
| REST Task | `Send-Provision-Notification` | Sends JSON webhook for ITSM integration |
| Workflow | `Provisioning-Automation-Workflow` | Chains tasks for lifecycle automation |

![Morpheus Tasks](docs/screenshots/morpheus-tasks.png)

![Morpheus Workflow](docs/screenshots/morpheus-post-provision-automation-workflow.png)

### 🖥️ Instance Provisioning

Successfully provisioned AWS EC2 instances through Morpheus:

- **Instance Type:** Ubuntu 20.04
- **Cloud:** AWS-Lab
- **Verification:** EC2 instance created, IPs assigned, compute details populated

![Instance List](docs/screenshots/morpheus-instance-list.png)

![Instance Review](docs/screenshots/morpheus-instance-review.png)

### 🔐 RBAC & Governance

Configured role-based access control demonstrating enterprise governance:

![Roles Configuration](docs/screenshots/morpheus-roles.png)

![User Permissions](docs/screenshots/morpheus-user-permissions.png)

![Groups Permissions](docs/screenshots/morpheus-groups-permission.png)

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
│       └── prod/                 # Production environment
├── ansible/
│   ├── ansible.cfg
│   ├── roles/
│   │   ├── base-config/          # Base system configuration
│   │   │   ├── tasks/main.yml
│   │   │   ├── handlers/main.yml
│   │   │   ├── defaults/main.yml
│   │   │   └── templates/
│   │   └── web-server/           # Nginx with security hardening
│   │       ├── tasks/main.yml
│   │       ├── handlers/main.yml
│   │       ├── defaults/main.yml
│   │       └── templates/
│   └── playbooks/
│       └── site.yml
├── scripts/
│   └── servicenow_cmdb_sync.py   # CMDB validation script
└── docs/
    └── screenshots/              # Lab documentation
```

---

## CI/CD Pipeline

Multi-stage pipeline with security scanning and approval gates:

| Stage | Jobs | Status |
|-------|------|--------|
| **Validate** | Terraform validate, Ansible lint | ✅ Passing |
| **Security** | TFSec, Checkov, Secrets scan, SAST | ✅ Passing |
| **Plan** | Terraform plan (dev & prod) | ✅ Passing |
| **Approve** | Manual approval gate | ✅ Configured |
| **Apply** | Terraform apply, Ansible configure | ✅ Ready |

![GitHub Pipeline](docs/screenshots/morpheus-github-pipeline.png)

---

## Terraform Modules

### VMware VM Module

Reusable module for VM provisioning:
```hcl
module "web_server" {
  source = "../../modules/vmware-vm"

  vm_name            = "${var.environment}-web-01"
  cpu_count          = var.vm_cpu_count
  memory_mb          = var.vm_memory_mb
  environment        = var.environment
  vsphere_datacenter = var.vsphere_datacenter
  vsphere_cluster    = var.vsphere_cluster
  vsphere_template   = var.vsphere_template

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

**Features:**
- Configurable CPU, memory, disk sizing
- Template-based cloning
- Environment tagging
- Multi-environment support (dev/prod)

---

## Ansible Roles

### Base Configuration Role

- System package installation
- SSH hardening (key-only auth, root login disabled)
- NTP/Chrony time synchronization
- User and group management
- Security baseline configuration

### Web Server Role

- Nginx installation and configuration
- SSL/TLS support with security headers
- Health check endpoints
- Firewall configuration (UFW)
- Self-signed certificate generation
```yaml
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

## ServiceNow Integration

Python script for CMDB validation and incident management:
```bash
# Demo mode
python scripts/servicenow_cmdb_sync.py \
  --vm-name dev-web-01 \
  --environment dev \
  --demo

# Production mode
python scripts/servicenow_cmdb_sync.py \
  --vm-name prod-web-01 \
  --environment prod \
  --expected-cpu 4
```

**Features:**
- CMDB record lookup and validation
- Automated incident creation on sync failures
- Configurable validation rules
- JSON output for CI/CD integration

---

## Troubleshooting Performed

Demonstrated real-world diagnostic capabilities:

### IAM Permission Issues
- Identified missing `DescribeInstanceTypes` and `RunInstances` permissions
- Used AWS CLI to reproduce and verify fixes
- Successfully resolved for EC2 provisioning

### Networking
- Analyzed SSH failures caused by missing key pairs
- Verified security groups, VPC, and subnet configurations

### Morpheus CE Limitations
Documented platform constraints:
- Community Edition provisioning workflow limitations
- Agent installation differences from Enterprise
- Instance lifecycle state management

> This troubleshooting experience demonstrates the diagnostic skills needed for production CMP environments.

---

## Skills Demonstrated

| Skill | Implementation |
|-------|----------------|
| Cloud Management Platform | Morpheus installation, configuration, AWS integration |
| Infrastructure as Code | Terraform modules with dev/prod environments |
| Configuration Management | Ansible roles with Jinja2 templates |
| CI/CD Pipelines | GitHub Actions multi-stage with security scanning |
| ITSM Integration | ServiceNow CMDB validation and incident creation |
| Cloud Platforms | AWS EC2 provisioning, IAM troubleshooting |
| Security Automation | TFSec, Checkov, SSH hardening, SAST scanning |
| Python Scripting | REST API integration with error handling |
| RBAC/Governance | Role-based access control, group policies |
| DevOps Practices | GitOps, automated testing, approval gates |

---

## Morpheus Screenshots

### Dashboard
![Dashboard](docs/screenshots/morpheus-dashboard.png)

### Instance Types
![Instance Types](docs/screenshots/morpheus-instance-types.png)

### Feature Access
![Features](docs/screenshots/morpheus-feature.png)

### Web Server Deployment
![Web Server Deployment](docs/screenshots/morpheus-web-server-deployment.png)

---

## Getting Started

### Prerequisites

- Terraform >= 1.6.0
- Ansible >= 2.15
- Python >= 3.10
- HPE Morpheus Enterprise (Community Edition or higher)

### Quick Start
```bash
# Clone repository
git clone https://github.com/your-actual-github-username/morpheus-cmp-lab.git
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

---

## Interview Summary

### 20-Second Version
> "I built a Morpheus automation lab with AWS integration, provisioned EC2 instances, and created CI/CD pipelines with Terraform and Ansible - demonstrating full-stack CMP automation skills."

### 45-Second Version
> "Using Morpheus Community Edition, I integrated AWS cloud, resolved IAM permission issues, and successfully provisioned EC2 instances. I built automation workflows combining shell scripts for Nginx installation with REST tasks for ServiceNow integration. The GitHub repository includes Terraform modules, Ansible roles with security hardening, and a CI/CD pipeline with security scanning - all passing validation."

### 90-Second Version
> "I completed a comprehensive Morpheus CMP automation lab demonstrating enterprise-grade practices. Starting with Morpheus Community Edition installation, I integrated AWS cloud and resolved IAM provisioning failures for DescribeInstanceTypes and RunInstances permissions. I successfully provisioned Ubuntu EC2 instances through Morpheus and built automation workflows with script tasks for Nginx installation and REST tasks for webhook notifications.

> The GitHub repository includes Terraform modules for VMware VM provisioning with separate dev/prod environments, Ansible roles implementing base configuration and web server deployment with security hardening, and a multi-stage CI/CD pipeline with TFSec and Checkov security scanning. I also developed a Python script for ServiceNow CMDB validation with automated incident creation.

> This lab demonstrates my understanding of CMP architecture, multi-cloud provisioning, IAM troubleshooting, workflow design, and infrastructure automation - exactly the skills needed for the CMP Automation Engineer role."

---

## Author

Paul Harris - CMP Automation Engineer Candidate

---

## License

This project is for demonstration purposes.
