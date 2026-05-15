from pathlib import Path


def train_model(model, X_train, y_train):
    history = model.fit(
        X_train,
        y_train,
        epochs=20,
        batch_size=8,
        validation_split=0.2,
        verbose=1,
    )
    return history


def evaluate_model(model, X_test, y_test):
    evaluation_results = model.evaluate(X_test, y_test, verbose=0)
    metric_names = getattr(model, 'metrics_names', [])

    if isinstance(evaluation_results, (list, tuple)):
        return {name: value for name, value in zip(metric_names, evaluation_results)}

    return {metric_names[0] if metric_names else 'score': evaluation_results}


def save_model(model, project_slug: str, model_dir: Path) -> Path:
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / f"{project_slug}.keras"

    if model_path.exists():
        model_path.unlink()

    model.save(model_path)
    return model_path