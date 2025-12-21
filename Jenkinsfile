pipeline {
    agent any

    environment {
        IMAGE_NAME = "devangkubde88/webapp"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Read Commit Message') {
            steps {
                script {
                    env.COMMIT_MSG = sh(
                        script: "git log -1 --pretty=%B",
                        returnStdout: true
                    ).trim()

                    echo "Commit message detected: ${COMMIT_MSG}"
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { !COMMIT_MSG.startsWith("ci:") }
            }
            steps {
                steps {
                    sh """
                      docker build -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        -f ../automated-k8s-cicd/Dockerfile \
                        ../automated-k8s-cicd
                    """
                }
            }
        }

        stage('Login to DockerHub') {
            when {
                expression { !env.COMMIT_MSG.startsWith("ci:") }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                      echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                    """
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { !env.COMMIT_MSG.startsWith("ci:") }
            }
            steps {
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Update Helm values.yaml (GitOps)') {
            when {
                expression { !env.COMMIT_MSG.startsWith("ci:") }
            }
            steps {
                sh """
                  sed -i 's|repository:.*|repository: ${IMAGE_NAME}|' automated-k8s-cicd/helm/myapp/values.yaml
                  sed -i 's|tag:.*|tag: \"${IMAGE_TAG}\"|' automated-k8s-cicd/helm/myapp/values.yaml
                """
            }
        }

        stage('Commit & Push GitOps Change') {
            when {
                expression { !env.COMMIT_MSG.startsWith("ci:") }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh """
                      git config user.name "jenkins"
                      git config user.email "jenkins@ci.local"

                      git add automated-k8s-cicd/helm/myapp/values.yaml
                      git commit -m "ci: update image tag to ${IMAGE_TAG}" || echo "No changes to commit"

                      git pull --rebase https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git main
                      git push https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git main
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ CI finished. ArgoCD will reconcile the cluster."
        }
        failure {
            echo "❌ CI failed."
        }
    }
}
