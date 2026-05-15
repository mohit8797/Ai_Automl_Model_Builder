# 🚀 Deployment Guide - AutoML Model Builder

Complete step-by-step deployment instructions for multiple platforms.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker](#docker)
3. [Render](#render)
4. [Railway](#railway)
5. [HuggingFace Spaces](#huggingface-spaces)
6. [Azure App Service](#azure-app-service)
7. [AWS Lambda](#aws-lambda)
8. [Production Checklist](#production-checklist)

---

## Local Development

### Prerequisites
- Python 3.11+
- pip
- Virtual environment

### Setup Steps

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/automl-model-builder.git
cd automl-model-builder
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Create Directories**
```bash
mkdir -p uploads/datasets outputs/models outputs/inference outputs/reports logs
```

6. **Run Development Server**
```bash
python run.py
```

7. **Access Application**
```
Open http://localhost:5000 in browser
```

### Troubleshooting

**TensorFlow installation issues:**
```bash
pip install --upgrade tensorflow
```

**Permission errors on macOS/Linux:**
```bash
chmod +x run.py
```

**Port 5000 already in use:**
```bash
# Use different port
FLASK_ENV=development FLASK_DEBUG=1 flask run --port 5001
```

---

## Docker

### Prerequisites
- Docker installed and running
- Docker Compose (optional)

### Option 1: Docker Build & Run

1. **Build Image**
```bash
docker build -t automl-builder:latest .
```

2. **Run Container**
```bash
docker run -d \
  --name automl \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key-here \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/logs:/app/logs \
  automl-builder:latest
```

3. **Check Status**
```bash
docker ps
docker logs automl
```

4. **Access Application**
```
Open http://localhost:5000
```

5. **Stop Container**
```bash
docker stop automl
docker remove automl
```

### Option 2: Docker Compose

1. **Update .env**
```bash
cp .env.example .env
# Edit with your values
```

2. **Start Services**
```bash
docker-compose up -d
```

3. **View Logs**
```bash
docker-compose logs -f web
```

4. **Stop Services**
```bash
docker-compose down
```

### Docker Best Practices

- **Multi-stage builds for smaller images**
- **Don't run as root user**
- **Use environment variables for secrets**
- **Implement health checks**
- **Set resource limits**

---

## Render

[Render.com](https://render.com) - Easy platform for deploying web services

### Prerequisites
- Render account (free tier available)
- GitHub repository with code

### Deployment Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Create Render Account**
- Visit [render.com](https://render.com)
- Sign up with GitHub

3. **Create Web Service**
- Click "New +"
- Select "Web Service"
- Connect GitHub repository

4. **Configure Service**

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn wsgi:app
```

**Environment Variables:**
```
FLASK_ENV=production
SECRET_KEY=your-unique-secret-key
DEBUG=False
LOG_LEVEL=INFO
```

**Advanced Settings:**
- Plan: Free (0.5 CPU, 0.5 GB RAM)
- Region: Choose closest to users
- Auto-deploy: Enable

5. **Deploy**
- Click "Create Web Service"
- Wait for deployment (2-3 minutes)
- Get public URL

6. **Monitor**
```
https://dashboard.render.com → Select your service
```

### Tips
- **Keep secrets in environment variables**
- **Use persistent volumes for uploads/models**
- **Monitor memory usage (512MB limit on free)**
- **Set up alerts for failures**

---

## Railway

[Railway.app](https://railway.app) - Modern deployment platform

### Prerequisites
- Railway account
- GitHub repository

### Deployment Steps

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login**
```bash
railway login
```

3. **Connect Project**
```bash
cd your-project-directory
railway init
```

4. **Add Environment Variables**

Using Railway dashboard or CLI:
```bash
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
```

5. **Deploy**
```bash
railway up
```

6. **Get URL**
```bash
railway open
```

### Advanced Configuration

Create `railway.json`:
```json
{
  "build": {
    "builder": "dockerfile",
    "buildpacks": []
  },
  "deploy": {
    "startCommand": "gunicorn wsgi:app",
    "restartPolicyType": "on_failure"
  }
}
```

### Database Setup

```bash
# Add MySQL
railway add
# Select MySQL
# Configure connection string

# View credentials
railway variables
```

---

## HuggingFace Spaces

[HuggingFace Spaces](https://huggingface.co/spaces) - Share ML models and apps

### Prerequisites
- HuggingFace account
- GitHub repository (optional)

### Deployment Steps

1. **Create Space**
- Go to huggingface.co/spaces
- Click "Create new Space"
- Choose Streamlit, Gradio, or Docker

2. **Select Docker**
- Choose "Docker" as runtime
- Create Space

3. **Upload Files**
```bash
# Clone space repository
git clone https://huggingface.co/spaces/yourusername/your-space
cd your-space

# Add your files
cp -r app/* .
cp -r static/* .
cp -r templates/* .
cp requirements.txt .
cp Dockerfile .

# Commit and push
git add .
git commit -m "Deploy AutoML builder"
git push
```

4. **Configure Dockerfile**

Update Dockerfile to use Docker runtime:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "wsgi:app"]
```

5. **Access**
```
https://huggingface.co/spaces/yourusername/your-space
```

---

## Azure App Service

### Prerequisites
- Azure subscription
- Azure CLI installed
- GitHub repository

### Deployment Steps

1. **Create App Service**
```bash
az group create --name automl-group --location eastus

az appservice plan create \
  --name automl-plan \
  --resource-group automl-group \
  --sku F1 --is-linux

az webapp create \
  --resource-group automl-group \
  --plan automl-plan \
  --name automl-builder \
  --runtime "PYTHON:3.11"
```

2. **Configure Deployment**
```bash
# Connect GitHub
az webapp deployment github-actions add \
  --repo-url https://github.com/yourusername/automl-builder \
  --branch main \
  --github-token YOUR_TOKEN \
  --resource-group automl-group \
  --name automl-builder
```

3. **Set Environment Variables**
```bash
az webapp config appsettings set \
  --resource-group automl-group \
  --name automl-builder \
  --settings \
    FLASK_ENV=production \
    SECRET_KEY=your-secret-key \
    DEBUG=False
```

4. **Deploy**
```bash
git push origin main
# Azure will auto-deploy from GitHub
```

5. **Access**
```
https://automl-builder.azurewebsites.net
```

### Troubleshooting

View logs:
```bash
az webapp log tail --name automl-builder --resource-group automl-group
```

---

## AWS Lambda

### Prerequisites
- AWS account
- AWS CLI configured
- SAM CLI or Serverless Framework

### Deployment with SAM

1. **Create template.yaml**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  AutoMLFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: wsgi.app
      Runtime: python3.11
      Timeout: 300
      MemorySize: 1024
      CodeUri: .
      Environment:
        Variables:
          FLASK_ENV: production
          SECRET_KEY: !Ref SecretKey
```

2. **Deploy**
```bash
sam build
sam deploy --guided
```

### Deployment with Serverless Framework

1. **Install Serverless**
```bash
npm install -g serverless
serverless create --template aws-python
```

2. **Configure serverless.yml**
```yaml
service: automl-builder

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  environment:
    FLASK_ENV: production

functions:
  app:
    handler: wsgi.app
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

3. **Deploy**
```bash
serverless deploy
```

---

## Production Checklist

Before deploying to production:

### Security
- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set `DEBUG=False`
- [ ] Use HTTPS/SSL certificate
- [ ] Enable CORS properly
- [ ] Validate all user inputs
- [ ] Use environment variables for secrets
- [ ] Set secure headers (CSP, X-Frame-Options)
- [ ] Enable CSRF protection

### Performance
- [ ] Configure database connection pooling
- [ ] Set up caching (Redis/Memcached)
- [ ] Enable gzip compression
- [ ] Optimize static files
- [ ] Configure CDN for assets
- [ ] Set appropriate timeouts

### Reliability
- [ ] Set up error monitoring (Sentry/DataDog)
- [ ] Configure logging aggregation
- [ ] Set up backup strategy
- [ ] Configure auto-scaling
- [ ] Set up health checks
- [ ] Test disaster recovery

### Maintenance
- [ ] Document deployment process
- [ ] Set up CI/CD pipeline
- [ ] Regular security updates
- [ ] Monitor disk space
- [ ] Archive old logs
- [ ] Test backups regularly

---

## Comparison Table

| Platform | Cost | Ease | Scalability | Best For |
|----------|------|------|-------------|----------|
| Local | Free | Easy | Limited | Development |
| Docker | Free | Medium | Good | Any |
| Render | $7+/mo | Easy | Good | Simple apps |
| Railway | $5+/mo | Easy | Good | Medium apps |
| HuggingFace | Free | Easy | Limited | ML demos |
| Azure | $15+/mo | Medium | Excellent | Enterprise |
| AWS | Pay-as-you-go | Hard | Excellent | Large scale |

---

## Tips & Tricks

### Optimize Image Size
```bash
# Use alpine base image
FROM python:3.11-alpine
```

### Speed Up Builds
```bash
# Cache dependencies layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

### Reduce Package Size
```bash
# Install only production dependencies
pip install --no-dev -r requirements.txt
```

### Monitor Performance
```bash
# Monitor real-time logs
tail -f logs/automl.log

# Check resource usage
docker stats automl
```

---

## Support

- **Documentation**: See README.md
- **Issues**: Report on GitHub
- **Discussions**: Join community forums

Last Updated: May 2026
