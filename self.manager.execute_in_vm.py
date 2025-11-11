# ... (existing imports and SystemManager class definition)

class SystemManager:
    # ... (existing __init__ and methods like provision_vm, write_fs, etc.)

    def execute_in_vm(self, tenant_id, command):
        """Simulates executing a Linux command inside a specific VM."""
        print(f"  [VM {tenant_id}] Executing: {command}")
        
        if command.startswith("mount /dev/sdb /mnt/tenant_B_path"):
            # UT-05: Tenant A trying to mount Tenant B's resource
            return False, "Error: Mount failed. Device not found or permission denied."
        
        elif command.startswith("umount /"):
            # UT-06: Tenant trying to unmount critical shared point
            return False, "Error: umount: /: device is busy or insufficient privileges."
            
        elif command.startswith("ls -l /..") or command.startswith("cd ../.."):
            # UT-07: Tenant trying to traverse out of its dedicated path
            return False, "ls: cannot access '../..': Permission denied."
            
        elif "chmod 777 my_file.txt" in command:
            # UT-09: Tenant modifying permissions in their own path
            return True, "Permissions changed successfully."
            
        elif "chown root:root my_file.txt" in command:
            # UT-10: Tenant trying to change ownership to a privileged/external user
            return False, "Error: Operation not permitted: Cannot change file ownership."
            
        elif "ls -l my_file.txt" in command:
            # UT-08: Positive permission check
            return True, "drwxrwxr-x tenantA_user tenantA_group my_file.txt"

        # Default success for general commands
        return True, "Command executed successfully (simulated)."

# Initialize the mock system manager (already done in the previous response)
system_manager = SystemManager()