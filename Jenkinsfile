pipeline {
    agent any

    environment {
        IMAGE_NAME = "devangkubde88/webapp"
        GIT_BRANCH = "main"
        VALUES_FILE = "automated-k8s-cicd/helm/myapp/values.yaml"
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
                    VERSION = sh(
                        script: "cat VERSION",
                        returnStdout: true
                    ).trim()
                    echo "Current version: ${VERSION}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${VERSION} automated-k8s-cicd
                """
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
                    echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
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

        stage('Update Helm values.yaml') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: 'github-creds',
                usernameVariable: 'GIT_USER',
                passwordVariable: 'GIT_PASS'
            )
        ]) {
            sh '''
            git config user.name "jenkins"
            git config user.email "jenkins@ci.local"

            # Ensure we are on main
            git checkout main

            # Always sync with remote before changing
            git pull --rebase origin main

            # Update image tag
            sed -i "s/tag:.*/tag: ${VERSION}/" automated-k8s-cicd/helm/myapp/values.yaml

            git add automated-k8s-cicd/helm/myapp/values.yaml
            git commit -m "ci: update image tag to ${VERSION}" || echo "No changes to commit"

            git push https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git main
            '''
        }
    }
}


        stage('Bump Version') {
            steps {
                script {
                    NEXT_VERSION = sh(
                        script: "awk -F. '{print \$1\".\"(\$2+1)}' VERSION",
                        returnStdout: true
                    ).trim()

                    sh """
                    echo ${NEXT_VERSION} > VERSION
                    git add VERSION
                    git commit -m "ci: bump version to ${NEXT_VERSION}"
                    """
                }
            }
        }

        stage('Push Version Bump') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_PASS'
                    )
                ]) {
                    sh """
                    git push https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git ${GIT_BRANCH}
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ CI completed successfully. Argo CD will deploy automatically."
        }
        failure {
            echo "❌ CI failed."
        }
    }
}
