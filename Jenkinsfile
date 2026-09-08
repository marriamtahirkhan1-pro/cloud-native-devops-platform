pipeline {
    agent any

    environment {
        PATH = "/var/jenkins_home/.local/bin:${env.PATH}"

        AWS_REGION = "us-east-1"
        AWS_ACCOUNT_ID = "792811916398"

        ECR_REPOSITORY = "cloud-native-devops-platform"
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        EKS_CLUSTER = "cloud-native-devops"
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
                    python3 -m pip install \
                      --user \
                      -r app/requirements.txt \
                      --break-system-packages
                '''
            }
        }

        stage('Run Tests') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'postgres-database-url',
                        variable: 'DATABASE_URL'
                    )
                ]) {
                    sh '''
                        echo "Running tests with PostgreSQL..."
                        python3 -m pytest -v
                    '''
                }
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
                    docker build \
                      -t cloud-native-devops-platform:${BUILD_NUMBER} \
                      -t cloud-native-devops-platform:latest \
                      .
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
                        aws ecr get-login-password \
                          --region $AWS_REGION | \
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
                      cloud-native-devops-platform:${BUILD_NUMBER} \
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
                    docker push \
                      $ECR_REGISTRY/$ECR_REPOSITORY:${BUILD_NUMBER}

                    docker push \
                      $ECR_REGISTRY/$ECR_REPOSITORY:latest
                '''
            }
        }

        stage('Deploy to Amazon EKS') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-eks-deploy-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        echo "Configuring access to Amazon EKS..."

                        aws eks update-kubeconfig \
                          --region $AWS_REGION \
                          --name $EKS_CLUSTER

                        echo "Deploying image build ${BUILD_NUMBER}..."

                        kubectl set image \
                          deployment/cloud-native-devops-platform \
                          app=$ECR_REGISTRY/$ECR_REPOSITORY:${BUILD_NUMBER}

                        echo "Waiting for Kubernetes rollout..."

                        kubectl rollout status \
                          deployment/cloud-native-devops-platform \
                          --timeout=180s

                        echo "EKS deployment completed successfully."
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-eks-deploy-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        aws eks update-kubeconfig \
                          --region $AWS_REGION \
                          --name $EKS_CLUSTER

                        echo "Application Pods:"
                        kubectl get pods \
                          -l app=cloud-native-devops-platform

                        echo "Application Service:"
                        kubectl get service cloud-native-devops-service
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }

        failure {
            echo 'CI/CD pipeline failed. Check the failed stage logs.'
        }

        always {
            sh '''
                docker logout $ECR_REGISTRY || true
            '''
        }
    }
}