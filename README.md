📋 Table of Contents

Overview
Architecture
Features
Technology Stack
Prerequisites
Project Structure
Setup Guide
How It Works
Pipeline Logic
Troubleshooting
Future Enhancements
Contributing
License


🎯 Overview
This project demonstrates a complete end-to-end CI/CD workflow using industry-standard DevOps practices and tools. It automates the entire software delivery pipeline from code commit to production deployment on Kubernetes.
What Problem Does This Solve?
Traditional deployment workflows are:

⏰ Time-consuming (manual builds, deployments)
🐛 Error-prone (human mistakes in configuration)
🔄 Inconsistent (different environments, different results)
📊 Hard to track (who deployed what, when?)

This automation provides:

✅ Speed: From code push to production in minutes
✅ Reliability: Consistent, repeatable deployments
✅ Traceability: Git history shows all changes
✅ Rollback: Easy to revert to previous versions


🏗️ Architecture
┌─────────────────────────────────────────────────────────────────┐
│                         Developer                                │
│                             │                                    │
│                             ▼                                    │
│                   ┌──────────────────┐                          │
│                   │   Push Code to   │                          │
│                   │     GitHub       │                          │
│                   └────────┬─────────┘                          │
│                            │                                    │
│                            │ Webhook Trigger                    │
│                            ▼                                    │
│                   ┌──────────────────┐                          │
│                   │                  │                          │
│                   │   Jenkins CI     │                          │
│                   │                  │                          │
│                   │  1. Detect Changes                          │
│                   │  2. Build Docker Image                      │
│                   │  3. Push to DockerHub                       │
│                   │  4. Update values.yaml                      │
│                   │                  │                          │
│                   └────────┬─────────┘                          │
│                            │                                    │
│                            │ Git Commit                         │
│                            ▼                                    │
│                   ┌──────────────────┐                          │
│                   │   GitHub Repo    │                          │
│                   │  (GitOps Source) │                          │
│                   └────────┬─────────┘                          │
│                            │                                    │
│                            │ ArgoCD Sync                        │
│                            ▼                                    │
│                   ┌──────────────────┐                          │
│                   │                  │                          │
│                   │   ArgoCD CD      │                          │
│                   │                  │                          │
│                   │  1. Detect Changes                          │
│                   │  2. Pull Helm Charts                        │
│                   │  3. Deploy to K8s                           │
│                   │                  │                          │
│                   └────────┬─────────┘                          │
│                            │                                    │
│                            ▼                                    │
│                   ┌──────────────────┐                          │
│                   │                  │                          │
│                   │   AWS EKS        │                          │
│                   │   Cluster        │                          │
│                   │                  │                          │
│                   │  ┌────────────┐  │                          │
│                   │  │   Pods     │  │                          │
│                   │  │ (Running)  │  │                          │
│                   │  └────────────┘  │                          │
│                   │                  │                          │
│                   └──────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

✨ Features
CI Pipeline (Jenkins)

🔍 Smart Change Detection: Only builds when application code changes
🐳 Automated Docker Builds: Builds and tags images with build numbers
📦 DockerHub Integration: Automatically pushes images to registry
🔄 GitOps Updates: Updates Helm values with new image tags
🛡️ Loop Prevention: Intelligent commit detection prevents infinite loops
🔐 Secure Credentials: Uses Jenkins Credential Manager for secrets

CD Pipeline (ArgoCD)

👁️ Continuous Monitoring: Watches Git repository for changes
🔄 Auto-Sync: Automatically deploys changes to Kubernetes
🎯 Declarative GitOps: Git as single source of truth
📊 Visual Dashboard: Real-time deployment status
⏮️ Easy Rollback: One-click rollback to previous versions

Application

🐍 Flask Web App: Lightweight Python web application
💊 Health Checks: Built-in health and metrics endpoints
🎨 Modern UI: Beautiful gradient interface
📊 System Info: Displays container and cluster information


