from pathlib import Path
import joblib


def save_preprocessing_objects(
    project_slug: str,
    scaler,
    label_encoders,
    target_encoder,
    inference_root: Path,
):
    export_dir = inference_root / project_slug
    export_dir.mkdir(parents=True, exist_ok=True)

    # Save scaler
    scaler_path = export_dir / "scaler.pkl"
    joblib.dump(scaler, scaler_path)

    # Save label encoders
    encoders_path = export_dir / "label_encoders.pkl"
    joblib.dump(label_encoders, encoders_path)

    # Save target encoder
    target_encoder_path = export_dir / "target_encoder.pkl"
    joblib.dump(target_encoder, target_encoder_path)

    return {
        "scaler_path": scaler_path,
        "encoders_path": encoders_path,
        "target_encoder_path": target_encoder_path
    }


def generate_requirements_file(project_slug: str, inference_root: Path) -> Path:
    export_dir = inference_root / project_slug
    export_dir.mkdir(parents=True, exist_ok=True)

    # Generate an OS-safe requirements file. TensorFlow can be platform-specific
    # so we provide a comment and leave the final TensorFlow install to the
    # user / README where platform-specific instructions are documented.
    requirements_content = """
# Core python packages (version pins removed so pip can pick compatible builds)
pandas
numpy
scikit-learn
joblib

# TensorFlow is optional and platform-specific. See README.md for platform
# specific installation instructions (Windows / Intel Mac / Apple Silicon Mac).
# Example (Intel mac / Linux / Windows):
# tensorflow
# For Apple Silicon (M1/M2/M3) use:
# pip install tensorflow-macos tensorflow-metal
"""

    requirements_path = export_dir / "requirements.txt"
    with open(requirements_path, "w") as f:
        f.write(requirements_content.strip())

    return requirements_path


