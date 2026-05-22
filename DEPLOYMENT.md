# Deployment Guide — IT Inventory Tracker

This document explains the production deployment setup for the IT Inventory Tracker project.

## Production Architecture

```txt
Vercel Frontend
    ↓
AWS ECS Fargate Backend
    ↓
PostgreSQL Database
```

The backend is containerized with Docker, stored in Amazon ECR, and deployed to AWS ECS Fargate. The frontend is deployed on Vercel and calls the backend through an HTTPS API.

## Live Services

### Frontend

```txt
https://it-inventory-tracker.vercel.app
```

### Backend API

```txt
http://52.14.187.149:8000
```

The browser should call `/api` on the Vercel site (HTTPS proxy), not the raw task IP.

### Important API Endpoints

```txt
GET /health
GET /api/dashboard
GET /api/items
GET /api/locations
POST /api/items
PUT /api/items/{id}
DELETE /api/items/{id}
```

Example:

```txt
https://it-inventory-tracker.vercel.app/api/items
```

## Tech Stack

### Frontend

```txt
React
TypeScript
Vite
Tailwind CSS
Vercel
```

### Backend

```txt
FastAPI
Python
SQLAlchemy
Docker
AWS ECS Fargate
Amazon ECR
```

### Database

```txt
PostgreSQL
```

### CI/CD

```txt
GitHub Actions
AWS IAM OIDC Role
Amazon ECR
AWS ECS Fargate
```

## Deployment Flow

```txt
Push to main
    ↓
GitHub Actions starts
    ↓
Docker image is built from backend/Dockerfile
    ↓
Image is pushed to Amazon ECR
    ↓
ECS task definition is updated with the new image
    ↓
ECS Fargate service is redeployed
    ↓
Health check confirms backend is running
```

## GitHub Actions CI/CD

The workflow file is located at:

```txt
.github/workflows/deploy-backend.yaml
```

It runs when changes are pushed to:

```txt
backend/**
.github/workflows/deploy-backend.yaml
```

The workflow performs these steps:

```txt
1. Checks out the repository code
2. Authenticates to AWS using GitHub OIDC
3. Logs into Amazon ECR
4. Builds the backend Docker image
5. Pushes the Docker image to ECR using the Git commit SHA as the image tag
6. Downloads the current ECS task definition
7. Updates the task definition with the new image
8. Deploys the updated task definition to ECS
9. Waits for the ECS service to become stable
```

This avoids manually building, tagging, pushing, and updating ECS through the AWS Console.

## AWS Resources

### Region

```txt
us-east-2
```

### ECR Repository

```txt
inventory-backend
```

### ECS Cluster

```txt
default
```

### ECS Service

```txt
inventory-backend-service
```

### ECS Task Definition Family

```txt
default-inventory-backend-service
```

### ECS Container Name

```txt
Main
```

### Container Port

```txt
8000
```

### Health Check Path

```txt
/health
```

## Environment Variables

### Vercel Frontend Environment Variable

```txt
# Unset VITE_API_URL, or set VITE_API_URL=/api (see vercel.json ECS proxy)
```

Important: the value includes `/api` because the frontend code calls paths like:

```txt
${VITE_API_URL}/items
${VITE_API_URL}/dashboard
```

### ECS Backend Environment Variables

```txt
POSTGRES_URL=<PostgreSQL connection string>
CORS_ORIGINS=https://it-inventory-tracker.vercel.app,http://localhost:5173,http://localhost:3000
```

Do not commit `POSTGRES_URL` to GitHub. It contains database credentials.

## CORS

The backend allows the Vercel frontend to call the API.

The backend supports:

```txt
https://it-inventory-tracker.vercel.app
Vercel preview URLs ending in .vercel.app
Local development URLs
```

This prevents browser CORS errors when the Vercel frontend calls the ECS backend.

## Health Check

The backend has a dedicated health endpoint:

```txt
GET /health
```

Expected response:

```json
{
  "status": "healthy"
}
```

ECS uses this endpoint to confirm the backend container is healthy after deployment.

## PostgreSQL Database

The backend uses PostgreSQL when `POSTGRES_URL` is provided.

If `POSTGRES_URL` is missing, the backend may fall back to SQLite locally. In production, `POSTGRES_URL` must be set in ECS.

To check whether data exists, open:

```txt
https://it-inventory-tracker.vercel.app/api/items
```

If it returns an empty list:

```json
[]
```

then the backend is working, but the database is empty or not seeded.

## Seeding Demo Data

The project includes a seed script for demo inventory data.

Run from the `backend` folder:

```powershell
$env:POSTGRES_URL="your_postgres_connection_string"
python -m app.seed_data
```

Do not paste the real connection string into GitHub.

After seeding, test:

```txt
https://it-inventory-tracker.vercel.app/api/items
```

You should see inventory items returned as JSON.

## Local Development

### Backend

```powershell
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on:

```txt
http://localhost:8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on:

```txt
http://localhost:5173
```

