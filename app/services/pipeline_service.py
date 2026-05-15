from pathlib import Path

from app.utils.paths import ensure_dir, slugify
from ml.exporter import (
    generate_inference_script,
    generate_requirements_file,
    save_preprocessing_objects,
)
from ml.model_builder import build_model
from ml.preprocess import analyze_dataset, preprocess_data
from ml.trainer import evaluate_model, save_model, train_model


def run_pipeline(dataset_path: Path, project_name: str, target_column: str, config):
    analysis_result = analyze_dataset(str(dataset_path), target_column)
    df = analysis_result["dataframe"]
    task_type = analysis_result["task_type"]

    preprocess_result = preprocess_data(df, target_column, task_type)

    X_train = preprocess_result["X_train"]
    X_test = preprocess_result["X_test"]
    y_train = preprocess_result["y_train"]
    y_test = preprocess_result["y_test"]
    input_shape = preprocess_result["input_shape"]

    num_classes = None
    if task_type == "classification":
        num_classes = len(set(y_train))

    model = build_model(input_shape, task_type, num_classes=num_classes)
    history = train_model(model, X_train, y_train)
    evaluation = evaluate_model(model, X_test, y_test)

    model_dir = ensure_dir(Path(config.MODEL_DIR))
    inference_root = ensure_dir(Path(config.INFERENCE_DIR))

    project_slug = slugify(project_name)

    model_path = save_model(model, project_slug, model_dir)

    artifact_paths = save_preprocessing_objects(
        project_slug,
        preprocess_result["scaler"],
        preprocess_result["label_encoders"],
        preprocess_result["target_encoder"],
        inference_root,
    )

    requirements_path = generate_requirements_file(project_slug, inference_root)

    inference_script_path = generate_inference_script(
        project_slug,
        task_type,
        model_path=model_path,
        inference_root=inference_root,
        feature_columns=preprocess_result.get("feature_columns"),
    )

    return {
        "project_name": project_name,
        "project_slug": project_slug,
        "task_type": task_type,
        "model_path": str(model_path),
        "model_filename": model_path.name,
        "requirements_path": str(requirements_path),
        "inference_script_path": str(inference_script_path),
        "artifact_paths": {k: str(v) for k, v in artifact_paths.items()},
        "evaluation": evaluation,
        "history_keys": list(history.history.keys()),
    }