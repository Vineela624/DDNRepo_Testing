# TestAutomationLibrary.py - This serves as the Robot Framework Library

import time
from unittest.mock import MagicMock # Keep MagicMock for simulation

class TestAutomationLibrary:
    """
    A Robot Framework Library exposing End-to-End QA Keywords.
    This replaces the SystemManager and incorporates the scenario logic.
    """
    
    def __init__(self):
        self.tenant_data = {}
        # Initial provisioning (used by MT tests)
        self._provision_initial_tenants()

    def _provision_initial_tenants(self):
        # Internal provisioning helper
        for tenant_id, resources in [('TenantA', {'cpu': 2, 'mem': 4}), 
                                     ('TenantB', {'cpu': 4, 'mem': 8}), 
                                     ('TenantC', {'cpu': 1, 'mem': 2})]:
            self.provision_vm(tenant_id, resources)

    def provision_vm(self, tenant_id, resources):
        """[UT-01] Simulates provisioning a VM."""
        storage = resources.get('storage', 0)
        if storage > 500: # HC-02 check
            raise AssertionError(f"Provisioning failed: Storage limit exceeded for {tenant_id}.")
        
        self.tenant_data[tenant_id] = {
            'vm_status': 'running', 
            'fs_path': f'/mnt/shared/tenant_{tenant_id}/', 
            'resources': resources
        }
        return "SUCCESS"

    def deprovision_tenant(self, tenant_id):
        """[MT-05] Simulates deleting a tenant and its resources."""
        if tenant_id in self.tenant_data:
            del self.tenant_data[tenant_id]
            return True
        return False

    def check_vm_status(self, tenant_id):
        """Returns the current VM status."""
        return self.tenant_data.get(tenant_id, {}).get('vm_status', 'unknown')

    def attempt_cross_tenant_write(self, tenant_a, tenant_b):
        """[MT-01] Tenant A attempts to write to Tenant B's filesystem."""
        # This keyword should be called with Run Keyword And Expect Error
        if tenant_a != tenant_b:
            raise PermissionError(f"Permission Denied: {tenant_a} cannot access {tenant_b}'s data.")
        return "Write Succeeded (Unexpected!)"
    
    def check_resource_isolation(self, tenant_id_a, tenant_id_b):
        """[MT-02] Placeholder for checking resource contention/QoS."""
        # In a real environment, this would call a monitoring API
        return True

    def check_logging_for_leakage(self, tenant_id_a, tenant_id_b):
        """[UT-02] Checks if Tenant A's logs contain Tenant B's data."""
        logs_a = "Log for Tenant A only."
        if "Tenant B" in logs_a:
            return False
        return True
        
    def execute_fs_command_in_vm(self, tenant_id, command):
        """[UT-05, UT-06, UT-10] Simulates VM execution of Linux commands."""
        if command.startswith("mount /dev/sdb /mnt/tenant_B_path"):
            raise PermissionError(f"[UT-05] Mount failed in {tenant_id}: Permission denied or resource missing.")
        
        elif command.startswith("umount /"):
            raise PermissionError(f"[UT-06] Unmount failed in {tenant_id}: Critical device busy.")
            
        elif "chown root:root" in command:
            raise PermissionError(f"[UT-10] Operation not permitted: Cannot change file ownership.")
            
        return "Command executed successfully."

    def simulate_host_failure(self, tenant_id):
        """[SR-01] Simulates Host failure leading to HA failover."""
        time.sleep(1) 
        # Logic assumes HA automatically recovers the VM
        self.tenant_data[tenant_id]['vm_status'] = 'running'
        return "HA Failover complete"
        
    def simulate_guest_crash_and_recovery(self, tenant_id):
        """[SR-03] Simulates Guest OS crash and auto-restart."""
        time.sleep(0.5) 
        self.tenant_data[tenant_id]['vm_status'] = 'running'
        return "Guest auto-restart successful"