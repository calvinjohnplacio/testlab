pipeline {
    agent any
    environment {
        GIT_REPO_URL = 'https://github.com/calvinjohnplacio/testlab.git'
        GIT_CREDENTIALS_ID = 'github-pat2'
        GIT_BRANCH = 'main'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: "*/${env.GIT_BRANCH}"]], userRemoteConfigs: [[url: "${env.GIT_REPO_URL}", credentialsId: "${env.GIT_CREDENTIALS_ID}"]]])
            }
        }
        stage('Detect Change') {
            steps {
                script {
                    def changed = sh(script: "git diff --name-only HEAD~1 HEAD | grep '.php' | head -n 1", returnStdout: true).trim()
                    env.TARGET_PHP_FILE = changed ?: "index.php"
                }
            }
        }
        stage('Stage & Force Verbose Errors') {
            steps {
                sh '''
                sudo mkdir -p /var/www/html/staging
                sudo rsync -av --delete --exclude='venv/' --exclude='.git/' ./ /var/www/html/staging/
                
                # This forces PHP to show errors even if the main php.ini says no
                echo "php_flag display_errors On" | sudo tee /var/www/html/staging/.htaccess
                echo "php_value error_reporting 32767" | sudo tee -a /var/www/html/staging/.htaccess
                
                sudo chown -R www-data:www-data /var/www/html/staging
                '''
            }
        }
        stage('Run Strict Test') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install selenium
                python3 test.py
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                # Only runs if test.py exited with 0
                sudo rsync -av --delete --exclude='venv/' --exclude='.git/' --exclude='staging/' ./ /var/www/html/
                sudo chown -R www-data:www-data /var/www/html/
                '''
            }
        }
    }
}
