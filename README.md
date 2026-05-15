# 🤖 AutoML Model Builder - Professional AI SaaS Platform

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask 3.0+](https://img.shields.io/badge/Flask-3.0+-red.svg)](https://flask.palletsprojects.com/)
[![TensorFlow 2.16+](https://img.shields.io/badge/TensorFlow-2.16+-orange.svg)](https://tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A professional, production-ready AutoML platform that enables anyone to build, train, and deploy machine learning models without writing code. Built with modern frontend design, comprehensive backend architecture, and deployment-ready features.

Supported operating systems:
- Windows
- macOS
- Linux

Supported Python versions:
- Recommended: Python 3.10 or 3.11
- Note: TensorFlow has known compatibility issues with Python 3.13 and 3.14; prefer 3.10/3.11 for best results.

## ✨ Key Features

### 🎯 Core Capabilities
- **No-Code Model Building**: Upload dataset → Configure → Train → Deploy
- **Automatic Model Detection**: Detects regression/classification tasks automatically
- **Data Preprocessing**: Smart handling of missing values, outliers, feature engineering
- **Hyperparameter Tuning**: Automatic optimization for better model performance
- **Cross-Validation**: K-fold cross-validation for robust evaluation
- **Multiple Model Types**: Neural Networks, Random Forest, XGBoost, SVM, KNN, Decision Trees

### 📊 Supported Models
- Classification (Binary & Multiclass)
- Regression
- Neural Networks (ANN, CNN, RNN, LSTM)
- Ensemble Methods (Random Forest, XGBoost)
- Support Vector Machines (SVM)
- K-Nearest Neighbors (KNN)
- Decision Trees

### 📁 Input/Output Formats
**Input**: CSV, Excel files (up to 25MB)  
**Output**: 
- `.h5` (TensorFlow/Keras models)
- `.pkl` (Scikit-learn/ML models)
- Preprocessing objects (scalers, encoders)
- Complete prediction scripts
- `requirements.txt` files
- Deployment templates (Flask, FastAPI, Docker)

### 🚀 Deployment Options
- Local development (Flask)
- Docker containerization
- Render
- Railway  
- HuggingFace Spaces
- Azure App Service
- AWS/GCP/Lambda

### 🎨 Professional UI/UX
- Modern dark AI theme with glassmorphism
- Responsive design (mobile, tablet, desktop)
- Multi-step form wizard with progress tracking
- Real-time notifications and toast messages
- Loading spinners and progress bars
- Production-grade typography and spacing
- Smooth animations and transitions

### 📈 Comprehensive Analytics
- Performance metrics (Accuracy, Precision, Recall, F1, RMSE, MAE, R²)
- Confusion matrices for classification
- Training history and loss curves
- Detailed evaluation reports
- CSV export capabilities

## 🛠 Tech Stack

### Backend
- **Framework**: Flask 3.1+ (Python web framework)
- **ML/AI**: TensorFlow 2.16+, Keras, Scikit-learn
- **Data**: Pandas, NumPy, Scipy
- **Database**: MySQL/PostgreSQL support
- **Logging**: Python logging with file rotation
- **Production**: Gunicorn WSGI server

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS custom properties
- **JavaScript (ES6+)** - Interactive features
- **No Dependencies** - Pure vanilla JS (no jQuery, no frameworks needed)

### DevOps & Deployment
- **Containerization**: Docker
- **Version Control**: Git/GitHub
- **Environment**: .env configuration
- **Monitoring**: Application logs and health checks

## 📦 Project Structure

```
AutoML Model Builder/
├── app/                          # Flask application
│   ├── __init__.py              # App factory with error handling
│   ├── config.py                # Configuration with env support
│   ├── logger.py                # Logging setup
│   ├── routes/
│   │   ├── web.py              # Web routes with validation
│   │   └── api.py              # REST API endpoints
│   ├── services/
│   │   └── pipeline_service.py # ML pipeline orchestration
│   └── utils/
│       ├── paths.py            # Path utilities
│       └── validation.py       # Input validation
│
├── ml/                          # ML pipeline modules
│   ├── model_builder.py         # Model architecture
│   ├── trainer.py              # Training logic
│   ├── preprocess.py           # Data preprocessing
│   └── exporter.py             # Model export utilities
│
├── templates/                   # Jinja2 templates
│   ├── index.html              # Professional homepage
│   └── result.html             # Results/output page
│
├── static/                      # Static assets
│   ├── css/
│   │   └── style.css           # Modern CSS theme
│   └── js/
│       └── main.js             # UI utilities & interactions
│
├── outputs/                     # Generated files
│   ├── models/                 # Trained .h5 and .pkl models
│   ├── inference/              # Prediction scripts
│   └── reports/                # Evaluation reports
│
├── uploads/                     # User uploaded datasets
├── logs/                        # Application logs
├── database/                    # Database schemas
├── run.py                       # Development server
├── wsgi.py                      # Production WSGI entry
├── Dockerfile                   # Container configuration
├── docker-compose.yml           # Multi-container setup
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager
- Virtual environment (recommended)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/automl-model-builder.git
cd automl-model-builder
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Create necessary directories**
```bash
mkdir -p uploads/datasets outputs/models outputs/inference outputs/reports logs
```

6. **Run development server**
```bash
python run.py
# Or with Flask CLI:
FLASK_APP=app flask run
```

7. **Access application**
```
Open http://localhost:5000 in your browser
```

## 📖 Usage Guide

### Building Your First Model

1. **Navigate to Homepage**
   - Visit http://localhost:5000
   - Review features and capabilities
   - Click "Build Your Model" button

2. **Fill Project Details (Step 1)**
   - Enter project name (e.g., "Sales Prediction")
   - Describe your problem
   - Click Next

3. **Upload Dataset (Step 2)**
   - Drag & drop CSV file or click to select
   - File must be < 25MB
   - Click Next

4. **Configure Model (Step 3)**
   - Select target column (what to predict)
   - Choose problem type (Classification/Regression)
   - Select framework (TensorFlow/Scikit-learn/XGBoost)
   - Click Next

5. **Training Options (Step 4)**
   - Enable hyperparameter tuning (optional)
   - Enable auto feature engineering
   - Enable cross-validation
   - Click Next

6. **Review & Submit (Step 5)**
   - Review all settings
   - Click "Train Model"
   - Wait for training to complete

7. **View Results**
   - See performance metrics
   - Download trained model
   - Get deployment code samples
   - Follow deployment guides

## 💻 Production Deployment

### Local Development (Flask)
```bash
export FLASK_ENV=development
export DEBUG=True
python run.py
```

### Docker Deployment

1. **Build Docker image**
```bash
docker build -t automl-builder:latest .
```

2. **Run container**
```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  automl-builder:latest
```

3. **Docker Compose**
```bash
docker-compose up -d
```

### Render Deployment

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set environment variables in Render dashboard
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `gunicorn wsgi:app`
7. Deploy!

### Railway Deployment

1. Install Railway CLI: `npm i -g @railway/cli`
2. Connect GitHub: `railway login`
3. Initialize project: `railway init`
4. Set environment variables
5. Deploy: `railway up`

### Azure App Service

1. Create Web App on Azure Portal
2. Set runtime to Python 3.11
3. Configure deployment via GitHub Actions
4. Set environment variables in Application Settings
5. Deploy: `git push azure main`

### AWS/Lambda Deployment

1. Package as Lambda function
2. Set handler to `wsgi.app`
3. Use AWS SAM or Serverless Framework
4. Deploy: `sam deploy` or `serverless deploy`

## 🔧 Configuration

### Environment Variables (.env)
```env
# Flask
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-super-secret-key

# Files
MAX_UPLOAD_SIZE=26214400  # 25MB
UPLOAD_DIR=uploads/datasets

# Models
MODEL_DIR=outputs/models
INFERENCE_DIR=outputs/inference

# Training
BATCH_SIZE=32
EPOCHS=100
TEST_SPLIT=0.2

# Features
ENABLE_FEATURE_ENGINEERING=True
ENABLE_HYPERPARAMETER_TUNING=False
ENABLE_CROSS_VALIDATION=True

# Logging
LOG_LEVEL=INFO
```

## 📊 Example: Using Trained Models

### Python Inference
```python
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import pickle

# Load model and preprocessing
model = load_model('model.h5')
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Prepare data
df = pd.read_csv('input.csv')
X = scaler.transform(df)

# Predict
predictions = model.predict(X)
print("Predictions:", predictions)
```

### Flask API Server
```python
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import pickle

app = Flask(__name__)
model = load_model('model.h5')
scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    X = scaler.transform([list(data.values())])
    pred = model.predict(X)
    return jsonify({'prediction': float(pred[0])})

if __name__ == '__main__':
    app.run(debug=False, port=5000)
```

### FastAPI Server
```python
from fastapi import FastAPI
from pydantic import BaseModel
from tensorflow.keras.models import load_model
import pickle

app = FastAPI()
model = load_model('model.h5')
scaler = pickle.load(open('scaler.pkl', 'rb'))

class InputData(BaseModel):
    features: list

@app.post("/predict")
async def predict(data: InputData):
    X = scaler.transform([data.features])
    pred = model.predict(X)
    return {"prediction": float(pred[0])}
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_routes.py::test_index
```

## 📝 API Endpoints

### Web Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage |
| POST | `/create-project` | Create and train model |
| GET | `/health` | Health check |

### REST API (Coming Soon)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/models` | Create model |
| GET | `/api/models/<id>` | Get model details |
| POST | `/api/predict` | Make predictions |
| DELETE | `/api/models/<id>` | Delete model |

## 🔒 Security Features

- ✅ CSRF protection with Flask-WTF
- ✅ Secure file uploads with validation
- ✅ SQL injection protection with SQLAlchemy
- ✅ Environment variable for sensitive data
- ✅ Input validation and sanitization
- ✅ Secure headers (CSP, X-Frame-Options, etc.)
- ✅ Rate limiting (coming soon)
- ✅ User authentication (coming soon)

## 📊 Monitoring & Logging

Application logs are stored in `logs/automl.log` with:
- Request/response tracking
- Error logging with stack traces
- Performance metrics
- Model training logs
- File rotation (10MB per file, 5 backups)

View logs:
```bash
tail -f logs/automl.log
```

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: Check [DOCS.md](DOCS.md)
- **Issues**: Report on [GitHub Issues](https://github.com/yourusername/automl-builder/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/yourusername/automl-builder/discussions)
- **Email**: support@automlbuilder.dev

## 🙏 Acknowledgments

- TensorFlow/Keras for deep learning
- Scikit-learn for ML algorithms
- Flask for web framework
- All contributors and users

## 📈 Roadmap

- [ ] User authentication & profiles
- [ ] Model versioning & comparison
- [ ] Advanced hyperparameter tuning
- [ ] AutoML feature selection
- [ ] Real-time model monitoring
- [ ] API key management
- [ ] Advanced export formats
- [ ] Model marketplace
- [ ] Collaborative projects
- [ ] Mobile app

---

**Made with ❤️ for the ML community** | Last Updated: May 2026
└── README.md
```

## Outputs
- Trained model file (`.h5`)
- Inference script (`predict.py`)
- Training report
- Requirements file
- Preprocessing artifacts

## Installation & Setup

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd automl-model-builder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py
```

### Docker Deployment
```bash
# Build image
docker build -t automl-builder .

# Run container
docker run -p 5000:5000 automl-builder
```

### Production Deployment

#### Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

#### Render/Railway
1. Connect your repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn wsgi:app`
4. Configure environment variables

#### Azure/AWS
1. Use the provided Dockerfile
2. Deploy to Azure App Service or AWS Elastic Beanstalk
3. Configure environment variables for production

## Usage
1. Access the web interface at `http://localhost:5000`
2. Enter your ML problem statement
3. Upload a CSV dataset
4. Specify the target column
5. Click "Create Project"
6. Wait for model training to complete
7. Download the generated model and inference code

## API Endpoints
- `GET /` - Web interface
- `POST /create-project` - Create new ML project
- `GET /api/health` - Health check

## Configuration
Edit `app/config.py` to modify:
- Upload limits
- Model directories
- Database settings
- Flask configuration

## Testing
Run the test suite:
```bash
python test_pipeline.py
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request