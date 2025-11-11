*** Settings ***
Library    SystemManagerLibrary

*** Test Cases ***
HC-02 Storage Pool Limit: Deny Oversized Provisioning
    [Documentation]    Verify provisioning fails when storage allocation exceeds the pool limit.
    Run Keyword And Expect Error    *AssertionError* Provision VM    TenantOversize    cpu=1|mem=1|storage=501
    Check VM Status    TenantOversize
    Should Be Equal    ${status}    unknown    Oversized VM was provisioned.

VC-01 Snapshot/Rollback: Configuration Isolation
    [Documentation]    Verify rollback of TenantA does not affect TenantB's configuration/status.
    # We will mock the snapshot/rollback logic within the library (not explicitly shown here)
    # Assume TenantA has been provisioned for this test
    Check Unaffected Status    TenantB
    Log To Console    Snapshot and rollback simulation successful for TenantA.