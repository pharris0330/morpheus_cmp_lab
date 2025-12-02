#!/usr/bin/env python3
"""
ServiceNow CMDB Validation Script
=================================
This script validates that VMs provisioned through Morpheus CMP
are properly synchronized to the ServiceNow CMDB.

Usage:
    python servicenow_cmdb_sync.py --vm-name <name> --environment <env>
    python servicenow_cmdb_sync.py --vm-name dev-web-01 --environment dev --validate

Author: Morpheus Automation Lab
Version: 1.0.0
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, Optional, Tuple, Any

# Third-party imports
try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("ERROR: 'requests' library required. Install with: pip install requests")
    sys.exit(1)


#--------------------------------------------------------------
# Configuration
#--------------------------------------------------------------

class ServiceNowConfig:
    """ServiceNow connection configuration."""
    
    def __init__(self):
        # Load from environment variables (secure) or use defaults for demo
        self.instance = os.getenv('SNOW_INSTANCE', 'dev123456.service-now.com')
        self.username = os.getenv('SNOW_USERNAME', 'admin')
        self.password = os.getenv('SNOW_PASSWORD', '')
        self.api_version = 'v2'
        
        # API endpoints
        self.base_url = f"https://{self.instance}/api/now/{self.api_version}"
        self.cmdb_table = os.getenv('SNOW_CMDB_TABLE', 'cmdb_ci_vm_instance')
        self.incident_table = 'incident'
        
        # Timeouts
        self.timeout = 30
        self.retry_attempts = 3
        self.retry_delay = 5

    def validate(self) -> bool:
        """Validate configuration is complete."""
        if not self.password:
            logging.warning("SNOW_PASSWORD not set - running in demo mode")
            return False
        return all([self.instance, self.username, self.password])


#--------------------------------------------------------------
# Logging Setup
#--------------------------------------------------------------

def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure logging with appropriate level and format."""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    return logging.getLogger(__name__)


#--------------------------------------------------------------
# ServiceNow API Client
#--------------------------------------------------------------

class ServiceNowClient:
    """Client for interacting with ServiceNow REST API."""
    
    def __init__(self, config: ServiceNowConfig):
        self.config = config
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(config.username, config.password)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.logger = logging.getLogger(__name__)

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Tuple[bool, Dict]:
        """
        Make HTTP request to ServiceNow API with retry logic.
        
        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        url = f"{self.config.base_url}/{endpoint}"
        
        for attempt in range(self.config.retry_attempts):
            try:
                self.logger.debug(f"API Request: {method} {url}")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=self.config.timeout
                )
                
                # Log response status
                self.logger.debug(f"Response Status: {response.status_code}")
                
                # Handle response
                if response.status_code == 200:
                    return True, response.json()
                elif response.status_code == 201:
                    return True, response.json()
                elif response.status_code == 401:
                    self.logger.error("Authentication failed - check credentials")
                    return False, {"error": "Authentication failed"}
                elif response.status_code == 404:
                    self.logger.warning("Resource not found")
                    return False, {"error": "Not found"}
                else:
                    self.logger.warning(
                        f"Request failed with status {response.status_code}: "
                        f"{response.text[:200]}"
                    )
                    
            except requests.exceptions.Timeout:
                self.logger.warning(f"Request timeout (attempt {attempt + 1})")
            except requests.exceptions.ConnectionError as e:
                self.logger.warning(f"Connection error (attempt {attempt + 1}): {e}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                return False, {"error": str(e)}
            
            # Wait before retry
            if attempt < self.config.retry_attempts - 1:
                import time
                time.sleep(self.config.retry_delay)
        
        return False, {"error": "Max retries exceeded"}


#--------------------------------------------------------------
# CMDB Functions
#--------------------------------------------------------------

def get_cmdb_record(
    client: ServiceNowClient, 
    vm_name: str,
    additional_filters: Optional[Dict] = None
) -> Optional[Dict]:
    """
    Retrieve a VM record from ServiceNow CMDB.
    
    Args:
        client: ServiceNow API client
        vm_name: Name of the VM to look up
        additional_filters: Optional additional query filters
        
    Returns:
        CMDB record dict if found, None otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Looking up CMDB record for VM: {vm_name}")
    
    # Build query parameters
    query = f"name={vm_name}"
    if additional_filters:
        for key, value in additional_filters.items():
            query += f"^{key}={value}"
    
    params = {
        'sysparm_query': query,
        'sysparm_limit': 1,
        'sysparm_display_value': 'true',
        'sysparm_fields': ','.join([
            'sys_id',
            'name',
            'ip_address',
            'cpu_count',
            'ram',
            'disk_space',
            'state',
            'os',
            'os_version',
            'environment',
            'managed_by',
            'sys_created_on',
            'sys_updated_on',
            'correlation_id',
            'discovery_source'
        ])
    }
    
    # Make API request
    endpoint = f"table/{client.config.cmdb_table}"
    success, response = client._make_request('GET', endpoint, params=params)
    
    if not success:
        logger.error(f"Failed to query CMDB: {response.get('error', 'Unknown error')}")
        return None
    
    # Parse response
    result = response.get('result', [])
    
    if not result:
        logger.warning(f"No CMDB record found for VM: {vm_name}")
        return None
    
    record = result[0]
    logger.info(f"Found CMDB record: sys_id={record.get('sys_id')}")
    
    return record


