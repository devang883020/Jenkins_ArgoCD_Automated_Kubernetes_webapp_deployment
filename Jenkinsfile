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

    stage('Push Image') {
      steps {
        sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
      }
    }

    stage('Configure AWS & Deploy to EKS') {
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

    stage('Bump Version') {
      steps {
        sh '''
        git checkout main

        NEXT_VERSION=$(awk -F. '{print $1"."($2+1)}' VERSION)
        echo "$NEXT_VERSION" > VERSION

        git config user.name "jenkins"
        git config user.email "jenkins@local"

        git add VERSION
        git commit -m "Bump version to $NEXT_VERSION"
        git push origin main
        '''
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
