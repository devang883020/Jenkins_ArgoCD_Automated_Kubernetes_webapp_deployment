pipeline {

    agent any

    environment {
        IMAGE_NAME = "devangkubde88/webapp"
        AWS_REGION = "ap-south-1"
        CLUSTER_NAME = "my-eks-cluster"
        GIT_CREDENTIALS_ID = "github-creds"
        COMMIT_MSG = ""
    }

    stages {

        /* ===================== ADDED (REQUIRED) ===================== */
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git fetch --unshallow || true'
            }
        }

        stage('Read Commit Message') {
            steps {
                script {
                    env.COMMIT_MSG = sh(
                        script: "git log -1 --pretty=%B",
                        returnStdout: true
                    ).trim()
                    echo "Commit Message: ${env.COMMIT_MSG}"
                }
            }
        }
        /* ============================================================= */

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} automated-k8s-cicd/
                '''
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Configure AWS & EKS') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    sh '''
                    aws sts get-caller-identity
                    aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}
                    kubectl get nodes
                    '''
                }
            }
        }

        
        /* ===================== MODIFIED (ONLY WHEN) ===================== */
        stage('Update Helm values.yaml (GitOps)') {
            when {
                expression {
                    !env.COMMIT_MSG.startsWith("ci:")
                }
            }
            steps {
                sh '''
                sed -i "s|tag:.*|tag: ${BUILD_NUMBER}|" automated-k8s-cicd/helm/myapp/values.yaml
                '''
            }
        }
        /* ================================================================ */

        stage('Push Git Changes') {
            when {
                expression {
                    !env.COMMIT_MSG.startsWith("ci:")
                }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${GIT_CREDENTIALS_ID}",
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh '''
                    git config user.name "jenkins"
                    git config user.email "jenkins@ci.local"

                    git add automated-k8s-cicd/helm/myapp/values.yaml
                    git commit -m "ci: update image tag to ${BUILD_NUMBER}" || echo "No changes"

                    git pull --rebase https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git main
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
