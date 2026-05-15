# 🚀 Quick Start Guide - AutoML Model Builder

Get up and running in **5 minutes**! For comprehensive docs, see [README.md](README.md).

---

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git
- 2GB RAM (minimum)

---

## Option 1: Local Development (Easiest)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/automl-model-builder.git
cd automl-model-builder
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Optional: Edit .env for custom settings
```

### Step 5: Create Directories
```bash
mkdir -p uploads/datasets outputs/models outputs/inference logs
```

### Step 6: Run Server
```bash
python run.py
```

### Step 7: Access Application
```
Open browser to: http://localhost:5000
```

**Done! 🎉**

---

## Option 2: Docker (Recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/automl-model-builder.git
cd automl-model-builder
```

### Step 2: Configure Environment
```bash
cp .env.example .env
```

### Step 3: Start Services
```bash
docker-compose up -d
```

### Step 4: Access Application
```
Open browser to: http://localhost:5000
```

**Done! 🎉**

### View Logs
```bash
docker-compose logs -f web
```

### Stop Services
```bash
docker-compose down
```

---

## Option 3: Using Make Commands (If Available)

```bash
# Setup
make install-dev
make setup-dev

# Run
make run

# Test
make test

# Docker
make docker-up
make docker-down

# View all commands
make help
```

---

## Using the Application

### 1. **Homepage** (http://localhost:5000)
- See project overview
- Read features
- View deployment options

### 2. **Create Project** (Multi-step form)
- **Step 1**: Enter project name and statement
- **Step 2**: Upload your CSV dataset
- **Step 3**: Configure model (target column, problem type)
- **Step 4**: Set training options (epochs, batch size)
- **Step 5**: Review and submit

### 3. **Training** (Automatic)
- Model trains on your data
- Wait for completion
- See progress in console logs

### 4. **Results** (http://localhost:5000/results)
- View accuracy and metrics
- Download trained model (.h5)
- Download prediction script
- Copy code examples
- Access deployment guides

---

## Example: Train Your First Model

### Sample CSV Format
```
Feature1,Feature2,Feature3,Target
1.5,2.3,3.1,0
2.1,2.9,3.5,1
1.8,2.5,3.2,0
...
```

### Steps:
1. Save CSV file locally
2. Go to http://localhost:5000
3. Fill form:
   - **Name**: "My First Model"
   - **Target Column**: "Target"
   - **Problem Type**: "Classification"
4. Upload CSV
5. Click "Submit"
6. Wait for training
7. Download and use model!

---

## Troubleshooting

### Port 5000 Already in Use
```bash
# Use different port
FLASK_ENV=development FLASK_DEBUG=1 flask run --port 5001
```

### Module Not Found Error
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Permission Denied (on Linux/Mac)
```bash
chmod +x run.py
```

### TensorFlow Installation Issues
```bash
pip install --upgrade tensorflow
# or (for Apple Silicon)
pip install tensorflow-macos
```

### Docker Issues
```bash
# Clear and restart
docker-compose down -v
docker-compose up --build
```

---

## Next Steps

### 1. Explore Documentation
- [README.md](README.md) - Full documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guides

### 2. Configure Settings
Edit `.env` file to customize:
- Max upload size
- Training parameters (epochs, batch size)
- Logging level
- Database connection

### 3. Deploy to Production
See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Render.com
- Railway.app
- HuggingFace Spaces
- Azure App Service
- AWS Lambda

### 4. Contribute
See [CONTRIBUTING.md](CONTRIBUTING.md) to:
- Report bugs
- Request features
- Submit code improvements

---

## Common Tasks

### Use Your Own Dataset
1. Prepare CSV with headers
2. Ensure target column is present
3. Upload via form

### Change Training Parameters
Edit `.env` or pass as environment variables:
```bash
EPOCHS=50 BATCH_SIZE=16 python run.py
```

### View Logs
```bash
tail -f logs/automl.log
```

### Download Trained Model
Models are saved to: `outputs/models/<project_name>.h5`

### Use Model for Predictions
```bash
# Download the predict.py from results page
python predict.py --input data.csv --model model.h5
```

