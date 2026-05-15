"""
Web routes for AutoML Model Builder
Handles HTML page rendering and form submissions
"""

from flask import Blueprint, current_app, render_template, request, redirect, url_for, send_from_directory, send_file, abort, after_this_request
from werkzeug.utils import secure_filename
from pathlib import Path
import shutil
import tempfile

from app.services.pipeline_service import run_pipeline
from app.utils.paths import slugify
from app.utils.validation import (
    allowed_file,
    validate_file_size,
    validate_form_input,
    validate_csv_file,
    ValidationException,
)
from app.config import Config
from app.logger import get_logger, FileException

logger = get_logger('web_routes')

web_bp = Blueprint("web", __name__)


@web_bp.route("/", methods=["GET"])
def index():
    """Homepage - display form and information"""
    logger.info("Rendering homepage")
    return render_template("index.html")


@web_bp.route("/create-project", methods=["POST"])
def create_project():
    """
    Handle project creation with uploaded dataset
    Validates inputs and starts model training pipeline
    """
    logger.info("Received project creation request")
    
    try:
        # ===== INPUT VALIDATION =====
        
        # Check if file is present
        if "dataset" not in request.files:
            logger.warning("No dataset file in request")
            raise FileException("Dataset file is required", payload={'field': 'dataset'})
        
        dataset_file = request.files.get("dataset")
        
        # Check if file was selected
        if dataset_file.filename == "":
            logger.warning("Empty filename provided")
            raise FileException("No file selected", payload={'field': 'dataset'})
        
        # Validate file extension
        if not allowed_file(dataset_file.filename):
            logger.warning(f"Invalid file extension: {dataset_file.filename}")
            raise FileException(
                "Only CSV and Excel files are allowed",
                payload={'field': 'dataset', 'allowed': ['csv', 'xlsx', 'xls']}
            )
        
        # Validate file size
        dataset_file.seek(0, 2)  # Seek to end
        file_size = dataset_file.tell()
        dataset_file.seek(0)  # Seek back to start
        
        if not validate_file_size(file_size):
            logger.warning(f"File too large: {file_size} bytes")
            raise FileException(
                "File size exceeds 25MB limit",
                payload={'field': 'dataset', 'max_size': '25MB', 'actual_size': f"{file_size / 1024 / 1024:.2f}MB"}
            )
        
        # Validate form fields
        form_data = {
            'project_name': request.form.get('project_name'),
            'problem_statement': request.form.get('problem_statement'),
            'target_column': request.form.get('target_column'),
            'problem_type': request.form.get('problem_type', 'classification'),
        }
        
        validated_data = validate_form_input(form_data)
        
        logger.info(f"Form validation successful for project: {validated_data['project_name']}")
        
        # ===== FILE UPLOAD =====
        
        upload_dir = Path(current_app.config["UPLOAD_DIR"])
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        safe_prefix = slugify(validated_data['project_name'])
        safe_filename = secure_filename(dataset_file.filename)
        dataset_path = upload_dir / f"{safe_prefix}_{safe_filename}"
        
        # Save uploaded file
        dataset_file.save(str(dataset_path))
        logger.info(f"Dataset saved to: {dataset_path}")
        
        # ===== VALIDATE DATASET CONTENT =====
        
        try:
            csv_metadata = validate_csv_file(str(dataset_path))
            logger.info(f"Dataset metadata: {csv_metadata}")
        except ValidationException as e:
            logger.error(f"Dataset validation failed: {str(e)}")
            # Clean up uploaded file
            if dataset_path.exists():
                dataset_path.unlink()
            raise
        
        # ===== RUN TRAINING PIPELINE =====
        
        logger.info(f"Starting training pipeline for project: {validated_data['project_name']}")
        
        result = run_pipeline(
            dataset_path=str(dataset_path),
            project_name=validated_data['project_name'],
            target_column=validated_data['target_column'],
            config=Config,
        )
        
        logger.info(f"Training pipeline completed successfully")
        
        return render_template("result.html", result=result)

    except ValidationException as e:
        logger.warning(f"Validation error: {e.message}")
        return render_template("index.html", error=e.message), 400

    except FileException as e:
        logger.warning(f"File error: {e.message}")
        return render_template("index.html", error=e.message), 400

    except Exception as e:
        logger.error(f"Unexpected error during project creation: {str(e)}", exc_info=True)
        error_msg = "An error occurred while creating your project. Please try again."
        return render_template("index.html", error=error_msg), 500


