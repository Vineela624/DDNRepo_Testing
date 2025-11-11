# SystemManagerLibrary.py (Save this file in your project directory)

class SystemManagerLibrary:
    """
    A Python Library to expose system interaction methods as Robot Framework Keywords.
    """
    
    # --- Constructor and Internal State ---
    def __init__(self):
        self.tenant_data = {}
        # Auto-provision initial tenants for testing isolation
        self.provision_vm('TenantA', {'cpu': 2, 'mem': 4})
        self.provision_vm('TenantB', {'cpu': 4, 'mem': 8})
        self.provision_vm('TenantC', {'cpu': 1, 'mem': 2})

    # --- Core Keywords (Mapping to SystemManager) ---
    
    def provision_vm(self, tenant_id, resources):
        """Simulates provisioning a VM and returns a status."""
        resources['storage'] = resources.get('storage', 0) # Ensure storage exists
        if resources['storage'] > 500:
            raise AssertionError(f"Provisioning failed: Storage limit exceeded for {tenant_id}.")
        
        self.tenant_data[tenant_id] = {
            'vm_status': 'running', 
            'fs_path': f'/mnt/shared/tenant_{tenant_id}/', 
            'resources': resources
        }
        return "SUCCESS"

    def deprovision_tenant(self, tenant_id):
        """Simulates deleting a tenant and its resources."""
        if tenant_id in self.tenant_data:
            del self.tenant_data[tenant_id]
            return "SUCCESS"
        return "Tenant not found"

    def write_fs_cross_tenant(self, tenant_a, tenant_b, data):
        """Simulates Tenant A trying to write to Tenant B's filesystem."""
        if tenant_a != tenant_b:
            raise PermissionError(f"Permission Denied: {tenant_a} cannot access {tenant_b}'s data.")
        return "Data written successfully."

    def check_vm_status(self, tenant_id):
        """Returns the current VM status."""
        return self.tenant_data.get(tenant_id, {}).get('vm_status', 'unknown')

    def check_resource_isolation(self, tenant_id_a, tenant_id_b):
        """Simulates checking if resource usage is isolated (MT-02)."""
        # In a real test, this would analyze monitoring data.
        return True

    def execute_fs_command_in_vm(self, tenant_id, command):
        """Simulates executing a Linux FS command inside a VM."""
        if command.startswith("mount /dev/sdb /mnt/tenant_B_path"):
            raise AssertionError(f"Mount failed in {tenant_id}: Permission denied or resource missing.")
        
        elif command.startswith("umount /"):
            raise AssertionError(f"Unmount failed in {tenant_id}: Critical device busy.")
            
        elif "chown root:root" in command:
            raise PermissionError("Operation not permitted: Cannot change file ownership.")
            
        return "Command executed successfully."
    
    def simulate_host_failure(self, tenant_id):
        """Simulates SR-01: Host failure leading to HA failover."""
        # In a real system, this would trigger the HA mechanism
        print(f"Simulating Host Failure for host running {tenant_id}...")
        self.tenant_data[tenant_id]['vm_status'] = 'restarting'
        # Assume HA is fast
        time.sleep(1) 
        self.tenant_data[tenant_id]['vm_status'] = 'running'
        return "HA Failover complete"

    def simulate_guest_crash_and_recovery(self, tenant_id):
        """Simulates SR-03: Guest OS crash and auto-restart."""
        print(f"Simulating guest crash in {tenant_id}...")
        self.tenant_data[tenant_id]['vm_status'] = 'crashed'
        time.sleep(0.5) 
        self.tenant_data[tenant_id]['vm_status'] = 'running'
        return "Guest auto-restart successful"
        
    def check_logs_for_leakage(self, tenant_id_a, tenant_id_b):
        """Simulates checking logs for UT-02."""
        # Logs for A should not contain B's data
        if tenant_id_b in "Log for A only.":
            return False
        return True
        
    def execute_backup_restore(self, tenant_id):
        """Simulates UT-03: Running a backup/restore job."""
        return "Backup and restore completed successfully"

    def check_unaffected_status(self, tenant_id):
        """Helper to ensure control tenants remain running."""
        status = self.check_vm_status(tenant_id)
        if status != 'running':
            raise AssertionError(f"Control tenant {tenant_id} was unexpectedly affected. Status: {status}")
        return status