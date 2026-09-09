Cloud Native DevOps Platform
============================

A practical cloud-native DevOps project built to demonstrate how an application can move from source code to a running and monitored Kubernetes environment through an automated CI/CD pipeline.

The project uses a FastAPI application with PostgreSQL and connects GitHub, Jenkins, SonarQube, Docker, AWS ECR and Amazon EKS into one complete deployment workflow. Prometheus and Grafana are used to monitor the Kubernetes environment.

Project Overview
================

The main goal of this project was to build a complete DevOps workflow rather than work with each tool separately.

The deployment flow is:

Developer → GitHub → Jenkins → Tests → SonarQube → Docker → AWS ECR → Amazon EKS → LoadBalancer → FastAPI

Monitoring flow:

Amazon EKS → Prometheus → Grafana

When new code is processed by Jenkins, the pipeline runs the tests, performs SonarQube analysis, builds the Docker image, pushes it to Amazon ECR and deploys the updated image to the EKS cluster.

Technology Stack
================

| Technology | Used For |
|---|---|
| Linux | Development and command-line environment |
| Git & GitHub | Version control and source code |
| Jenkins | CI/CD automation |
| Python / FastAPI | REST API |
| PostgreSQL | Application database |
| Pytest | Automated testing |
| SonarQube | Code quality analysis |
| Docker | Application containerization |
| AWS ECR | Docker image registry |
| Amazon EKS | Managed Kubernetes environment |
| Kubernetes | Application orchestration |
| AWS Load Balancer | Public application access |
| Prometheus | Infrastructure metrics |
| Grafana | Monitoring dashboards |
| Helm | Prometheus and Grafana deployment |

Architecture
============

Developer
    |
    v
GitHub
    |
    v
Jenkins
    |
    +------> Automated Tests
    |
    +------> SonarQube
    |
    v
Docker Build
    |
    v
Amazon ECR
    |
    v
Amazon EKS
    |
    +------> FastAPI
    |
    +------> PostgreSQL
    |
    v
AWS Load Balancer
    |
    v
Users


Monitoring

Amazon EKS
    |
    v
Prometheus
    |
    v
Grafana


CI/CD Pipeline
==============

The Jenkins pipeline handles the deployment process in the following order:

1. Checkout the latest code from GitHub
2. Install application dependencies
3. Run automated tests with Pytest
4. Run SonarQube code analysis
5. Build the Docker image
6. Authenticate with Amazon ECR
7. Tag the image with the Jenkins build number
8. Push the image to Amazon ECR
9. Deploy the new image to Amazon EKS
10. Verify the Kubernetes deployment

Using the Jenkins build number as the Docker image tag also makes it easier to identify which application build was deployed.

Application and Kubernetes
==========================

The application is a FastAPI REST API backed by PostgreSQL.

Both services run inside the Kubernetes environment. PostgreSQL is available internally through a Kubernetes service, while the FastAPI application is exposed through an AWS Load Balancer.

The Kubernetes configuration includes:

- FastAPI deployment
- PostgreSQL deployment
- Internal PostgreSQL service
- Public LoadBalancer service
- Kubernetes Secrets for database configuration
- Automated deployment from Jenkins

Docker and Amazon ECR
=====================

The application is packaged into a Docker image during the Jenkins pipeline.

Each successful pipeline build pushes a versioned image to the private Amazon ECR repository. A `latest` tag is also maintained.

For example, Jenkins Build 9 produced an ECR image tagged as:


9
latest


This makes the relationship between a Jenkins build and its container image easy to follow.

Code Quality
============

SonarQube is part of the Jenkins pipeline rather than being run manually.

The latest verified analysis passed the SonarQube Quality Gate with:

- 0 Bugs
- 0 Vulnerabilities
- 0 Security Hotspots
- 0 Code Smells

Monitoring
==========

Prometheus collects metrics from the Kubernetes environment and Grafana is used to visualize them.

The monitoring setup provides information such as:

- CPU usage
- Memory usage
- Node metrics
- Container metrics
- Resource allocation
- Filesystem usage

This makes it possible to check the health and resource usage of the EKS environment from Grafana.

Security
========

Security was also improved during the project instead of keeping development credentials directly in the repository.

The current setup includes:

- Sensitive `.env` values excluded from Git
- Kubernetes Secrets for database credentials
- Jenkins Credentials for CI/CD secrets
- Dedicated IAM user for Jenkins ECR access
- Dedicated IAM user for Jenkins EKS deployment
- ECR permissions limited to the project repository
- EKS deployment permissions reduced to the required AWS access
- Real credentials excluded from example Kubernetes secret files
- Previously exposed development credentials removed from Git history

FastAPI API
===========

The application provides a small task-management REST API.

Available endpoints include:

GET     /health
GET     /
GET     /api/tasks
POST    /api/tasks
GET     /api/tasks/{task_id}
PUT     /api/tasks/{task_id}
DELETE  /api/tasks/{task_id}


FastAPI also provides interactive Swagger documentation through:

/docs


Project Structure
=================

cloud-native-devops-platform/
|
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   └── ...
|
├── k8s/
│   ├── deployment.yaml
│   ├── postgres.yaml
│   ├── service.yaml
│   └── secrets.example.yaml
|
├── Dockerfile
├── Dockerfile.jenkins
├── docker-compose.yml
├── Jenkinsfile
├── sonar-project.properties
├── .gitignore
└── README.md


Current Status
==============

The main project workflow is complete and has been tested end to end.

Completed work includes:

- GitHub source control
- Jenkins CI/CD pipeline
- Automated Pytest testing
- SonarQube integration
- Docker containerization
- AWS ECR integration
- Amazon EKS deployment
- Kubernetes application and PostgreSQL deployment
- AWS Load Balancer
- Prometheus monitoring
- Grafana dashboards
- Jenkins credential management
- IAM permission hardening
- Git secret cleanup

The latest verified Jenkins pipeline run is Build 9, which completed successfully and passed the SonarQube Quality Gate.

What I Learned
==============

This project gave me practical experience connecting multiple DevOps tools into one working workflow.

Instead of only deploying an application, I worked through CI/CD automation, container image management, Kubernetes deployment, cloud permissions, secret handling, troubleshooting, monitoring and application verification.

The project also involved solving real deployment problems such as Kubernetes pod scheduling limits, EKS worker-node recovery, CI/CD credential issues and IAM permission cleanup.

Author
======

Marriam Khan

DevOps Engineer