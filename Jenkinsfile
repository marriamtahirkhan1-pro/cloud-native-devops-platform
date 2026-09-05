pipeline {
    agent any

    tools {
        sonarQube 'SonarScanner'
    }

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
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=cloud-native-devops-platform \
                          -Dsonar.sources=app
                    '''
                }
            }
        }
    }
}