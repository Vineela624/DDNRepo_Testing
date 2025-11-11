import unittest
import subprocess
import sys

# Define the path to the dispatcher script
# NOTE: This assumes 'test_library.py' is in the same directory.
LIBRARY_SCRIPT = sys.executable + " test_library.py" 

class TestInfrastructureOperations(unittest.TestCase):
    """
    Test suite for infrastructure operations (tenants, mounts, VM restart)
    by calling the 'test_library.py' script via subprocess.
    """

    def _run_test(self, command, expected_code=0, expected_output=None):
        """Helper to run the command and check return code and output."""
        full_command = f"{LIBRARY_SCRIPT} {command}"
        
        # Use shell=True for convenience, though generally discouraged for user input
        result = subprocess.run(
            full_command, 
            shell=True, 
            capture_output=True, 
            text=True
        )

        # Check the exit code
        self.assertEqual(
            result.returncode, 
            expected_code, 
            f"Command failed with unexpected code. Command: '{command}'. Stdout: {result.stdout.strip()}. Stderr: {result.stderr.strip()}"
        )

        # Check for specific expected output if provided
        if expected_output:
            self.assertIn(
                expected_output, 
                result.stdout, 
                f"Expected output '{expected_output}' not found in stdout."
            )
        
        return result

    def test_01_create_tenants_success(self):
        """Verify 3 tenants are created successfully."""
        print("\n--- Running Test 1: Create Tenants ---")
        result = self._run_test("create_tenants 3", expected_output="Successfully created tenant tenant_003")
        self.assertIn("Tenant creation complete.", result.stdout)

    def test_02_create_tenants_invalid_input(self):
        """Verify an error is returned for non-integer input."""
        print("\n--- Running Test 2: Invalid Tenant Input ---")
        # Expect non-zero exit code (1) and error message from the script's ValueError handler
        self._run_test("create_tenants not_a_number", expected_code=1, expected_output="ERROR: 'num_tenants' must be an integer.")

    def test_03_mount_file1_success(self):
        """Verify mounting file1 works and confirms MOUNT_SUCCESS."""
        print("\n--- Running Test 3: Mount file1 ---")
        self._run_test("mount_file file1", expected_output="MOUNT_SUCCESS: /mnt/data/file1")

    def test_04_unmount_file1_success(self):
        """Verify unmounting file1 works and confirms UNMOUNT_SUCCESS."""
        print("\n--- Running Test 4: Unmount file1 ---")
        self._run_test("unmount_file file1", expected_output="UNMOUNT_SUCCESS: /mnt/data/file1")
        
    def test_05_mount_xyz_success(self):
        """Verify mounting persistent file 'xyz' works."""
        print("\n--- Running Test 5: Mount persistent file 'xyz' ---")
        self._run_test("mount_file xyz", expected_output="MOUNT_SUCCESS: /mnt/data/xyz")

    def test_06_restart_vm_success(self):
        """Verify VM restart sequence completes."""
        print("\n--- Running Test 6: Restart VM ---")
        self._run_test("restart_vm", expected_output="RESTART_COMPLETE: VM is back online.")

    def test_07_check_mount_xyz_persistence(self):
        """Verify 'xyz' is reported as mounted after VM restart (simulated persistence)."""
        print("\n--- Running Test 7: Check 'xyz' Persistence ---")
        self._run_test("check_mount xyz", expected_code=0, expected_output="MOUNT_EXISTS: /mnt/data/xyz")

    def test_08_check_mount_file1_not_persistent(self):
        """Verify 'file1' is reported as NOT mounted (simulated non-persistence)."""
        print("\n--- Running Test 8: Check 'file1' is NOT Persistent ---")
        # Expect failure (return code 1) for non-persistent files
        self._run_test("check_mount file1", expected_code=1, expected_output="MOUNT_NOT_FOUND: /mnt/data/file1")


if __name__ == '__main__':
    # To use this, you would run: python test_suite.py
    unittest.main(argv=sys.argv[:1], exit=False)
