pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                
                git branch: 'main', url: 'https://github.com/MurtazaSajid/dental-clinic.git'
            }
        }

        stage('Syntax Check (Docker Pipeline)') {
            steps {
                script {
                    docker.image('python:3.11-slim').inside {
                        sh 'python -m py_compile app.py'
                    }
                }
            }
        }

        stage('Build & Run Containers') {
            steps {
                sh 'docker compose -f docker-compose-jenkins.yml down || true'
                sh 'docker compose -f docker-compose-jenkins.yml up -d'
            }
        }

        stage('Verify') {
            steps {
                sh 'sleep 25'
                sh 'docker ps'
                sh 'curl -f http://localhost:8081/health || (docker logs ci_dental_web; exit 1)'
            }
        }
    }
}
