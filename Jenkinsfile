pipeline {
    agent any

    environment {
        IMAGE_NAME = "devangkubde88/webapp"
        GITOPS_PATH = "automated-k8s-cicd/helm/myapp/values.yaml"
        DOCKER_CREDS = "dockerhub-creds"
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
                    COMMIT_MSG = sh(
                        script: "git log -1 --pretty=%B",
                        returnStdout: true
                    ).trim()

                    echo "Commit message detected: ${COMMIT_MSG}"
                }
            }
        }

        stage('Check if App Code Changed') {
            steps {
                script {
                    CODE_CHANGED = sh(
                        script: "git diff --name-only HEAD~1 HEAD | grep -E '^main.py' || true",
                        returnStdout: true
                    ).trim()

                    echo "Code changed: ${CODE_CHANGED}"
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { CODE_CHANGED != "" }
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
                expression { CODE_CHANGED != "" }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: dockerhub-cred,
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { CODE_CHANGED != "" }
            }
            steps {
                sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('Update Helm values.yaml (GitOps)') {
            when {
                expression {
                    CODE_CHANGED != "" &&
                    !COMMIT_MSG.startsWith("ci:")
                }
            }
            steps {
                sh """
                  sed -i 's|tag:.*|tag: ${BUILD_NUMBER}|' ${GITOPS_PATH}
                """
            }
        }

        stage('Commit & Push GitOps Change') {
            when {
                expression {
                    CODE_CHANGED != "" &&
                    !COMMIT_MSG.startsWith("ci:")
                }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: github-creds,
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh """
                      git config user.name "jenkins"
                      git config user.email "jenkins@ci.local"

                      git add ${GITOPS_PATH}
                      git commit -m "ci: update image tag to ${BUILD_NUMBER}"

                      git pull --rebase https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git main
                      git push https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git main
                    """
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