For local frontend development, use:

```txt
VITE_API_URL=http://localhost:8000/api
```

## Manual Backend Docker Deploy

Normally, GitHub Actions handles deployment automatically.

If manual deployment is needed:

```powershell
cd backend
docker build -t inventory-backend:manual .
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 070203626345.dkr.ecr.us-east-2.amazonaws.com
docker tag inventory-backend:manual 070203626345.dkr.ecr.us-east-2.amazonaws.com/inventory-backend:manual
docker push 070203626345.dkr.ecr.us-east-2.amazonaws.com/inventory-backend:manual
```

Then update the ECS service image URI to:

```txt
070203626345.dkr.ecr.us-east-2.amazonaws.com/inventory-backend:manual
```

## Smoke Test Script

The project includes a smoke test script:

```txt
scripts/smoke-test.ps1
```

Run it from the project root (defaults to the production ECS URL):

```powershell
.\scripts\smoke-test.ps1
```

Against local Docker:

```powershell
.\scripts\smoke-test.ps1 -ApiBase "http://localhost:8000"
```

The script checks:

```txt
/health
/api/items
```

This confirms the backend is reachable and the API is responding.

## GitHub Actions Secret

The GitHub Actions workflow uses this repository secret:

```txt
AWS_ROLE_TO_ASSUME
```

Example value:

```txt
arn:aws:iam::070203626345:role/GitHubActionsECSDeployRole
```

This role is assumed through GitHub OIDC. No long-lived AWS access keys are stored in GitHub.

## Common Troubleshooting

### CORS error in browser

Check that ECS has:

```txt
CORS_ORIGINS=https://it-inventory-tracker.vercel.app,http://localhost:5173,http://localhost:3000
```

Also confirm the backend code allows Vercel preview URLs.

### Frontend shows "Failed to fetch" on Vercel

Common causes after removing the load balancer:

1. **Mixed content** — The Vercel site is HTTPS. Browsers block `http://task-ip:8000` from the page. Fix: leave `VITE_API_URL` unset (or set `/api`) and proxy through Vercel (`vercel.json` rewrites to ECS).

2. **Missing `/api` in `VITE_API_URL`** — FastAPI routes live under `/api/...`. If you set a direct API host, use `http://IP:8000/api`, not `http://IP:8000`.

3. **Dead ECS Service Connect DNS** — URLs like `https://….ecs.us-east-2.on.aws` stop resolving when that endpoint is removed. Use the task public IP or a new HTTPS hostname.

Check Vercel → Project → Settings → Environment Variables:

```txt
# Recommended (proxy via vercel.json):
(delete VITE_API_URL or set to /api)

# Only if you have a public HTTPS API:
VITE_API_URL=https://your-api-host.example.com/api
```

After changing env vars, **redeploy** the frontend (Vite bakes env at build time).

Make sure the variable name is exactly `VITE_API_URL`, not `Vite_API_URL`.

### ECS deployment rolls back

Check:

```txt
ECS Service → Events
ECS Service → Tasks → Stopped tasks
CloudWatch logs
```

Common causes:

```txt
Bad image
Wrong port
Bad health check path
Missing environment variable
Database connection issue
```

### API returns empty data

Open:

```txt
/api/items
```

If it returns:

```json
[]
```

then the API works, but PostgreSQL probably has no seeded data.

Run:

```powershell
python -m app.seed_data
```

with `POSTGRES_URL` set.

### GitHub Actions cannot assume role

Check the GitHub secret:

```txt
AWS_ROLE_TO_ASSUME
```

It must be the IAM role ARN, not the ECR repository ARN.

Correct format:

```txt
arn:aws:iam::070203626345:role/GitHubActionsECSDeployRole
```

## Interview Summary

This project demonstrates:

```txt
Full-stack deployment
Docker containerization
AWS ECS Fargate
Amazon ECR
PostgreSQL integration
Vercel frontend deployment
CORS configuration
Health checks
GitHub Actions CI/CD
AWS IAM OIDC authentication
Smoke testing with PowerShell
```

A concise interview explanation:

```txt
I deployed the frontend on Vercel and containerized the FastAPI backend with Docker. The backend image is stored in Amazon ECR and runs on ECS Fargate. The backend connects to PostgreSQL through an ECS environment variable. I also set up GitHub Actions with AWS OIDC so every backend push to main automatically builds a new Docker image, pushes it to ECR, updates the ECS task definition, and redeploys the ECS service. I added a /health endpoint and a smoke-test script to verify the deployment.
```

## Kubernetes Note

This project is deployed with ECS Fargate for simplicity and cost control.

A Kubernetes version would use:

```txt
Deployment → to run backend pods
Service → to expose backend pods internally
Ingress or LoadBalancer → to expose the API publicly
Secrets → for POSTGRES_URL
ConfigMap → for non-sensitive configuration
```

ECS was chosen for the live deployment because it provides managed container hosting without the cost and operational overhead of running EKS.
