# Hackathon 2 – Phase IV
## Local Kubernetes Deployment of Todo Chatbot

### Project Overview
This project is part of **Hackathon 2 – Phase IV**, where the goal was to deploy a cloud-native Todo Chatbot application on a local Kubernetes cluster using **Minikube** and **Helm**, following an **agentic, spec-driven development workflow**.

The application consists of:

- **Frontend:** Next.js
- **Backend:** FastAPI (Todo logic + Chatbot)

Both components are containerized and deployed locally using modern DevOps tools and AI-assisted agents.

---

### Objectives
- Containerize frontend and backend applications
- Deploy the system locally on Kubernetes using Minikube
- Use Helm charts for structured deployment
- Leverage AI agents for Docker and Kubernetes operations
- Achieve a fully working, healthy local deployment

---

### Technology Stack
- **Containerization:** Docker (Docker Desktop)  
- **Docker AI:** Gordon (Docker AI Agent)  
- **Orchestration:** Kubernetes (Minikube)  
- **Package Manager:** Helm  
- **AI DevOps Tools:** kubectl-ai, Kagent  
- **Frontend:** Next.js  
- **Backend:** FastAPI (Python)  

---

### Development Approach
This phase followed an **Agentic Dev Stack workflow**:
1. Define the specification  
2. Generate a deployment plan  
3. Break the plan into tasks  
4. Implement using AI agents (no manual coding)  

Docker and Kubernetes operations were handled with AI-assisted tools to ensure consistency and correctness.

---

### What Was Implemented

#### Docker Setup
- Separate Docker images for frontend and backend  
- Optimized Dockerfiles and `.dockerignore` files  
- Backend health checks implemented  
- Images successfully built and tested locally  

#### Kubernetes Deployment
- Local Kubernetes cluster created using Minikube  
- Helm charts created for frontend and backend  
- Frontend deployed with **2 replicas**  
- Backend deployed with **1 replica**  
- Internal service communication configured  
- All pods verified as healthy  

---

### Deployment Status
- ✅ Frontend pods running and healthy  
- ✅ Backend pod running and healthy  
- ✅ Services exposed locally  
- ✅ Health checks returning successful responses  

---

### Access Information
- **Frontend:** http://localhost:3000  
- **Backend:** http://localhost:7860  
- **Backend Health Check:** http://localhost:7860/health  

---

### Key Learnings
- Hands-on experience with Docker and Kubernetes  
- Understanding Helm-based deployments  
- Practical use of AI-assisted DevOps tools  
- Experience with spec-driven, agentic workflows  
- Local cloud-native deployment without cloud costs  

---

### Conclusion
Phase IV successfully demonstrates a **fully containerized, Kubernetes-deployed application running locally**.  
This project showcases practical DevOps skills, AI-assisted automation, and modern cloud-native deployment practices.
