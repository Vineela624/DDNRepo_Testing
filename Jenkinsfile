// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent {
        any // Use 'any' to run on any available Jenkins agent/node
    }

    // Define environment variables, like the report directory
    environment {
        ROBOT_OPTIONS = "--outputdir Reports --logtitle 'Robot Framework Execution Log'"
    }

    stages {
        stage('Setup Environment') {
            steps {
                // Assuming Python is accessible on the agent, install dependencies
                sh 'pip install robotframework'
                sh 'pip install robotframework-seleniumlibrary' // Include only necessary libs
                sh 'mkdir -p Reports' // Ensure the output directory exists
                
                // Confirm the Python library file is in the workspace
                sh 'ls -l TestAutomationLibrary.py'
            }
        }
        
        // --- 1. Multi-tenancy Test Suite ---
        stage('Run Multi-tenancy Tests (Isolation)') {
            steps {
                echo 'Starting Multi-tenancy Isolation checks...'
                // Run the test suite and save results to a unique subdirectory
                sh "robot ${ROBOT_OPTIONS}/MT TestSuit_MultiTenancy.robot"
            }
            post {
                failure {
                    echo 'Multi-tenancy tests failed. Stopping pipeline.'
                }
            }
        }
        
        // --- 2. Utils Test Suite (Provisioning & FS Commands) ---
        stage('Run Utils Tests (Tools & Filesystem)') {
            steps {
                echo 'Starting Utility and Filesystem command checks...'
                sh "robot ${ROBOT_OPTIONS}/UT TestSuit_Utils.robot"
            }
        }
        
        // --- 3. Hardware and VM Config Test Suite ---
        stage('Run Config Tests (Limits & Snapshot)') {
            steps {
                echo 'Starting Hardware and VM Configuration checks...'
                sh "robot ${ROBOT_OPTIONS}/CFG TestSuit_HardwareAndVMConfig.robot"
            }
        }
        
        // --- 4. Redundancy Checks Test Suite ---
        stage('Run Redundancy Tests (HA & Failover)') {
            steps {
                echo 'Starting Redundancy and Failover checks...'
                sh "robot ${ROBOT_OPTIONS}/RDY TestSuit_RedundancyChecks.robot"
            }
        }
    }
    
    post {
        always {
            // Archive all generated reports regardless of the test result
            archiveArtifacts artifacts: 'Reports/**/*'
            
            // Publish test results to Jenkins UI (requires Junit Plugin)
            junit 'Reports/**/*.xml' 
            
            echo 'Robot Framework execution finished.'
        }
    }
}
