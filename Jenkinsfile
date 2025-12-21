pipeline {
    agent any

    environment {
        AWS_REGION      = "ap-south-1"
        EKS_CLUSTER     = "my-eks-cluster"
        IMAGE_REPO      = "devangkubde88/webapp"
        GIT_REPO_URL    = "https://github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git"
        HELM_VALUES     = "automated-k8s-cicd/helm/myapp/values.yaml"
    }

    options {
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                  docker build -t ${IMAGE_REPO}:${BUILD_NUMBER} automated-k8s-cicd/
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                      docker push ${IMAGE_REPO}:${BUILD_NUMBER}
                    '''
                }
            }
        }

        stage('Update Helm values.yaml (GitOps)') {
            when {
                not {
                    changelog 'ci: update image tag*'
                }
            }
            steps {
                sh '''
                  git config user.name "jenkins"
git config user.email "jenkins@ci.local"

# 🔑 CRITICAL FIX
git checkout main

# Always sync first
git pull --rebase origin main

# Update values.yaml using yq (Option A)
yq e -i '.image.repository = "devangkubde88/webapp"' automated-k8s-cicd/helm/myapp/values.yaml
yq e -i '.image.tag = "'"${BUILD_NUMBER}"'"' automated-k8s-cicd/helm/myapp/values.yaml

git add automated-k8s-cicd/helm/myapp/values.yaml
git commit -m "ci: update image tag to ${BUILD_NUMBER}" || echo "No changes"

git push origin main
                '''
            }
        }

        stage('Push Git Changes') {
            when {
                not {
                    changelog 'ci: update image tag*'
                }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh '''
                      git pull --rebase ${GIT_REPO_URL} main
                      git push https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ CI completed. ArgoCD will auto-sync the deployment."
        }
        failure {
            echo "❌ CI failed."
        }
    }
}
