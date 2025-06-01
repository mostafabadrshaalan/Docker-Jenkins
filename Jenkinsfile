// TestDocker/Jenkinsfile
pipeline {
    agent any // Or specify a label for an agent with Docker & Docker Compose installed

    environment {
        COMPOSE_FILE_BASE = "docker-compose.yml"          // For mongo, mongo-express, and base app config
        COMPOSE_FILE_DEV_OVERRIDE = "docker-compose-dev.yml" // For app's dev build target and volume mount
        PROJECT_NAME = "testdocker" // Used for potential volume cleanup if needed
    }

    stages {
        stage('Checkout') {
            steps {
                // This will checkout from the SCM configured in the Jenkins job
                checkout scm
            }
        }

        stage('Build Development App Image') {
            steps {
                script {
                    echo "Building python-app using 'development' target..."
                    // docker-compose-dev.yml specifies `target: development`.
                    // This command builds only the python-app service image.
                    sh "docker-compose -f ${COMPOSE_FILE_DEV_OVERRIDE} build python-app"
                    echo "Development image for python-app built."
                }
            }
        }

        stage('Run Tests (Start App & Check Endpoint)') {
            // This stage will spin up the app (using dev build) and mongo,
            // then perform a simple check.
            steps {
                script {
                    echo "Starting services for testing..."
                    // Use both compose files. docker-compose-dev.yml will override python-app specifics.
                    // `--build python-app` ensures the latest dev image is used.
                    // `-V` recreates anonymous volumes.
                    sh "docker-compose -f ${COMPOSE_FILE_BASE} -f ${COMPOSE_FILE_DEV_OVERRIDE} up -d --build python-app -V"

                    echo "Waiting for app to start (up to 30 seconds)..."
                    // Simple health check loop for the app
                    // Port 4000 is from your .env and docker-compose.yml
                    timeout(time: 30, unit: 'SECONDS') {
                        sh """
                            count=0
                            until curl -sf http://localhost:4000/; do
                                sleep 5
                                count=\$((count+1))
                                if [ "\$count" -ge 6 ]; then
                                    echo "App did not start in time."
                                    # Capture logs if app fails to start
                                    docker-compose -f ${COMPOSE_FILE_BASE} -f ${COMPOSE_FILE_DEV_OVERRIDE} logs python-app
                                    exit 1
                                fi
                                echo "Retrying curl to http://localhost:4000/..."
                            done
                            echo "App is responding at http://localhost:4000/!"
                        """
                    }
                    // You can add more specific test commands here if you have them, e.g.:
                    // sh "docker-compose -f ${COMPOSE_FILE_DEV_OVERRIDE} exec -T python-app pytest"
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Cleaning up services..."
                // Always bring down the services after the pipeline.
                // `--remove-orphans` removes containers for services not defined in the files.
                // `-v` removes anonymous volumes associated with the containers.
                // The named volume 'mongo-db' will NOT be removed by default with `down -v`.
                // This is generally fine, but if you need a fresh DB for every CI run,
                // you might consider not using a named volume for mongo in a CI-specific compose file
                // or explicitly removing it.
                sh "docker-compose -f ${COMPOSE_FILE_BASE} -f ${COMPOSE_FILE_DEV_OVERRIDE} down --remove-orphans -v || true"

                // Optional: If you want to ensure the named mongo volume is also cleaned for CI:
                // echo "Removing named volume ${PROJECT_NAME}_mongo-db if it exists..."
                // sh "docker volume rm ${PROJECT_NAME}_mongo-db || true"
                // Note: Docker Compose prepends the project directory name (lowercase) to volume names.
                // If your Jenkins workspace is /var/lib/jenkins/workspace/TestDocker-CI-Build,
                // the project name might be 'testdocker-ci-build' or similar,
                // so the volume could be 'testdocker-ci-build_mongo-db'.
                // You can find the exact name with `docker volume ls`.
                // For simplicity, we'll assume `testdocker_mongo-db` if you're running from TestDocker directory.
                // A more robust way is `docker-compose -p ${PROJECT_NAME} ... down -v --remove-orphans`
                // and `docker volume rm ${PROJECT_NAME}_mongo-db`.
                // The `-p` flag sets the project name explicitly.

                echo "Cleanup finished."
            }
        }
        success {
            script {
                echo "CI Build & Test Pipeline executed successfully!"
            }
        }
        failure {
            script {
                echo "CI Build & Test Pipeline failed!"
                // Capture logs on failure for all services
                sh "docker-compose -f ${COMPOSE_FILE_BASE} -f ${COMPOSE_FILE_DEV_OVERRIDE} logs --tail='100' || true"
            }
        }
    }
}