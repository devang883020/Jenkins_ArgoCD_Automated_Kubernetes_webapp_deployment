pipeline {
    agent any

    environment {
        IMAGE_NAME   = 'devangkubde88/webapp'
        AWS_REGION   = 'ap-south-1'
        CLUSTER_NAME = 'my-eks-cluster'
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Read & Increment Version') {
            steps {
                script {
                    def version = readFile('VERSION').trim()
                    def parts = version.tokenize('.')
                    def major = parts[0]
                    def minor = parts[1].toInteger() + 1
                    env.VERSION = "${major}.${minor}"

                    writeFile file: 'VERSION', text: env.VERSION
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                  docker build \
                    -f automated-k8s-cicd/Dockerfile \
                    -t ${IMAGE_NAME}:${VERSION} \
                    automated-k8s-cicd
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
                    sh '''
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                sh '''
                  docker push ${IMAGE_NAME}:${VERSION}
                '''
            }
        }

        stage('Configure AWS & EKS') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                    sh '''
                      aws eks update-kubeconfig \
                        --region ${AWS_REGION} \
                        --name ${CLUSTER_NAME}
                    '''
                }
            }
        }

        stage('Deploy to EKS using Helm') {
            steps {
                sh '''
                  helm upgrade --install webapp automated-k8s-cicd/helm/myapp \
                    --set image.repository=${IMAGE_NAME} \
                    --set image.tag=${VERSION}
                '''
            }
        }

        stage('Commit Version Bump') {
            steps {
                sh '''
                  git config user.name "jenkins"
                  git config user.email "jenkins@local"
                  git add VERSION
                  git commit -m "Bump version to ${VERSION}" || true
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment Successful'
        }
        failure {
            echo '❌ Deployment Failed'
        }
    }
}
