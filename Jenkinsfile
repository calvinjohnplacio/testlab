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
                    // Detect changed PHP file
                    def changed = sh(script: "git diff --name-only HEAD~1 HEAD | grep '.php' | head -n 1", returnStdout: true).trim()
                    env.TARGET_PHP_FILE = changed ?: "index.php"
                    echo "Targeting: ${env.TARGET_PHP_FILE}"
                }
            }
        }

        stage('Stage & Force Errors') {
            steps {
                sh '''
                sudo mkdir -p /var/www/html/staging
                # Sync everything EXCEPT environment files
                sudo rsync -av --delete --exclude='venv/' --exclude='.git/' ./ /var/www/html/staging/
                
                # STRICT MODE: Force PHP to display errors in the staging area
                # We create a local .user.ini for PHP to override global settings
                echo "display_errors=On" | sudo tee /var/www/html/staging/.user.ini
                echo "error_reporting=E_ALL" | sudo tee -a /var/www/html/staging/.user.ini
                
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
            // This ONLY runs if Python returns exit code 0
            steps {
                sh '''
                sudo rsync -av --delete --exclude='venv/' --exclude='.git/' --exclude='staging/' ./ /var/www/html/
                sudo rm -f /var/www/html/.user.ini
                sudo chown -R www-data:www-data /var/www/html/
                '''
            }
        }
    }

    post {
        failure {
            echo "❌ Build Failed: Errors found in ${env.TARGET_PHP_FILE}. Deployment aborted."
        }
    }
}
