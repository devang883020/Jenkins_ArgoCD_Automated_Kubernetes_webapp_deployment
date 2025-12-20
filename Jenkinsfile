pipeline {
  agent any

  environment {
    AWS_REGION   = "ap-south-1"
    CLUSTER_NAME = "my-eks-cluster"
    IMAGE_NAME   = "devangkubde88/webapp"
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
          IMAGE_TAG = readFile('VERSION').trim()
          echo "Using image tag: ${IMAGE_TAG}"
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh """
        docker build \
          -t ${IMAGE_NAME}:${IMAGE_TAG} \
          -f automated-k8s-cicd/Dockerfile \
          automated-k8s-cicd
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
          sh '''
          echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
          '''
        }
      }
    }

    stage('Push Image to DockerHub') {
      steps {
        sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
      }
    }

    stage('Deploy to EKS using Helm') {
      steps {
        withCredentials([
          [$class: 'AmazonWebServicesCredentialsBinding',
           credentialsId: 'aws-creds']
        ]) {
          sh """
          aws sts get-caller-identity

          aws eks update-kubeconfig \
            --region ${AWS_REGION} \
            --name ${CLUSTER_NAME}

          kubectl get nodes

          helm upgrade --install webapp automated-k8s-cicd/helm/myapp \
            --set image.repository=${IMAGE_NAME} \
            --set image.tag=${IMAGE_TAG}
          """
        }
      }
    }

    stage('Bump Version & Push to GitHub') {
      steps {
        withCredentials([
          usernamePassword(
            credentialsId: 'github-creds',
            usernameVariable: 'GIT_USER',
            passwordVariable: 'GIT_PASS'
          )
        ]) {
          sh '''
          git checkout main
          git pull --rebase origin main

          NEXT_VERSION=$(awk -F. '{print $1"."($2+1)}' VERSION)
          echo "$NEXT_VERSION" > VERSION

          git config user.name "Jenkins CI"
          git config user.email "jenkins@cicd.com"

          git add VERSION
          git commit -m "Bump version to $NEXT_VERSION" || echo "No changes to commit"

          git push https://${GIT_USER}:${GIT_PASS}@github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git HEAD:main
          '''
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
