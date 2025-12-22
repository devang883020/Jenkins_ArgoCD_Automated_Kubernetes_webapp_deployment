pipeline {
    agent any

    environment {
        IMAGE_NAME = "devangkubde88/webapp"
        GITOPS_PATH = "automated-k8s-cicd/helm/myapp/values.yaml"
        DOCKER_CREDS = "dockerhub-cred"
        GIT_CREDS = "github-creds"
    }

    stages {

        stage('Checkout SCM') {
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

                    echo "Commit message detected: ${env.COMMIT_MSG}"
                }
            }
        }

        stage('Check if App Code Changed') {
            steps {
                script {
                    def changed = sh(
                        script: "git diff --name-only HEAD~1 HEAD | grep -E '^automated-k8s-cicd/app/main.py\$' || true",
                        returnStdout: true
                    ).trim()

                    if (changed) {
                        env.CODE_CHANGED = "true"
                    } else {
                        env.CODE_CHANGED = "false"
                    }

                    echo "Code changed: ${env.CODE_CHANGED}"
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.CODE_CHANGED == "true" }
            }
            steps {
                sh """
                  docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                  -f automated-k8s-cicd/Dockerfile automated-k8s-cicd
                """
            }
        }

        stage('Login to DockerHub') {
            when {
                expression { env.CODE_CHANGED == "true" }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.CODE_CHANGED == "true" }
            }
            steps {
                sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('Update Helm values.yaml & Push (GitOps)') {
            when {
                expression {
                    env.CODE_CHANGED == "true" &&
                    !env.COMMIT_MSG.startsWith("ci:")
                }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh '''
                      # Configure git
                      git config user.name "jenkins"
                      git config user.email "jenkins@ci.local"

                      # Ensure we're on the main branch (not detached HEAD)
                      git checkout main

                      # Pull latest changes from remote
                      git pull https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git main

                      # Now update the values.yaml file
                      sed -i "s|tag:.*|tag: ${BUILD_NUMBER}|" ${GITOPS_PATH}

                      # Stage and commit the changes
                      git add ${GITOPS_PATH}
                      git commit -m "ci: update image tag to ${BUILD_NUMBER}"

                      # Push to remote
                      git push https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ CI completed. ArgoCD will sync automatically."
        }
        failure {
            echo "❌ CI failed."
        }
    }
}