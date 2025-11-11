class Utils(unittest.TestCase):
    """Test Suite for System Utilities (Provisioning, Monitoring, Backup, and Filesystem Commands)."""

    def setUp(self):
        self.manager = system_manager
        self.test_tenant_id = 'TenantD'
        # Ensure base tenants A and B are running
        self.manager.provision_vm('TenantA', {'cpu': 2, 'mem': 4})
        self.manager.provision_vm('TenantB', {'cpu': 4, 'mem': 8})

    # --- Existing Utils Scenarios (UT-01 to UT-04) remain here ---
    
    # ... (Omitted UT-01 to UT-04 for brevity in this response, assume they are present)
    
    # --- New Filesystem Scenarios (UT-05 to UT-10) ---

    def test_UT_05_mount_isolation(self):
        """Verify Tenant A cannot mount resources belonging to Tenant B."""
        print(f"\n  Running UT-05: Mount Isolation Check.")
        # Tenant A attempts to mount a volume path intended for Tenant B
        success, output = self.manager.execute_in_vm(
            tenant_id='TenantA',
            command='mount /dev/sdb /mnt/tenant_B_path -o ro'
        )
        self.assertFalse(success, "Tenant A unexpectedly mounted Tenant B's designated resource.")
        self.assertIn("permission denied", output.lower(), "Expected permission/device error on mount failure.")

    def test_UT_06_unmount_protection(self):
        """Verify critical mount points are protected from unmount by the tenant."""
        print(f"  Running UT-06: Critical Unmount Protection.")
        # Tenant A attempts to unmount a critical shared mount point or root FS (/)
        success, output = self.manager.execute_in_vm(
            tenant_id='TenantA',
            command='umount /' 
        )
        self.assertFalse(success, "Critical mount point was successfully unmounted by a tenant VM.")
        self.assertIn("device is busy", output.lower(), "Expected 'device busy' or permission error for critical unmount.")

    def test_UT_07_list_traverse_negative(self):
        """Verify Tenant A cannot traverse out of its assigned directory boundaries."""
        print(f"  Running UT-07: Filesystem Traverse Denial.")
        # Tenant A attempts to list files outside its dedicated mount path
        success, output = self.manager.execute_in_vm(
            tenant_id='TenantA',
            command='ls -l /.. /etc/hosts'
        )
        # Note: Even if the command is "successful" (returns 0), the output must show "Permission denied"
        self.assertIn("permission denied", output.lower(), "Tenant A was able to traverse outside its isolated path.")

    def test_UT_08_permission_check_positive(self):
        """Verify a tenant can correctly check permissions on its own files."""
        print(f"  Running UT-08: Permission Check (Positive).")
        # Tenant A checks permissions on a file it created
        success, output = self.manager.execute_in_vm(
            tenant_id='TenantA',
            command='ls -l my_file.txt'
        )
        self.assertTrue(success, "Tenant A failed to check permissions on its own file.")
        self.assertIn("tenantA_user", output, "Filesystem did not correctly report ownership.")
        self.assertIn("drwxrwxr-x", output, "Filesystem did not correctly report access bits.")

    def test_UT_09_give_remove_permission_positive(self):
        """Verify a tenant can change permissions on its own files."""
        print(f"  Running UT-09: CHMOD/CHOWN Positive Test.")
        
        # 1. Granting permission
        success_grant, output_grant = self.manager.execute_in_vm(
            tenant_id='TenantA',
            command='chmod 777 my_file.txt'
        )
        self.assertTrue(success_grant, f"Tenant A failed to grant permissions on its own file. Output: {output_grant}")
        
        # 2. Revoking permission (implicitly via another chmod)
        success_revoke, output_revoke = self.manager.execute_in_vm(
            tenant_id='TenantA',
            command='chmod 700 my_file.txt'
        )
        self.assertTrue(success_revoke, f"Tenant A failed to revoke permissions on its own file. Output: {output_revoke}")

    def test_UT_10_give_permission_negative(self):
        """Verify a tenant cannot change ownership (chown) to privileged/external users."""
        print(f"  Running UT-10: CHOWN/CHMOD Negative Test.")
        
        # Attempt to change file ownership to 'root'
        success, output = self.manager.execute_in_vm(
            tenant_id='TenantA',
            command='chown root:root my_file.txt'
        )
        self.assertFalse(success, "Tenant A successfully changed ownership to 'root'/'external' user.")
        self.assertIn("operation not permitted", output.lower(), "Expected permission denial on chown attempt.")

    def tearDown(self):
        """Cleanup after the Utils test suit."""
        self.manager.deprovision_tenant('TenantD')
        self.manager.deprovision_tenant('TenantA')
        self.manager.deprovision_tenant('TenantB')

# --- Next Step (Execution Block) ---
if __name__ == '__main__':
    # To run only the Utils test suit:
    # suite = unittest.TestLoader().loadTestsFromTestCase(Utils)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    print("\n--- Running All Test Suits (MultiTenancy, Utils, RedundancyChecks, HardwareAndVMConfig) ---")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)