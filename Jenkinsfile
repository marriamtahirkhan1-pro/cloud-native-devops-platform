pipeline {
    agent any

    environment {
        PATH = "/var/jenkins_home/.local/bin:${env.PATH}"
        DATABASE_URL = "postgresql://taskuser:taskpassword@host.docker.internal:5432/taskdb"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --user -r app/requirements.txt --break-system-packages
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "Running tests with PostgreSQL..."
                    python3 -m pytest -v
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv(
                        installationName: 'SonarQube',
                        credentialsId: 'sonarqube-token-global'
                    ) {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.login="\$SONAR_AUTH_TOKEN"
                        """
                    }
                }
            }
        }
    }
}