pipeline {
    agent any

    environment {
        PATH = "/var/jenkins_home/.local/bin:${env.PATH}"
        DATABASE_URL = "postgresql://taskuser:taskpassword@host.docker.internal:5432/taskdb"

        AWS_REGION = "us-east-1"
        AWS_ACCOUNT_ID = "792811916398"
        ECR_REPOSITORY = "cloud-native-devops-platform"
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
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

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t cloud-native-devops-platform:latest .
                '''
            }
        }

        stage('AWS ECR Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-ecr-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        aws ecr get-login-password --region $AWS_REGION | \
                        docker login \
                        --username AWS \
                        --password-stdin $ECR_REGISTRY
                    '''
                }
            }
        }

        stage('Docker Tag') {
            steps {
                sh '''
                    docker tag \
                    cloud-native-devops-platform:latest \
                    $ECR_REGISTRY/$ECR_REPOSITORY:${BUILD_NUMBER}

                    docker tag \
                    cloud-native-devops-platform:latest \
                    $ECR_REGISTRY/$ECR_REPOSITORY:latest
                '''
            }
        }

        stage('Push to AWS ECR') {
            steps {
                sh '''
                    docker push $ECR_REGISTRY/$ECR_REPOSITORY:${BUILD_NUMBER}
                    docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
                '''
            }
        }
    }
}