@web_bp.route('/download/model/<project_slug>', methods=['GET'])
def download_model(project_slug):
    model_dir = Path(current_app.config['MODEL_DIR'])
    model_filename = secure_filename(f"{project_slug}.keras")
    model_path = model_dir / model_filename

    if not model_path.exists():
        logger.warning(f"Model not found for download: {model_path}")
        abort(404)

    return send_from_directory(directory=str(model_dir), path=model_filename, as_attachment=True)


@web_bp.route('/download/artifact/<project_slug>/<artifact_name>', methods=['GET'])
def download_artifact(project_slug, artifact_name):
    inference_dir = Path(current_app.config['INFERENCE_DIR']) / project_slug
    safe_name = secure_filename(artifact_name)
    allowed_files = {
        'scaler.pkl',
        'label_encoders.pkl',
        'target_encoder.pkl',
        'requirements.txt',
        'predict.py',
        'README.md',
        'sample_input.py',
    }

    if safe_name not in allowed_files:
        logger.warning(f"Attempt to download unsupported artifact: {safe_name}")
        abort(404)

    artifact_path = inference_dir / safe_name
    if not artifact_path.exists():
        logger.warning(f"Artifact not found for download: {artifact_path}")
        abort(404)

    return send_from_directory(directory=str(inference_dir), path=safe_name, as_attachment=True)


@web_bp.route('/download/zip/<project_slug>', methods=['GET'])
def download_project_zip(project_slug):
    model_dir = Path(current_app.config['MODEL_DIR'])
    inference_dir = Path(current_app.config['INFERENCE_DIR']) / project_slug
    archive_name = f"{project_slug}_artifacts"

    if not inference_dir.exists() or not (model_dir / f"{project_slug}.keras").exists():
        logger.warning(f"Zip download missing artifacts for project: {project_slug}")
        abort(404)

    temp_dir = tempfile.mkdtemp()
    zip_path = Path(temp_dir) / f"{archive_name}.zip"

    try:
        with tempfile.TemporaryDirectory() as archive_temp:
            zip_root = Path(archive_temp) / 'project_artifacts'
            zip_root.mkdir(parents=True, exist_ok=True)

            # copy model
            shutil.copy(str(model_dir / f"{project_slug}.keras"), str(zip_root / f"model.keras"))

            # copy inference artifacts (if present)
            for artifact in ['scaler.pkl', 'label_encoders.pkl', 'target_encoder.pkl', 'requirements.txt', 'predict.py', 'README.md', 'sample_input.py']:
                source_file = inference_dir / artifact
                if source_file.exists():
                    shutil.copy(str(source_file), str(zip_root / artifact))

            shutil.make_archive(str(zip_path.with_suffix('')), 'zip', root_dir=str(Path(archive_temp)))

        @after_this_request
        def cleanup(response):
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass
            return response

        return send_file(str(zip_path), as_attachment=True)
    except Exception:
        if Path(temp_dir).exists():
            shutil.rmtree(temp_dir)
        raise


@web_bp.route('/download/dockerfile', methods=['GET'])
def download_dockerfile():
    project_root = Path(current_app.config['PROJECT_ROOT'])
    dockerfile_path = project_root / 'Dockerfile'

    if not dockerfile_path.exists():
        logger.warning(f"Dockerfile not found for download: {dockerfile_path}")
        abort(404)

    return send_from_directory(directory=str(dockerfile_path.parent), path=dockerfile_path.name, as_attachment=True)


@web_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    logger.info("Health check requested")
    return render_template("index.html"), 200


@web_bp.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size too large errors"""
    logger.warning(f"Request entity too large: {str(error)}")
    return render_template(
        "index.html",
        error="File size exceeds 25MB limit. Please upload a smaller file."
    ), 413