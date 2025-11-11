*** Settings ***
Library    SystemManagerLibrary

*** Test Cases ***
SR-01 Host Failure: HA Failover Check
    [Documentation]    Verify that host failure is handled by HA, and the VM resumes running.
    # Provision a specific VM for HA testing
    Provision VM    TenantHA    cpu=2|mem=4
    Simulate Host Failure    TenantHA
    ${status}=    Check VM Status    TenantHA
    Should Be Equal    ${status}    running    HA failed to restore the VM.
    Deprovision Tenant    TenantHA

SR-03 Tenant Guest Crash: Auto-Restart and Containment
    [Documentation]    Verify a guest OS crash is contained and triggers auto-restart.
    # Use an existing tenant (TenantA) for the crash simulation
    Simulate Guest Crash And Recovery    TenantA
    ${status_A}=    Check VM Status    TenantA
    Should Be Equal    ${status_A}    running    Guest auto-restart failed.
    Check Unaffected Status    TenantB    # Verify containment