🛠️ Technology Stack
ComponentTechnologyPurposeSource ControlGitHubCode repository and webhook triggerCI ServerJenkinsContinuous Integration automationCD ToolArgoCDGitOps-based Continuous DeploymentContainer RuntimeDockerApplication containerizationContainer RegistryDockerHubImage storage and distributionOrchestrationKubernetes (EKS)Container orchestration and managementPackage ManagerHelmKubernetes application packagingCloud ProviderAWSInfrastructure hosting (EKS, ALB)ApplicationFlask (Python)Web application frameworkIngressAWS ALBLoad balancing and external access

📦 Prerequisites
Before you begin, ensure you have:
Required Tools:

✅ AWS Account with EKS cluster access
✅ Jenkins server (2.400+) installed and running
✅ kubectl configured to access your cluster
✅ Helm 3.x installed
✅ ArgoCD installed on Kubernetes cluster
✅ DockerHub account
✅ GitHub account

Required Knowledge:

Basic understanding of Git and GitHub
Familiarity with Docker and containers
Basic Kubernetes concepts
Jenkins pipeline basics


📁 Project Structure
Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment/
│
├── Jenkinsfile                      # Jenkins pipeline definition
├── VERSION                          # Application version tracking
├── README.md                        # This file
│
└── automated-k8s-cicd/
    │
    ├── Dockerfile                   # Docker image definition
    ├── requirements.txt             # Python dependencies
    │
    ├── app/
    │   ├── main.py                 # Flask application
    │   └── __init__.py             # Python package init
    │
    └── helm/
        └── myapp/
            ├── Chart.yaml          # Helm chart metadata
            ├── values.yaml         # Configuration values
            └── templates/
                ├── deployment.yaml # Kubernetes deployment
                ├── service.yaml    # Kubernetes service
                └── ingress.yaml    # AWS ALB ingress

🚀 Setup Guide
Step 1: Clone the Repository
bashgit clone https://github.com/devang883020/Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment.git
cd Jenkins_ArgoCD_Automated_Kubernetes_webapp_deployment
Step 2: Configure Jenkins

Install Required Plugins:

Git Plugin
Docker Plugin
Pipeline Plugin
Credentials Binding Plugin


Add Credentials:

Go to Jenkins → Manage Jenkins → Credentials
Add DockerHub credentials (ID: dockerhub-creds)
Add GitHub credentials (ID: github-creds)


Create Pipeline Job:

New Item → Pipeline
Configure: Pipeline from SCM
SCM: Git
Repository URL: Your GitHub repo URL
Script Path: Jenkinsfile


Configure GitHub Webhook:

Go to your GitHub repository
Settings → Webhooks → Add webhook
Payload URL: http://your-jenkins-url/github-webhook/
Content type: application/json
Select: Just the push event



Step 3: Setup AWS EKS Cluster
bash# Create EKS cluster (if not exists)
eksctl create cluster \
  --name my-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2

# Configure kubectl
aws eks update-kubeconfig --name my-cluster --region us-east-1
Step 4: Install ArgoCD
bash# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Expose ArgoCD server
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
Step 5: Configure ArgoCD Application

Login to ArgoCD UI
Create New Application:

Application Name: myapp
Project: default
Sync Policy: Automatic
Repository URL: Your GitHub repo
Path: automated-k8s-cicd/helm/myapp
Cluster: https://kubernetes.default.svc
Namespace: default



Step 6: Install AWS ALB Ingress Controller
bash# Add Helm repo
helm repo add eks https://aws.github.io/eks-charts

# Install AWS Load Balancer Controller
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=my-cluster \
  --set serviceAccount.create=true \
  --set serviceAccount.name=aws-load-balancer-controller
Step 7: Test the Pipeline
bash# Make a change to main.py
echo "# Test change" >> automated-k8s-cicd/app/main.py

# Commit and push
git add .
git commit -m "test: trigger pipeline"
git push origin main

