class MultiTenancy(unittest.TestCase):
    """Test Suite for Multi-tenancy Isolation and Security."""

    @classmethod
    def setUpClass(cls):
        """Setup initial tenants for cross-tenant testing."""
        cls.manager = system_manager
        print("\n--- Setting up MultiTenancy Test Suite ---")
        cls.manager.provision_vm('TenantA', {'cpu': 2, 'mem': 4})
        cls.manager.provision_vm('TenantB', {'cpu': 4, 'mem': 8})

    def test_MT_01_data_isolation(self):
        """Verify Tenant A cannot read/write Tenant B's filesystem data."""
        print(f"  Running MT-01: Data Isolation Check.")
        # Tenant A attempts to write to Tenant B's space
        success, message = self.manager.write_fs(
            tenant_id='TenantA',
            path='/data/file.txt',
            data='Secret Data',
            target_tenant='TenantB'
        )
        self.assertFalse(success, f"Expected cross-tenant write to fail, but it succeeded. Message: {message}")
        self.assertIn("Permission Denied", message, "Expected permission denied message.")

    def test_MT_02_resource_contention(self):
        """Verify minimum resource guarantees during contention."""
        print(f"  Running MT-02: Resource Contention Check.")
        # In a real test, this would involve loading both VMs/Containers simultaneously
        # and checking performance metrics via the monitoring API.
        is_isolated = self.manager.check_isolation('TenantA', 'TenantB')
        self.assertTrue(is_isolated, "Resource isolation failed: High load on A degraded B's performance unexpectedly.")

    def test_MT_05_cleanup_integrity(self):
        """Verify de-provisioning a tenant cleans up all resources without affecting others."""
        print(f"  Running MT-05: Cleanup Integrity Check (Deprovisioning).")
        # Ensure TenantB is running before cleanup
        self.assertEqual(self.manager.check_vm_status('TenantB'), 'running', "TenantB not running before test.")

        # Provision a new temporary tenant (C) and de-provision it
        self.manager.provision_vm('TenantC', {'cpu': 1, 'mem': 2})
        cleanup_success = self.manager.deprovision_tenant('TenantC')
        
        self.assertTrue(cleanup_success, "Deprovisioning of Tenant C failed.")
        self.assertEqual(self.manager.check_vm_status('TenantC'), 'unknown', "Tenant C VM/data still exists after cleanup.")
        
        # Verify Tenant A and B are still functional
        self.assertEqual(self.manager.check_vm_status('TenantA'), 'running', "Tenant A was affected by Tenant C's cleanup.")
        self.assertEqual(self.manager.check_vm_status('TenantB'), 'running', "Tenant B was affected by Tenant C's cleanup.")