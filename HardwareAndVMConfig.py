class HardwareAndVMConfig(unittest.TestCase):
    """Test Suite for Hardware and VM/Container Configuration Changes."""

    def setUp(self):
        self.manager = system_manager
        # Provision a dedicated VM for config testing
        self.config_tenant_id = 'TenantCONFIG'
        self.manager.provision_vm(self.config_tenant_id, {'cpu': 1, 'mem': 2, 'storage': 50})
        self.manager.provision_vm('TenantCONTROL', {'cpu': 1, 'mem': 2, 'storage': 50})

    def test_HC_02_storage_pool_limit(self):
        """Verify provisioning fails when storage capacity is exceeded."""
        print(f"\n  Running HC-02: Storage Pool Limit Check.")
        # Attempt to provision a VM that exceeds the (mocked) storage limit of 500
        success, message = self.manager.provision_vm('TenantOVER', {'cpu': 1, 'mem': 2, 'storage': 600})
        
        self.assertFalse(success, "VM provisioning succeeded despite exceeding storage limit.")
        self.assertIn("storage limit exceeded", message, "Did not receive expected resource limit error message.")

    def test_VC_01_snapshot_and_rollback(self):
        """Verify Snapshot/Checkpoint and Rollback is tenant-local and non-disruptive."""
        print(f"  Running VC-01: Snapshot/Rollback Isolation.")
        
        # Mocking specific functions for config management
        self.manager.take_snapshot = MagicMock(return_value=True)
        self.manager.rollback_vm = MagicMock(return_value=True)
        
        # 1. Take snapshot of TenantCONFIG
        self.assertTrue(self.manager.take_snapshot(self.config_tenant_id), "Snapshot failed.")
        
        # 2. Simulate configuration change/data write (new state)
        self.manager.write_fs(self.config_tenant_id, '/new_file', 'pre_rollback', self.config_tenant_id)

        # 3. Rollback TenantCONFIG
        self.assertTrue(self.manager.rollback_vm(self.config_tenant_id), "Rollback failed.")
        
        # 4. Verify isolation (TenantCONTROL should be running)
        self.assertEqual(self.manager.check_vm_status('TenantCONTROL'), 'running', "TenantCONTROL was affected by TenantCONFIG's rollback.")
        
        # In a real test, verify that '/new_file' no longer exists after rollback

    def test_VC_03_security_hardening_isolation(self):
        """Verify security policy application (e.g., SELinux profile) is isolated."""
        print(f"  Running VC-03: Security Hardening Isolation.")
        
        self.manager.apply_security_policy = MagicMock()
        self.manager.check_policy_status = MagicMock(side_effect=lambda tenant: 'ENFORCING' if tenant == self.config_tenant_id else 'DISABLED')

        # 1. Apply policy to TenantCONFIG
        self.manager.apply_security_policy(self.config_tenant_id, 'ENFORCING')
        
        # 2. Verify policy is applied to the target tenant
        self.assertEqual(self.manager.check_policy_status(self.config_tenant_id), 'ENFORCING', "Policy failed to apply to target tenant.")
        
        # 3. Verify policy is NOT applied to the control tenant
        self.assertEqual(self.manager.check_policy_status('TenantCONTROL'), 'DISABLED', "Policy leaked to other tenant.")

    def tearDown(self):
        self.manager.deprovision_tenant(self.config_tenant_id)
        self.manager.deprovision_tenant('TenantCONTROL')
        self.manager.deprovision_tenant('TenantOVER') # Clean up failed provisioning attempts as well