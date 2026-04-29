pipeline {
    agent any

    environment {
        GIT_REPO_URL = 'https://github.com/calvinjohnplacio/testlab.git'
        GIT_CREDENTIALS_ID = 'github-pat'
        GIT_BRANCH = 'main'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${env.GIT_BRANCH}"]],
                    userRemoteConfigs: [[
                        url: "${env.GIT_REPO_URL}",
                        credentialsId: "${env.GIT_CREDENTIALS_ID}"
                    ]]
                ])
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Test') {
            steps {
                sh '''
                . venv/bin/activate
                python test.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                rsync -av --delete ./ /var/www/html/
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS ✔"
        }
        failure {
            echo "FAILED ❌"
        }
        always {
            cleanWs()
        }
    }
}

