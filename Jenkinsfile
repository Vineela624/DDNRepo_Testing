pipeline {
    // 🚨 FIX IS HERE: The agent type 'any' must be inside the braces.
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
                // Ensure Python/pip is available on the agent running this
                sh 'pip install robotframework'
                sh 'pip install robotframework-seleniumlibrary' 
                sh 'mkdir -p Reports' 
                sh 'ls -l TestAutomationLibrary.py'
            }
        }
        
        // ... (Remaining stages for Robot Framework execution) ...
        // ... (Post block for archiving/reporting) ...
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'Reports/**/*'
            junit 'Reports/**/*.xml' 
            echo 'Robot Framework execution finished.'
        }
    }
}
