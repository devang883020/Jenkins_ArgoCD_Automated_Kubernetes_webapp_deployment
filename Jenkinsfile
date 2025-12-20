pipeline {
    agent any

    environment {
        AWS_REGION   = "ap-south-1"
        CLUSTER_NAME = "my-eks-cluster"
        IMAGE_NAME   = "devangkubde88/webapp"
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        /* =======================
           🔒 PREVENT INFINITE LOOP
           ======================= */
        stage('Prevent CI Loop') {
            when {
                expression {
                    sh(
                        script: "git log -1 --pretty=%B | grep -i '\\[ci skip\\]'",
                        returnStatus: true
                    ) == 0
                }
            }
            steps {
                echo "🛑 CI-generated commit detected. Skipping pipeline."
                script {
                    currentBuild.result = 'SUCCESS'
                }
                error("Stopping pipeline to prevent infinite loop")
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    IMAGE_TAG = sh(
                        script: "cat VERSION",
                        returnStdout: true
                    ).trim()

                    sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} automated-k8s-cicd/
                    """
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                    echo "${DOCKER_PASS}" | docker login -u ${DOCKER_USER} --password-stdin
                    """
                }
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                sh """
                docker push ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Configure AWS & EKS') {
            steps {
                withCredentials([
                    [
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-creds'
                    ]
                ]) {
                    sh """
                    aws sts get-caller-identity
                    aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}
                    kubectl get nodes
                    """
                }
            }
        }

        stage('Deploy to EKS using Helm') {
            steps {
                sh """
                helm upgrade --install webapp automated-k8s-cicd/helm/myapp \
                  --set image.repository=${IMAGE_NAME} \
                  --set image.tag=${IMAGE_TAG}
                """
            }
        }

        stage('Bump Version') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-http',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_PASS'
                    )
                ]) {
                    sh """
                    git checkout main
                    git pull --rebase origin main

                    NEXT_VERSION=\$(awk -F. '{print \$1"."(\$2+1)}' VERSION)
                    echo \$NEXT_VERSION > VERSION

                    git config user.name "Jenkins CI"
                    git config user.email "jenkins@cicd.com"

                    git add VERSION
                    git commit -m "Bump version to \$NEXT_VERSION [ci skip]" || echo "No changes"

                    git push https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git HEAD:main
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD Pipeline Completed Successfully"
        }
        failure {
            echo "❌ CI/CD Pipeline Failed"
        }
    }
}
