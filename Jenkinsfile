// TestDocker/Jenkinsfile
pipeline {
    agent any // Run on any available agent

    stages {
        stage('Checkout') {
            steps {
                // This will checkout from the SCM configured in the Jenkins job
                echo "Checking out source code..."
                checkout scm
                echo "Source code checked out successfully."
                echo "Current commit details:"
                sh 'git log -1 --pretty=%B' // Print the last commit message
            }
        }

        stage('Simple Build Step') {
            steps {
                echo "This is a simple build step."
                echo "Simulating a build process..."
                // As a placeholder, list files in the workspace
                sh 'ls -la'
                echo "If app.py exists, print its first few lines:"
                sh 'if [ -f app.py ]; then head -n 5 app.py; else echo "app.py not found"; fi'
                echo "Simple build step completed."
            }
        }
    }

    post {
        always {
            script {
                echo "Pipeline finished."
            }
        }
        success {
            script {
                echo "Basic CI Pipeline executed successfully!"
            }
        }
        failure {
            script {
                echo "Basic CI Pipeline failed!"
            }
        }
    }
}