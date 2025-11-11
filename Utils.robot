*** Settings ***
Library    SystemManagerLibrary
Test Setup     Set Test Variable    ${NEW_TENANT}    TenantNEW
Test Teardown  Deprovision Tenant    ${NEW_TENANT}

*** Test Cases ***
UT-01 Provisioning Tool: Isolated Setup
    [Documentation]    Verify a new tenant is provisioned successfully.
    ${status}=    Provision VM    ${NEW_TENANT}    cpu=2|mem=4|storage=50
    Should Be Equal    ${status}    SUCCESS
    ${vm_status}=    Check VM Status    ${NEW_TENANT}
    Should Be Equal    ${vm_status}    running

UT-02 Monitoring/Logging: Check for Data Leakage
    [Documentation]    Verify logs of TenantA do not contain TenantB's data.
    ${is_isolated}=    Check Logs For Leakage    TenantA    TenantB
    Should Be True    ${is_isolated}    Logging data leakage detected.

UT-03 Backup/Restore: Non-Disruptive and Isolated
    [Documentation]    Verify restore of TenantB does not affect TenantA.
    ${result}=    Execute Backup Restore    TenantB
    Should Be Equal    ${result}    Backup and restore completed successfully
    Check Unaffected Status    TenantA    # Check if TenantA is still running

UT-05 Mount Isolation: Deny Cross-Tenant Mount
    [Documentation]    Tenant A attempting to mount Tenant B's dedicated resource should fail.
    ${command}=    Set Variable    mount /dev/sdb /mnt/tenant_B_path
    Run Keyword And Expect Error    *AssertionError* Execute Fs Command In Vm    TenantA    ${command}

UT-10 Give Permission: Deny CHOWN to Root/External User
    [Documentation]    Tenant A trying to change ownership of its file to root should fail.
    ${command}=    Set Variable    chown root:root my_file.txt
    Run Keyword And Expect Error    *PermissionError* Execute Fs Command In Vm    TenantA    ${command}

