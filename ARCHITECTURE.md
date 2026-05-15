# 🏗️ System Architecture - AutoML Model Builder

Comprehensive documentation of the AutoML Model Builder's architecture, design patterns, and component interactions.

## Table of Contents

1. [High-Level Overview](#high-level-overview)
2. [Frontend Architecture](#frontend-architecture)
3. [Backend Architecture](#backend-architecture)
4. [ML Pipeline Architecture](#ml-pipeline-architecture)
5. [Data Flow](#data-flow)
6. [Design Patterns](#design-patterns)
7. [File Structure](#file-structure)

---

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  (HTML5, CSS3, Vanilla JavaScript - No Dependencies)        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                     Flask Web Server                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes & Controllers (web.py, api.py)              │  │
│  │  - Request handling                                  │  │
│  │  - Input validation                                 │  │
│  │  - Response formatting                              │  │
│  └──────────────────────────────────────────────────────┘  │
└────┬─────────────────────────────────────────────────┬─────┘
     │                                                 │
     ▼                                                 ▼
┌──────────────────────┐                  ┌──────────────────────┐
│  ML Pipeline Service │                  │  Database Layer      │
│                      │                  │  (MySQL/PostgreSQL)  │
│ - Orchestration      │                  │                      │
│ - Data Processing    │                  │ - Model Metadata     │
│ - Model Training     │                  │ - User Projects      │
│ - Evaluation         │                  │ - Training History   │
│ - Export             │                  └──────────────────────┘
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│           ML/AI Pipeline (ml/ directory)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Model Builder   │ Trainer      │ Preprocessor       │  │
│  │ - Architecture  │ - Epochs     │ - Data Cleaning    │  │
│  │ - Layers        │ - Validation │ - Encoding         │  │
│  │ - Compilation   │ - Metrics    │ - Scaling          │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
           ▲
           │
           │ (TensorFlow/Keras + Scikit-learn)
           │
┌──────────────────────────────────────────────────────────────┐
│              File System Storage                             │
│  uploads/      - User uploaded datasets                      │
│  outputs/      - Trained models (.h5, .pkl)                │
│  logs/         - Application logs                            │
│  static/       - CSS, JS files                               │
│  templates/    - HTML templates                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Frontend Architecture

### Technology Stack
- **HTML5**: Semantic markup, modern web standards
- **CSS3**: Custom properties (variables), Grid, Flexbox, Animations
- **JavaScript (ES6+)**: Vanilla JS, no frameworks or dependencies

### Key Components

#### 1. Homepage (index.html)
```
Hero Section
    ├── Tagline & CTA
    └── Action Buttons

Navigation Bar
    ├── Logo
    ├── Menu Items
    └── CTA Button

Content Sections
    ├── Platform Overview
    ├── Features
    ├── Supported Models
    ├── Workflow
    ├── Use Cases
    └── Deployment Options

Multi-Step Form
    ├── Step 1: Project Info
    ├── Step 2: Dataset Upload
    ├── Step 3: Model Config
    ├── Step 4: Training Options
    └── Step 5: Review & Submit

Footer
```

#### 2. Results Page (result.html)
```
Success Banner
    ├── Status Indicator
    └── Next Steps

Project Summary
    ├── Project Details
    ├── Model Details
    └── Performance Metrics

Download Section
    ├── Model Files
    ├── Preprocessing Objects
    ├── Scripts
    └── Complete Package

Code Examples
    ├── Python Inference
    ├── Flask API
    ├── FastAPI
    └── Batch Prediction

Deployment Guides
    ├── Local Development
    ├── Docker
    ├── Render
    ├── Railway
    ├── HuggingFace
    └── Cloud Platforms
```

#### 3. JavaScript Utilities (main.js)

**Toast Notification System**
```javascript
Toast.success('Model trained successfully!')
Toast.error('Error during training')
Toast.warning('Warning message')
Toast.info('Information message')
```

**Loading Manager**
```javascript
LoadingManager.setLoading('.submit-btn', true)
LoadingManager.showFullPageLoader('Training...')
LoadingManager.hideFullPageLoader()
```

**Form Validator**
```javascript
FormValidator.validateRequired(input)
FormValidator.validateEmail(email)
FormValidator.validateFileSize(file, 25)
FormValidator.showError(input, 'Error message')
```

**File Upload Handler**
```javascript
FileUploadHandler.initDragDrop('.drop-zone', 'input[type="file"]')
```

**Multi-Step Form**
```javascript
const form = new MultiStepForm('#model-form')
form.nextStep()
form.previousStep()
form.getCurrentStep()
```

### Modern CSS Theme
- **Dark AI Theme**: Professional, eye-friendly dark background
- **Glassmorphism**: Modern frosted glass effect
- **Gradients**: Smooth gradient backgrounds
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG compliant
- **Performance**: Optimized animations, smooth transitions

---

## Backend Architecture

### Application Factory Pattern

```python
# app/__init__.py
def create_app() -> Flask:
    """Factory pattern for creating Flask instances"""
    app = Flask(__name__)
    app.config.from_object(get_config())
    
    # Initialize logging
    LoggerSetup.setup()
    
    # Register blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app
```

### Configuration Management

```python
# app/config.py - Hierarchical Configuration
Config           # Base configuration
├── DevelopmentConfig
├── ProductionConfig
└── TestingConfig

# Supports environment variables for:
- Flask settings
- File paths
- Training parameters
- Logging configuration
- Security settings
```

### Blueprints & Routes

```python
# Blueprint 1: Web Routes (web_bp)
GET  /                      - Homepage
POST /create-project        - Model training
GET  /health               - Health check

# Blueprint 2: API Routes (api_bp)
POST /api/models           - Create model
GET  /api/models/<id>      - Get model details
POST /api/predict          - Make predictions
```

### Middleware & Error Handling

```
Flask Request
    ↓
Logging Middleware (app.logger)
    ↓
Error Handling (error handlers)
    ↓
Routes
    ├── Validation (app/utils/validation.py)
    ├── Processing (app/services/)
    └── Response Formatting
    ↓
Flask Response
```

### Service Layer

```python
# app/services/pipeline_service.py
def run_pipeline(dataset_path, project_name, target_column, config):
    """Orchestrates entire ML training pipeline"""
    
    1. analyze_dataset()         # Analyze input data
    2. preprocess_data()         # Clean & prepare data
    3. build_model()            # Create model architecture
    4. train_model()            # Train neural network
    5. evaluate_model()         # Calculate metrics
    6. save_model()             # Save .h5 file
    7. save_preprocessing_objects()  # Save scalers/encoders
    8. generate_inference_script()   # Create prediction code
    9. generate_requirements_file()  # Create requirements.txt
    
    return {
        'project_name': str,
        'task_type': str,
        'model_path': Path,
        'requirements_path': Path,
        'evaluation': dict,
        'artifact_paths': dict
    }
```

### Logging System

```python
# app/logger.py - Centralized Logging

get_logger('module_name')

Logger Configuration:
├── File Handler
│   ├── Rotating file (10MB max)
│   ├── 5 backup files
│   └── logs/automl.log
├── Console Handler (development only)
└── Formatter: %(asctime)s - %(name)s - %(levelname)s - %(message)s

Exception Hierarchy:
├── APIException
│   ├── ValidationException
│   ├── ProcessingException
│   └── FileException
```

---

## ML Pipeline Architecture

### Data Flow

```
User Dataset (CSV)
    ↓
analyze_dataset()          # Detect data types & task
    ├── Read CSV
    ├── Infer column types
    ├── Detect problem type (classification/regression)
    └── Generate metadata
    ↓
preprocess_data()          # Clean & prepare data
    ├── Handle missing values
    ├── Encode categorical variables
    ├── Scale numerical features
    ├── Split train/test
    └── Save preprocessors
    ↓
build_model()              # Create neural network
    ├── Determine input shape
    ├── Select architecture (ANN/CNN/RNN/LSTM)
    ├── Add layers
    ├── Compile model
    └── Return model object
    ↓
train_model()              # Train on data
    ├── Fit model
    ├── Track history
    ├── Validate on test set
    └── Return training history
    ↓
evaluate_model()           # Calculate metrics
    ├── Accuracy/Precision/Recall
    ├── F1-Score
    ├── RMSE/MAE (regression)
    ├── Confusion matrix
    └── Return evaluation dict
    ↓
save_model()               # Save trained model
    ├── Save .h5 file
    ├── Save metadata
    └── Return path
    ↓
save_preprocessing_objects()  # Save scalers/encoders
    ├── Save scaler.pkl
    ├── Save label_encoders.pkl
    ├── Save target_encoder.pkl
    └── Return artifact paths
    ↓
generate_inference_script()  # Create prediction code
    ├── Generate predict.py
    ├── Include model loading
    ├── Include preprocessing
    └── Return script path
    ↓
generate_requirements_file()  # Create dependencies
    ├── Detect required packages
    ├── Pin versions
    └── Save requirements.txt
    ↓
Final Result
├── Trained Model (.h5)
├── Preprocessors (.pkl)
├── Prediction Script (.py)
├── Requirements (.txt)
├── Evaluation Metrics (dict)
└── Paths to all files
```

### Model Architecture Selection

```python
def build_model(input_shape, task_type, num_classes=None):
    """Select and build appropriate model"""
    
    if task_type == "regression":
        # Linear output layer
        model = Sequential([
            Dense(64, activation='relu', input_shape=(input_shape,)),
            Dense(32, activation='relu'),
            Dense(1, activation='linear')
        ])
        
    elif task_type == "classification":
        if num_classes == 2:
            # Binary classification
            output_layer = Dense(1, activation='sigmoid')
            loss = 'binary_crossentropy'
        else:
            # Multiclass
            output_layer = Dense(num_classes, activation='softmax')
            loss = 'sparse_categorical_crossentropy'
    
    model.compile(optimizer='adam', loss=loss, metrics=['accuracy'])
    return model
```

### Feature Engineering

```python
# Auto-detect and engineer features
- Polynomial features
- Interaction terms
- Feature scaling
- One-hot encoding
- Label encoding
- Missing value imputation
- Outlier detection
```

---

## Data Flow

### Request Flow

```
1. User fills multi-step form in browser
   ↓
2. Browser validates locally (JavaScript)
   ↓
3. User submits form to /create-project
   ↓
4. Flask receives POST request
   ↓
5. Validate file upload:
   - File exists
   - File format allowed
   - File size < 25MB
   ↓
6. Validate form fields:
   - Project name (1-100 chars)
   - Problem statement (1-1000 chars)
   - Target column name
   ↓
7. Save uploaded file to uploads/datasets/
   ↓
8. Validate CSV content:
   - Not empty
   - Has columns
   - Can parse
   ↓
9. Call run_pipeline() service
   ↓
10. ML Pipeline executes (analyze → preprocess → build → train → evaluate)
    ↓
11. Save all artifacts (model.h5, scalers, scripts)
    ↓
12. Return result dictionary to template
    ↓
13. Render result.html with:
    - Project summary
    - Performance metrics
    - Download buttons
    - Code examples
    - Deployment guides
```

### Error Handling Flow

```
Try to create project
    ├─ Validation Error
    │  ├─ Log warning
    │  ├─ Create APIException
    │  └─ Return error response to user
    │
    ├─ File Upload Error
    │  ├─ Log warning
    │  ├─ Delete partial file
    │  └─ Return error response
    │
    ├─ Processing Error
    │  ├─ Log error with traceback
    │  ├─ Cleanup temporary files
    │  └─ Return generic error message
    │
    └─ Unexpected Error
       ├─ Log error with full traceback
       ├─ Send alert (in production)
       └─ Return 500 error to user
```

---

## Design Patterns

### 1. Application Factory Pattern
```python
# Enables testing, multiple configurations, flexibility
app = create_app()  # Creates configured Flask instance
```

### 2. Service Layer Pattern
```python
# Separates business logic from routes
# routes/web.py → services/pipeline_service.py
```

### 3. Repository Pattern (Future)
```python
# Will abstract database access
# routes → services → repositories → database
```

### 4. Singleton Pattern
```python
# Logging setup runs once
LoggerSetup.setup()  # Only initializes once
get_logger('name')   # Reuses same configuration
```

### 5. Decorator Pattern
```python
# Custom decorators for middleware
@app.route('/create-project')
@validate_request
def create_project():
    pass
```

### 6. Strategy Pattern
```python
# Different strategies for different models
if task_type == "classification":
    strategy = ClassificationStrategy()
elif task_type == "regression":
    strategy = RegressionStrategy()
```

### 7. Template Method Pattern
```python
# ML pipeline defines steps
def run_pipeline():
    1. Analyze
    2. Preprocess
    3. Build
    4. Train
    5. Evaluate
    # Each step is method that can be overridden
```

---

## File Structure

```
automl-model-builder/
│
├── app/                           # Flask Application Core
│   ├── __init__.py               # App factory, error handlers
│   ├── config.py                 # Environment-aware config
│   ├── logger.py                 # Logging setup & exceptions
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── web.py               # Web routes (HTML pages)
│   │   └── api.py               # REST API endpoints
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── pipeline_service.py  # ML pipeline orchestration
│   │
│   └── utils/
│       ├── __init__.py
│       ├── paths.py             # Path utilities
│       ├── validation.py        # Input validation
│       └── helpers.py           # General helpers
│
├── ml/                            # Machine Learning Pipeline
│   ├── __init__.py
│   ├── model_builder.py          # Neural network architecture
│   ├── trainer.py                # Training logic
│   ├── preprocess.py             # Data preprocessing
│   └── exporter.py               # Model export utilities
│
├── database/                      # Database
│   ├── db.py                     # Database connection
│   └── models.sql                # Schema definitions
│
├── templates/                     # Jinja2 HTML Templates
│   ├── index.html                # Homepage & form
│   └── result.html               # Results page
│
├── static/                        # Static Assets
│   ├── css/
│   │   └── style.css             # Modern dark AI theme
│   └── js/
│       └── main.js               # Vanilla JS utilities
│
├── outputs/                       # Generated Artifacts
│   ├── models/                   # .h5 and .pkl files
│   ├── inference/                # Prediction scripts
│   └── reports/                  # Evaluation reports
│
├── uploads/                       # User Uploads
│   └── datasets/                 # CSV files
│
├── logs/                          # Application Logs
│   └── automl.log                # Main log file
│
├── utils/                         # Legacy Utilities
│   └── helpers.py
│
├── run.py                         # Development server
├── wsgi.py                        # Production WSGI entry
├── Dockerfile                     # Docker image
├── docker-compose.yml             # Multi-container setup
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
├── README.md                      # Project documentation
├── DEPLOYMENT.md                  # Deployment guides
├── ARCHITECTURE.md                # This file
└── LICENSE                        # MIT License
```

---

## Key Design Decisions

### 1. No Frontend Framework
- **Why**: Faster loading, smaller bundle size, no build step
- **Trade-off**: More vanilla JS code

### 2. Dark AI Theme
- **Why**: Professional, eye-friendly for long sessions
- **Benefits**: Reduces eye strain, modern appearance

### 3. Modular Backend
- **Why**: Scalability, testability, maintainability
- **Structure**: Config → Routes → Services → Business Logic

### 4. ML Pipeline as Service
- **Why**: Reusable, testable, decoupled
- **Flexibility**: Can be called from multiple routes

### 5. Extensive Error Handling
- **Why**: User-friendly error messages
- **Logging**: Full traceability for debugging

### 6. Environment-Based Config
- **Why**: Same code, different environments
- **Security**: Secrets not in codebase

---

## Scalability Considerations

### For Larger Datasets
- [ ] Implement chunked processing
- [ ] Add database caching
- [ ] Use async task queues (Celery)
- [ ] Implement pagination

### For More Users
- [ ] Add load balancing
- [ ] Implement rate limiting
- [ ] Use Redis for caching
- [ ] Database optimization (indexing)

### For Complex Models
- [ ] GPU support (CUDA)
- [ ] Distributed training
- [ ] Model versioning
- [ ] A/B testing framework

---

## Security Considerations

✅ **Implemented**
- Input validation
- File type checking
- File size limits
- CSRF protection ready
- Secure headers ready
- Error handling (no stack traces to users)

📋 **To Implement**
- User authentication
- API key management
- Rate limiting
- SQL injection protection (SQLAlchemy)
- XSS protection (Jinja2)
- CORS configuration

---

## Performance Optimization

✅ **Implemented**
- CSS custom properties (faster rendering)
- Vanilla JS (minimal overhead)
- Efficient queries
- File upload validation before processing
- Proper error handling (fail fast)

📋 **To Implement**
- Database connection pooling
- Redis caching
- CDN for static files
- Image optimization
- API response caching
- Database indexing

---

## Monitoring & Observability

**Logging**
- Application logs: logs/automl.log
- Request logging: route entry/exit
- Error logging: full traceback
- Model training logs: per-project

**Health Checks**
- GET /health endpoint
- Docker health checks
- Database connectivity
- File system access

**Metrics (Future)**
- Training time
- Model accuracy
- Error rates
- User statistics

---

Last Updated: May 2026
