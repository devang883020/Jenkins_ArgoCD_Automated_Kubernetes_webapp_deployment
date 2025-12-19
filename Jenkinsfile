pipeline {
  agent any

  environment {
    AWS_REGION = "ap-south-1"
    CLUSTER_NAME = "my-eks-cluster"
    IMAGE_NAME = "devangkubde88/webapp"
  }

  stages {

    stage('Checkout Code') {
      steps {
        checkout scm
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
          docker build \
            -t ${IMAGE_NAME}:${IMAGE_TAG} \
            -f automated-k8s-cicd/Dockerfile \
            automated-k8s-cicd
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
          echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
          """
        }
      }
    }

    stage('Push Image') {
      steps {
        sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
      }
    }

    stage('Configure AWS & EKS') {
      steps {
        withCredentials([
          string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
          string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
        ]) {
          sh """
          aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
          aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
          aws configure set region ${AWS_REGION}

          aws eks update-kubeconfig \
            --region ${AWS_REGION} \
            --name ${CLUSTER_NAME}

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
        sh """
        NEXT_VERSION=\$(awk -F. '{print \$1"."(\$2+1)}' VERSION)
        echo \$NEXT_VERSION > VERSION
        git config user.name "jenkins"
        git config user.email "jenkins@local"
        git add VERSION
        git commit -m "Bump version to \$NEXT_VERSION"
        git push origin main
        """
      }
    }
  }

  post {
    success {
      echo "✅ Deployment successful"
    }
    failure {
      echo "❌ Deployment failed"
    }
  }
}
