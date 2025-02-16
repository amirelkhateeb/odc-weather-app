pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "amirelkhateeb/weatherapp:latest"
        RECIPIENT_EMAIL = 'amirellkhateeb@gmail.com'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // استخدم الـ credentialsId الصحيح
                git credentialsId: 'secret-github', url: 'https://github.com/amirelkhateeb/weather-app.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // تحقق من وجود Docker
                    sh 'docker --version'
                    // بناء الصورة
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_hub_credentials', usernameVariable: 'DOCKERHUB_CREDENTIALS_USR', passwordVariable: 'DOCKERHUB_CREDENTIALS_PSW')]) {
                    sh '''
                        echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                        docker push ${DOCKER_IMAGE}
                    '''
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                script {
                    // تحقق من وجود Ansible
                    sh 'ansible --version'
                    // تأكد من وجود المفاتيح الخاصة
                    sh '''
                        cd ansible
                        if [ -f private_key_m01 ] && [ -f private_key_m02 ]; then
                            chmod 600 private_key_m01
                            chmod 600 private_key_m02
                            ansible-playbook -i inventory playbook.yml
                        else
                            echo "Error: Private keys not found!"
                            exit 1
                        fi
                    '''
                }
            }
        }
    }

    post {
        success {
            emailext (
                subject: "✅ Jenkins Build Successful: ${env.JOB_NAME}",
                body: """
                <h3>Jenkins Build Successful</h3>
                <p>The Jenkins build for <b>${env.JOB_NAME}</b> completed successfully. 🎉</p>
                <p>Build URL: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                """,
                mimeType: 'text/html',
                to: RECIPIENT_EMAIL
            )
        }
        failure {
            emailext (
                subject: "❌ Jenkins Build Failed: ${env.JOB_NAME}",
                body: """
                <h3>Jenkins Build Failed</h3>
                <p>The Jenkins build for <b>${env.JOB_NAME}</b> has failed. ⚠️</p>
                <p>Check the logs here: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                """,
                mimeType: 'text/html',
                to: RECIPIENT_EMAIL
            )
        }
    }
}
