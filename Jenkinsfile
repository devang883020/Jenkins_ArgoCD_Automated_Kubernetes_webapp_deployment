pipeline {
    agent any

    environment {
        IMAGE_NAME = "devangkubde88/webapp"
        GITOPS_PATH = "automated-k8s-cicd/helm/myapp/values.yaml"
        DOCKER_CREDS = "dockerhub-cred"
        GIT_CREDS = "github-creds"
        CODE_CHANGED = "false"
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
                        script: "git diff --name-only HEAD~1 HEAD | grep -E '^automated-k8s-cicd/app/main.py|^automated-k8s-cicd/main.py' || true",
                        returnStdout: true
                    ).trim()
                    
                    if (changed) {
                        env.CODE_CHANGED = "true"
                        echo "✅ Main.py file changed. Will build new Docker image."
                    } else {
                        env.CODE_CHANGED = "false"
                        echo "⏭️ No changes in main.py. Skipping build."
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { 
                    return env.CODE_CHANGED == "true" 
                }
            }
            steps {
                script {
                    echo "Building Docker image with tag: ${BUILD_NUMBER}"
                    sh """
                        docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                        -f automated-k8s-cicd/Dockerfile automated-k8s-cicd
                    """
                }
            }
        }

        stage('Login to DockerHub') {
            when {
                expression { 
                    return env.CODE_CHANGED == "true" 
                }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',  // Fixed: Added quotes
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { 
                    return env.CODE_CHANGED == "true" 
                }
            }
            steps {
                script {
                    echo "Pushing Docker image: ${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }

        stage('Update Helm values.yaml (GitOps)') {
            when {
                expression { 
                    return env.CODE_CHANGED == "true" && 
                           env.COMMIT_MSG != null &&
                           !env.COMMIT_MSG.startsWith("ci:")
                }
            }
            steps {
                script {
                    echo "Updating Helm values.yaml with new image tag"
                    sh """
                        sed -i 's|tag:.*|tag: "${BUILD_NUMBER}"|' ${GITOPS_PATH}
                        echo "Updated ${GITOPS_PATH} with tag: ${BUILD_NUMBER}"
                    """
                }
            }
        }

        stage('Commit & Push GitOps Change') {
            when {
                expression { 
                    return env.CODE_CHANGED == "true" && 
                           env.COMMIT_MSG != null &&
                           !env.COMMIT_MSG.startsWith("ci:")
                }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',  // Fixed: Added quotes
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    script {
                        echo "Committing and pushing GitOps changes"
                        sh """
                            git config user.name "jenkins"
                            git config user.email "jenkins@ci.local"
                            
                            git add ${GITOPS_PATH}
                            git commit -m "ci: update image tag to ${BUILD_NUMBER}"
                            
                            # Set remote URL with credentials
                            git remote set-url origin https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git
                            
                            git pull --rebase origin main
                            git push origin main
                        """
                    }
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
        always {
            script {
                echo "Pipeline completed with status: ${currentBuild.result}"
                echo "CODE_CHANGED: ${env.CODE_CHANGED}"
                echo "COMMIT_MSG: ${env.COMMIT_MSG}"
            }
        }
    }
}