# Watch Jenkins build
# Watch ArgoCD sync
# Access your application via ALB URL

🔍 How It Works
Complete Flow:

Developer pushes code to GitHub main branch
GitHub webhook triggers Jenkins pipeline
Jenkins Pipeline Executes:

   Stage 1: Checkout Code
   ├─ Pulls latest code from GitHub
   
   Stage 2: Read Commit Message
   ├─ Extracts commit message
   ├─ Stores in env.COMMIT_MSG
   
   Stage 3: Check Code Changes
   ├─ Compares HEAD with HEAD~1
   ├─ Looks for changes in main.py
   ├─ Sets CODE_CHANGED flag
   
   Stage 4: Build Docker Image (if CODE_CHANGED)
   ├─ Builds image with BUILD_NUMBER tag
   ├─ Example: devangkubde88/webapp:69
   
   Stage 5: Login to DockerHub (if CODE_CHANGED)
   ├─ Uses Jenkins credentials
   ├─ Securely authenticates
   
   Stage 6: Push Image (if CODE_CHANGED)
   ├─ Uploads to DockerHub
   
   Stage 7: Update GitOps (if CODE_CHANGED && !ci:)
   ├─ Checkout main branch
   ├─ Pull latest changes
   ├─ Update values.yaml with new tag
   ├─ Commit with "ci:" prefix
   ├─ Push to GitHub

ArgoCD Detects Change:

Polls GitHub repository every 3 minutes (default)
Detects new commit to values.yaml
Compares desired state (Git) vs actual state (Cluster)


ArgoCD Syncs:

Pulls updated Helm chart
Renders Kubernetes manifests
Applies changes to cluster
Updates deployment with new image


Kubernetes Performs Rolling Update:

Creates new pods with new image
Waits for pods to be ready
Terminates old pods
Zero-downtime deployment! ✅




🧠 Pipeline Logic
1. Smart Change Detection
groovydef changed = sh(
    script: "git diff --name-only HEAD~1 HEAD | grep -E '^automated-k8s-cicd/app/main.py$' || true",
    returnStdout: true
).trim()
Why this matters:

Only rebuilds Docker image when app code changes
Skips builds for README, docs, or config changes
Saves CI/CD resources and time
Reduces DockerHub storage usage

Example Scenarios:
Change: README.md → No build ❌
Change: main.py → Build triggered ✅
Change: Jenkinsfile → No build ❌
Change: values.yaml → No build ❌
2. Infinite Loop Prevention
groovywhen {
    expression {
        env.CODE_CHANGED == "true" &&
        !env.COMMIT_MSG.startsWith("ci:")
    }
}
The Problem:
Without this check:
1. Developer commits → Jenkins builds → Jenkins commits "ci: update tag"
2. GitHub webhook fires → Jenkins builds → Jenkins commits "ci: update tag"
3. GitHub webhook fires → Jenkins builds → ∞ LOOP!
The Solution:
With this check:
1. Developer commits "fix: bug" → Jenkins builds → Jenkins commits "ci: update tag"
2. GitHub webhook fires → Jenkins sees "ci:" → STOPS ✅
3. Detached HEAD Resolution
bash# Problem: Jenkins checks out specific commits (detached HEAD)
# Solution: Explicitly checkout branch before pushing

git checkout main           # Get on actual branch
git pull                   # Sync with remote
sed -i "s|tag:.*|tag: 69|" # Modify file
git add values.yaml        # Stage changes
git commit -m "ci: ..."    # Commit
git push                   # Push (works because we're on main!)
4. Proper Git Operation Order
bash# ❌ WRONG ORDER (causes "unstaged changes" error):
1. Modify file
2. Try to checkout/pull
3. Git complains about unstaged changes

# ✅ CORRECT ORDER:
1. Checkout branch (clean state)
2. Pull latest (still clean)
3. Modify file (create changes)
4. Commit immediately
5. Push