def generate_inference_script(
    project_slug: str,
    task_type: str,
    model_path: Path,
    inference_root: Path,
    feature_columns=None,
) -> Path:
    export_dir = inference_root / project_slug
    export_dir.mkdir(parents=True, exist_ok=True)

    scaler_path = export_dir / "scaler.pkl"
    encoders_path = export_dir / "label_encoders.pkl"
    target_encoder_path = export_dir / "target_encoder.pkl"

    # Build a beginner-friendly, robust predict.py script
    feature_cols_py = []
    if feature_columns:
        feature_cols_py = feature_columns

    # Precompute joined feature lines and a Python literal for expected columns
    feature_lines = ',\n'.join([f"    \"{c}\": [None]" for c in feature_cols_py])
    expected_columns_py = repr(feature_cols_py)

    inference_code = f"""
import sys
import os
import joblib
import pandas as pd
import numpy as np

from tensorflow.keras.models import load_model

# ------------------------- User editable section -------------------------
# Where to add input data:
# Replace the `data` dict below with your own input values or load from CSV.
# The keys must match the original feature column names used during training.
# ------------------------------------------------------------------------

# Example input (one row). Update values to match your dataset columns and types.
data = {{
{feature_lines}
}}

df = pd.DataFrame(data)

# -------------------- Load model & preprocessing objects -----------------
model = load_model(r"{model_path}")
scaler = joblib.load(r"{scaler_path}")
label_encoders = joblib.load(r"{encoders_path}")
target_encoder = joblib.load(r"{target_encoder_path}")

# -------------------- Input validation & reordering ---------------------
# Ensure we work with a copy to avoid editing original data
df = df.copy()

# Drop any extra columns that were not used during training
expected_columns = {expected_columns_py}
extra = [c for c in df.columns if c not in expected_columns]
if extra:
    print("Warning: dropping extra columns not used during training: {{}}".format(extra))
    df = df.drop(columns=extra)

# Check for missing columns required by the model
missing = [c for c in expected_columns if c not in df.columns]
if missing:
    raise ValueError("Missing required columns for prediction: {{}}. Please provide these columns with the exact names used during training.".format(missing))

# Reorder columns to match training order
df = df[expected_columns]

# Handle categorical columns (object / string dtypes)
for col in df.select_dtypes(include=['object', 'string']).columns:
    if col in label_encoders:
        # Check for unseen labels and provide a clear message
        known = set(label_encoders[col].classes_)
        provided = set(df[col].dropna().astype(str).unique())
        unseen = provided - known
        if unseen:
            raise ValueError(
                "Column '{{}}' contains unseen categorical values: {{}}.\n"
                "Make sure categorical values exactly match those used in training.\n"
                "You can update your input or retrain the model to include new categories.".format(col, sorted(list(unseen)))
            )
        # Safe transform
        try:
            df[col] = label_encoders[col].transform(df[col])
        except Exception as e:
            raise ValueError("Error encoding column '{{}}': {{}}".format(col, e))

# Fill any remaining NaNs (basic safety)
for col in df.columns:
    if df[col].dtype.kind in 'biufc':
        df[col] = df[col].fillna(0)
    else:
        df[col] = df[col].fillna('')

# Scale input
try:
    X_scaled = scaler.transform(df)
except Exception as e:
    raise RuntimeError("Failed to scale input features: {{}}".format(e))

# Predict
prediction = model.predict(X_scaled)

print("\\nRAW PREDICTION:")
print(prediction)

if "{task_type}" == "classification":
    predicted_class = np.argmax(prediction, axis=1)
    if target_encoder is not None:
        try:
            predicted_class = target_encoder.inverse_transform(predicted_class)
        except Exception:
            pass
    print("\\nFINAL CLASS:")
    print(predicted_class)
else:
    print("\\nPREDICTED VALUE:")
    # If model returns shape (n,1)
    if prediction.ndim == 2 and prediction.shape[1] == 1:
        print(prediction[0][0])
    else:
        print(prediction)

# ------------------------- How to run -----------------------------------
# Save this file and run: python predict.py
# For batch predictions, replace the `data` dict with a loaded DataFrame
# (e.g., df = pd.read_csv('input.csv')) and ensure column names match.
# ------------------------------------------------------------------------
"""

    inference_path = export_dir / "predict.py"
    with open(inference_path, "w") as f:
        f.write(inference_code)

    # Generate a small sample_input.py to show an example input structure
    sample_lines = [
        "# Sample input helper for beginners",
        "import pandas as pd",
        "",
        "data = {",
    ]
    for c in feature_cols_py:
        sample_lines.append(f"    \"{c}\": [None],")
    sample_lines.append("}")
    sample_lines.append("")
    sample_lines.append("df = pd.DataFrame(data)")
    sample_lines.append("print(\"Sample input DataFrame:\")")
    sample_lines.append("print(df)")

    sample_path = export_dir / "sample_input.py"
    with open(sample_path, "w") as f:
        f.write("\n".join(sample_lines))

    # Create a README.md for the exported artifacts (beginner friendly)
    readme_text = f"""# {project_slug} - Inference Artifacts

This folder contains the exported model and helper files to run predictions locally.

Files included:
- `predict.py` - A beginner-friendly script to run a single-row prediction.
- `sample_input.py` - Example input structure for `predict.py`.
- `requirements.txt` - Base Python dependencies (TensorFlow installation is platform-specific).
- `scaler.pkl`, `label_encoders.pkl`, `target_encoder.pkl` - Preprocessing objects.
- `{project_slug}.keras` - Trained Keras model file.

How to use:
1. Install dependencies (see requirements.txt). For TensorFlow see the main project README for platform-specific instructions.
2. Edit `sample_input.py` or open `predict.py` and replace the `data` dictionary with your own values.
3. Run `python predict.py` to get a prediction.

Important:
- Categorical values must exactly match those used during training.
- Deleting the preprocessing files or model file will break predictions.
"""

    readme_path = export_dir / "README.md"
    with open(readme_path, "w") as f:
        f.write(readme_text)

    return inference_path