*** Settings ***
Library    SystemManagerLibrary
Test Setup     Log To Console    Starting Multi-tenancy Test
Test Teardown  Log To Console    Multi-tenancy Test Complete

*** Test Cases ***
MT-01 Data Isolation: Deny Cross-Tenant Filesystem Write
    [Documentation]    Verify Tenant A cannot write to Tenant B's filesystem path.
    ${tenant_A}=    Set Variable    TenantA
    ${tenant_B}=    Set Variable    TenantB
    Run Keyword And Expect Error    *PermissionError* Write Fs Cross Tenant    ${tenant_A}    ${tenant_B}    Malicious Data
    
MT-02 Resource Contention: Check QoS and Isolation
    [Documentation]    Verify high load on one tenant doesn't starve others.
    # In a real scenario, this step would trigger load generation on VMs
    ${isolated}=    Check Resource Isolation    TenantA    TenantB
    Should Be True    ${isolated}    Resource isolation failed during contention.

MT-05 Cleanup Integrity: Verify No Artifacts After De-provisioning
    [Documentation]    Provision a temporary tenant, delete it, and verify other tenants are stable.
    Provision VM    TenantDEL    cpu=1|mem=1|storage=10
    Deprovision Tenant    TenantDEL
    ${status_A}=    Check VM Status    TenantA
    Should Be Equal    ${status_A}    running    TenantA was affected by cleanup.
    ${status_DEL}=   Check VM Status    TenantDEL
    Should Be Equal    ${status_DEL}    unknown    TenantDEL resources were not removed.