---

## Architecture Overview

```
┌─────────────────┐
│   Browser UI    │  (localhost:5000)
└────────┬────────┘
         │
┌────────▼────────┐
│  Flask Server   │  (Python)
└────────┬────────┘
         │
    ┌────┴──────────┬─────────────┐
    │               │             │
┌───▼───┐     ┌────▼────┐   ┌───▼──┐
│ Files │     │Database │   │ ML   │
│Upload │     │(MySQL)  │   │Model │
└───────┘     └─────────┘   └──────┘
```

---

## Key Files

| File/Folder | Purpose |
|------------|---------|
| `run.py` | Start development server |
| `wsgi.py` | Production entry point |
| `app/` | Flask application code |
| `ml/` | Machine learning pipeline |
| `templates/` | HTML pages |
| `static/` | CSS and JavaScript |
| `uploads/` | User uploaded datasets |
| `outputs/` | Trained models and scripts |
| `.env` | Configuration settings |

---

## Performance Tips

### For Faster Training
1. Use smaller datasets (start with 1000 rows)
2. Reduce epochs (start with 10)
3. Increase batch size (try 32 or 64)

### For Better Results
1. Clean your data (remove missing values)
2. Use more training data
3. Increase epochs (100+)
4. Tune batch size experimentally

### For Smooth UI
1. Test on good internet connection
2. Use modern browser (Chrome, Firefox, Safari)
3. Disable ad blockers if having issues

---

## Get Help

### Need Help?
- **Questions**: Read [README.md](README.md)
- **Issues**: Check [GitHub Issues](https://github.com/yourusername/automl-model-builder/issues)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)

### Report Bug
1. Go to GitHub Issues
2. Click "New Issue"
3. Describe the problem
4. Include screenshots/logs

### Request Feature
1. Go to GitHub Issues
2. Click "New Issue"
3. Choose "Feature request"
4. Describe what you want

---

## Tips & Tricks

### 💡 Tip 1: Save Your Models
Models are automatically downloaded. Back them up!

### 💡 Tip 2: Use Smaller Batches for GPU
If using GPU, batch size of 128 works well.

### 💡 Tip 3: Validate Your Data
Check for missing values before uploading.

### 💡 Tip 4: Monitor Training
Watch `logs/automl.log` for training progress.

### 💡 Tip 5: Try Multiple Models
Train several models with different parameters.

---

## Quick Command Reference

```bash
# Development
python run.py                      # Start server
python run.py --port 5001         # Use different port
FLASK_DEBUG=1 python run.py        # Debug mode

# Docker
docker-compose up -d               # Start services
docker-compose logs -f web         # View logs
docker-compose down                # Stop services

# Using Makefile
make run                           # Start server
make test                          # Run tests
make lint                          # Check code
make format                        # Format code
make docker-up                     # Start Docker
make help                          # All commands

# Installation
pip install -r requirements.txt    # Install prod deps
pip install -r requirements-dev.txt # Install dev deps
```

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 2GB | 8GB |
| CPU | 2-core | 4-core |
| Disk | 500MB | 2GB |
| Python | 3.9 | 3.11+ |
| OS | Any | Linux/macOS |

---

## What's Included

✅ Professional dark UI  
✅ Multi-step form wizard  
✅ Drag-drop file upload  
✅ Automated ML pipeline  
✅ Model evaluation metrics  
✅ Code generation  
✅ Docker support  
✅ Comprehensive docs  

---

## Next Actions

**Choose One:**
1. ✅ **Start using** → Run `python run.py`
2. 📚 **Learn more** → Read [README.md](README.md)
3. 🚀 **Deploy** → See [DEPLOYMENT.md](DEPLOYMENT.md)
4. 👨‍💻 **Contribute** → See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Support

- 📖 Documentation: [README.md](README.md)
- 🏗️ Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- 🚀 Deployment: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🤝 Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- 📊 Status: [PROJECT_STATUS.md](PROJECT_STATUS.md)

---

**Happy building! 🎉**

Last Updated: May 2024
