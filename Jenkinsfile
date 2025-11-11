// Jenkinsfile (Declarative Pipeline)
pipeline {
    // CORRECT: Specifying the 'any' agent type inside the block
    agent {
        any 
    }

    // Define environment variables
    environment {
        ROBOT_OPTIONS = "--outputdir Reports --logtitle 'Robot Framework Execution Log'"
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo 'Installing Robot Framework dependencies...'
                // Install dependencies. Ensure Python/pip is available on the 'any' agent.
                sh 'pip install robotframework'
                sh 'pip install robotframework-seleniumlibrary' 
                sh 'mkdir -p Reports' 
                sh 'ls -l TestAutomationLibrary.py' // Check for the library
            }
        }
        
        // 1. Multi-tenancy Test Suite
        stage('Run Multi-tenancy Tests (Isolation)') {
            steps {
                echo 'Starting Multi-tenancy Isolation checks...'
                sh "robot ${ROBOT_OPTIONS}/MT TestSuit_MultiTenancy.robot"
            }
        }
        
        // 2. Utils Test Suite
        stage('Run Utils Tests (Tools & Filesystem)') {
            steps {
                echo 'Starting Utility and Filesystem command checks...'
                sh "robot ${ROBOT_OPTIONS}/UT TestSuit_Utils.robot"
            }
        }
        
        // 3. Hardware and VM Config Test Suite
        stage('Run Config Tests (Limits & Snapshot)') {
            steps {
                echo 'Starting Hardware and VM Configuration checks...'
                sh "robot ${ROBOT_OPTIONS}/CFG TestSuit_HardwareAndVMConfig.robot"
            }
        }
        
        // 4. Redundancy Checks Test Suite
        stage('Run Redundancy Tests (HA & Failover)') {
            steps {
                echo 'Starting Redundancy and Failover checks...'
                sh "robot ${ROBOT_OPTIONS}/RDY TestSuit_RedundancyChecks.robot"
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'Reports/**/*'
            junit 'Reports/**/*.xml' 
            echo 'Robot Framework execution finished.'
        }
    }
}