def get_cmdb_records_by_environment(
    client: ServiceNowClient,
    environment: str
) -> list:
    """
    Retrieve all VM records for a specific environment.
    
    Args:
        client: ServiceNow API client
        environment: Environment name (dev, prod, etc.)
        
    Returns:
        List of CMDB records
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Querying CMDB records for environment: {environment}")
    
    params = {
        'sysparm_query': f"environment={environment}",
        'sysparm_display_value': 'true',
        'sysparm_fields': 'sys_id,name,ip_address,state,environment'
    }
    
    endpoint = f"table/{client.config.cmdb_table}"
    success, response = client._make_request('GET', endpoint, params=params)
    
    if not success:
        return []
    
    records = response.get('result', [])
    logger.info(f"Found {len(records)} records in environment: {environment}")
    
    return records


#--------------------------------------------------------------
# Validation Functions
#--------------------------------------------------------------

def validate_sync(
    expected: Dict[str, Any], 
    actual: Optional[Dict[str, Any]]
) -> Tuple[bool, list]:
    """
    Validate that CMDB record matches expected values from Terraform/Morpheus.
    
    Args:
        expected: Expected values from provisioning
        actual: Actual values from CMDB
        
    Returns:
        Tuple of (validation_passed: bool, discrepancies: list)
    """
    logger = logging.getLogger(__name__)
    logger.info("Validating CMDB sync...")
    
    discrepancies = []
    
    # Check if record exists
    if actual is None:
        discrepancies.append({
            'field': 'record',
            'expected': 'exists',
            'actual': 'not found',
            'severity': 'critical'
        })
        return False, discrepancies
    
    # Define validation rules
    validation_rules = {
        'name': {
            'required': True,
            'severity': 'critical'
        },
        'ip_address': {
            'required': False,
            'severity': 'warning'
        },
        'cpu_count': {
            'required': False,
            'severity': 'warning',
            'transform': lambda x: str(x) if x else None
        },
        'environment': {
            'required': True,
            'severity': 'high'
        },
        'state': {
            'required': False,
            'expected_values': ['On', 'Running', 'Powered On'],
            'severity': 'warning'
        }
    }
    
    # Validate each field
    for field, rules in validation_rules.items():
        expected_value = expected.get(field)
        actual_value = actual.get(field)
        
        # Apply transformation if specified
        if 'transform' in rules and expected_value:
            expected_value = rules['transform'](expected_value)
        
        # Skip if expected value not provided and not required
        if expected_value is None and not rules.get('required'):
            continue
        
        # Check for expected values list
        if 'expected_values' in rules:
            if actual_value not in rules['expected_values']:
                discrepancies.append({
                    'field': field,
                    'expected': f"one of {rules['expected_values']}",
                    'actual': actual_value,
                    'severity': rules['severity']
                })
            continue
        
        # Standard comparison
        if expected_value and str(expected_value) != str(actual_value):
            discrepancies.append({
                'field': field,
                'expected': expected_value,
                'actual': actual_value,
                'severity': rules['severity']
            })
    
    # Determine overall pass/fail
    critical_issues = [d for d in discrepancies if d['severity'] == 'critical']
    high_issues = [d for d in discrepancies if d['severity'] == 'high']
    
    passed = len(critical_issues) == 0 and len(high_issues) == 0
    
    # Log results
    if passed:
        logger.info("[OK] CMDB validation PASSED")
        if discrepancies:
            logger.warning(f"  (with {len(discrepancies)} minor discrepancies)")
    else:
        logger.error("[FAIL] CMDB validation FAILED")
        for d in discrepancies:
            logger.error(f"  [{d['severity'].upper()}] {d['field']}: "
                        f"expected '{d['expected']}', got '{d['actual']}'")
    
    return passed, discrepancies


#--------------------------------------------------------------
# Incident Management
#--------------------------------------------------------------

def create_incident_on_failure(
    client: ServiceNowClient,
    vm_name: str,
    environment: str,
    discrepancies: list,
    additional_details: Optional[str] = None
) -> Optional[str]:
    """
    Create a ServiceNow incident when CMDB validation fails.
    
    Args:
        client: ServiceNow API client
        vm_name: Name of the VM with sync issues
        environment: Environment where the issue occurred
        discrepancies: List of validation discrepancies
        additional_details: Optional additional context
        
    Returns:
        Incident number if created successfully, None otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Creating incident for CMDB sync failure...")
    
    # Build incident description
    description_lines = [
        f"CMDB Sync Validation Failed",
        f"",
        f"VM Name: {vm_name}",
        f"Environment: {environment}",
        f"Timestamp: {datetime.now().isoformat()}",
        f"",
        f"Discrepancies Found:",
        f"-" * 40
    ]
    
    for d in discrepancies:
        description_lines.append(
            f"[{d['severity'].upper()}] {d['field']}: "
            f"expected '{d['expected']}', actual '{d['actual']}'"
        )
    
    if additional_details:
        description_lines.extend([
            f"",
            f"Additional Details:",
            additional_details
        ])
    
    # Determine impact and urgency based on severity
    has_critical = any(d['severity'] == 'critical' for d in discrepancies)
    has_high = any(d['severity'] == 'high' for d in discrepancies)
    
    if has_critical:
        impact = '1'  # High
        urgency = '1'  # High
    elif has_high:
        impact = '2'  # Medium
        urgency = '2'  # Medium
    else:
        impact = '3'  # Low
        urgency = '3'  # Low
    
    # Build incident payload
    incident_data = {
        'short_description': f"CMDB Sync Failure: {vm_name} ({environment})",
        'description': '\n'.join(description_lines),
        'category': 'Software',
        'subcategory': 'Integration',
        'impact': impact,
        'urgency': urgency,
        'assignment_group': 'Cloud Operations',
        'caller_id': 'morpheus.integration',
        'configuration_item': vm_name,
        'u_environment': environment,  # Custom field example
        'correlation_id': f"cmdb-sync-{vm_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }
    
    # Create incident
    endpoint = f"table/{client.config.incident_table}"
    success, response = client._make_request('POST', endpoint, data=incident_data)
    
    if not success:
        logger.error(f"Failed to create incident: {response.get('error', 'Unknown error')}")
        return None
    
    result = response.get('result', {})
    incident_number = result.get('number')
    
    if incident_number:
        logger.info(f"[OK] Created incident: {incident_number}")
        return incident_number
    
    logger.error("Incident created but no number returned")
    return None


def resolve_incident(
    client: ServiceNowClient,
    incident_number: str,
    resolution_notes: str
) -> bool:
    """
    Resolve an existing incident.
    
    Args:
        client: ServiceNow API client
        incident_number: The incident number to resolve
        resolution_notes: Notes describing the resolution
        
    Returns:
        True if resolved successfully, False otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Resolving incident: {incident_number}")
    
    # First, get the incident sys_id
    params = {
        'sysparm_query': f"number={incident_number}",
        'sysparm_limit': 1,
        'sysparm_fields': 'sys_id'
    }
    
    endpoint = f"table/{client.config.incident_table}"
    success, response = client._make_request('GET', endpoint, params=params)
    
    if not success:
        logger.error("Failed to find incident")
        return False
    
    result = response.get('result', [])
    if not result:
        logger.error(f"Incident {incident_number} not found")
        return False
    
    sys_id = result[0].get('sys_id')
    
    # Update incident to resolved
    update_data = {
        'state': '6',  # Resolved
        'close_code': 'Solved (Permanently)',
        'close_notes': resolution_notes
    }
    
    endpoint = f"table/{client.config.incident_table}/{sys_id}"
    success, response = client._make_request('PATCH', endpoint, data=update_data)
    
    if success:
        logger.info(f"[OK] Incident {incident_number} resolved")
        return True
    
    logger.error(f"Failed to resolve incident: {response.get('error')}")
    return False


#--------------------------------------------------------------
# Main Validation Workflow
#--------------------------------------------------------------

def run_validation(
    vm_name: str,
    environment: str,
    expected_values: Dict[str, Any],
    create_incident: bool = True,
    demo_mode: bool = False
) -> Tuple[bool, Dict]:
    """
    Run full CMDB validation workflow.
    
    Args:
        vm_name: Name of the VM to validate
        environment: Environment name
        expected_values: Expected values to validate against
        create_incident: Whether to create incident on failure
        demo_mode: Run without actual API calls
        
    Returns:
        Tuple of (passed: bool, results: dict)
    """
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("  CMDB VALIDATION WORKFLOW")
    logger.info("=" * 60)
    logger.info(f"VM Name: {vm_name}")
    logger.info(f"Environment: {environment}")
    logger.info(f"Demo Mode: {demo_mode}")
    logger.info("=" * 60)
    
    results = {
        'vm_name': vm_name,
        'environment': environment,
        'timestamp': datetime.now().isoformat(),
        'passed': False,
        'cmdb_record': None,
        'discrepancies': [],
        'incident_number': None
    }
    
    # Demo mode - simulate validation
    if demo_mode:
        logger.info("Running in DEMO MODE - simulating API responses")
        
        # Simulate CMDB record
        simulated_record = {
            'sys_id': 'demo-sys-id-12345',
            'name': vm_name,
            'ip_address': '192.168.1.100',
            'cpu_count': expected_values.get('cpu_count', '2'),
            'environment': environment,
            'state': 'On',
            'managed_by': 'Morpheus'
        }
        
        results['cmdb_record'] = simulated_record
        passed, discrepancies = validate_sync(expected_values, simulated_record)
        results['passed'] = passed
        results['discrepancies'] = discrepancies
        
        logger.info("Demo validation complete")
        return passed, results
    
    # Production mode
    config = ServiceNowConfig()
    
    if not config.validate():
        logger.error("ServiceNow configuration incomplete")
        logger.error("Set environment variables: SNOW_INSTANCE, SNOW_USERNAME, SNOW_PASSWORD")
        results['error'] = "Configuration incomplete"
        return False, results
    
    client = ServiceNowClient(config)
    
    # Step 1: Retrieve CMDB record
    cmdb_record = get_cmdb_record(client, vm_name)
    results['cmdb_record'] = cmdb_record
    
    # Step 2: Validate sync
    passed, discrepancies = validate_sync(expected_values, cmdb_record)
    results['passed'] = passed
    results['discrepancies'] = discrepancies
    
    # Step 3: Create incident if validation failed
    if not passed and create_incident:
        incident_number = create_incident_on_failure(
            client=client,
            vm_name=vm_name,
            environment=environment,
            discrepancies=discrepancies
        )
        results['incident_number'] = incident_number
    
    return passed, results


#--------------------------------------------------------------
# CLI Interface
#--------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Validate VM synchronization with ServiceNow CMDB',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run validation in demo mode
  python servicenow_cmdb_sync.py --vm-name dev-web-01 --environment dev --demo

  # Run validation with real ServiceNow instance
  export SNOW_INSTANCE=your-instance.service-now.com
  export SNOW_USERNAME=admin
  export SNOW_PASSWORD=your-password
  python servicenow_cmdb_sync.py --vm-name dev-web-01 --environment dev

  # Validate with expected values
  python servicenow_cmdb_sync.py --vm-name dev-web-01 --environment dev \\
    --expected-cpu 2 --expected-memory 4096

  # Output results as JSON
  python servicenow_cmdb_sync.py --vm-name dev-web-01 --environment dev --json
        """
    )
    
    parser.add_argument(
        '--vm-name', '-n',
        required=True,
        help='Name of the VM to validate'
    )
    
    parser.add_argument(
        '--environment', '-e',
        required=True,
        choices=['dev', 'staging', 'prod', 'production'],
        help='Environment name'
    )
    
    parser.add_argument(
        '--expected-cpu',
        type=int,
        help='Expected CPU count'
    )
    
    parser.add_argument(
        '--expected-memory',
        type=int,
        help='Expected memory in MB'
    )
    
    parser.add_argument(
        '--expected-ip',
        help='Expected IP address'
    )
    
    parser.add_argument(
        '--no-incident',
        action='store_true',
        help='Do not create incident on failure'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run in demo mode (no actual API calls)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    # Build expected values from arguments
    expected_values = {
        'name': args.vm_name,
        'environment': args.environment
    }
    
    if args.expected_cpu:
        expected_values['cpu_count'] = args.expected_cpu
    if args.expected_memory:
        expected_values['ram'] = args.expected_memory
    if args.expected_ip:
        expected_values['ip_address'] = args.expected_ip
    
    # Run validation
    passed, results = run_validation(
        vm_name=args.vm_name,
        environment=args.environment,
        expected_values=expected_values,
        create_incident=not args.no_incident,
        demo_mode=args.demo
    )
    
    # Output results
    if args.json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print()
        print("=" * 60)
        print("  VALIDATION RESULTS")
        print("=" * 60)
        print(f"  Status: {'PASSED' if passed else 'FAILED'}")
        print(f"  VM: {results['vm_name']}")
        print(f"  Environment: {results['environment']}")
        
        if results.get('discrepancies'):
            print(f"  Discrepancies: {len(results['discrepancies'])}")
            for d in results['discrepancies']:
                print(f"    - [{d['severity']}] {d['field']}")
        
        if results.get('incident_number'):
            print(f"  Incident: {results['incident_number']}")
        
        print("=" * 60)
    
    # Return exit code
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())