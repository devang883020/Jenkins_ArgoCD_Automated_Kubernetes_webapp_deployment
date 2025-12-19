pipeline {
    agent any

    environment {
        IMAGE_NAME = "devangkubde88/webapp"
        AWS_REGION = "ap-south-1"
        CLUSTER_NAME = "my-eks-cluster"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Read Version') {
            steps {
                script {
                    VERSION = readFile('VERSION').trim()
                    echo "Current Version: ${VERSION}"
                }
            }
        }

        

        stage('Build Docker Image') {
    steps {
        sh """
          docker build \
            -f automated-k8s-cicd/Dockerfile \
            -t ${IMAGE_NAME}:${VERSION} \
            automated-k8s-cicd
        """
    }
}

        }

        stage('Push Image to DockerHub') {
            steps {
                sh """
                  docker push ${IMAGE_NAME}:${VERSION}
                """
            }
        }

        stage('Configure AWS & EKS') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    sh """
                      aws eks update-kubeconfig \
                        --region ${AWS_REGION} \
                        --name ${CLUSTER_NAME}
                    """
                }
            }
        }

        stage('Deploy to EKS using Helm') {
            steps {
                sh """
                  helm upgrade --install webapp automated-k8s-cicd/helm/myapp \
                    --set image.repository=${IMAGE_NAME} \
                    --set image.tag=${VERSION}
                """
            }
        }
    }

    post {
        success {
            echo "✅ Deployment Successful"
        }
        failure {
            echo "❌ Deployment Failed"
        }
    }
}
