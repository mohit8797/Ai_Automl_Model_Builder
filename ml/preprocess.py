import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


def analyze_dataset(file_path, target_column):

    # Read CSV
    df = pd.read_csv(file_path)

    print("\nDATASET PREVIEW:")
    print(df.head())

    print("\nDATASET SHAPE:")
    print(df.shape)

    print("\nCOLUMN TYPES:")
    print(df.dtypes)

    print("\nMISSING VALUES:")
    print(df.isnull().sum())

    # Detect task type
    task_type = detect_task_type(df, target_column)

    print("\nDETECTED TASK TYPE:", task_type)

    return {
        "dataframe": df,
        "task_type": task_type
    }


def detect_task_type(df, target_column):

    target = df[target_column]

    unique_values = target.nunique()

    # If object/string → classification
    if str(target.dtype) in ('object', 'string'):
        return "classification"

    # Small unique numeric values → classification
    elif unique_values <= 10:
        return "classification"

    # Otherwise regression
    else:
        return "regression"

def preprocess_data(df, target_column, task_type):

    # Separate features and target
    X = df.drop(columns=[target_column])

    y = df[target_column]

    # Detect categorical columns (handle both object and pandas string dtypes)
    categorical_cols = X.select_dtypes(include=['object', 'string']).columns

    # Detect numerical columns (exclude object/string dtypes)
    numerical_cols = X.select_dtypes(exclude=['object', 'string']).columns

    print("\nCATEGORICAL COLUMNS:")
    print(categorical_cols)

    print("\nNUMERICAL COLUMNS:")
    print(numerical_cols)

    # Handle missing values
    for col in numerical_cols:
        X[col] = X[col].fillna(X[col].mean())

    for col in categorical_cols:
        X[col] = X[col].fillna(X[col].mode()[0])

    # Encode categorical features
    label_encoders = {}

    for col in categorical_cols:

        le = LabelEncoder()

        X[col] = le.fit_transform(X[col])

        label_encoders[col] = le

    # Encode target if classification
    target_encoder = None

    if task_type == "classification":

        target_encoder = LabelEncoder()

        y = target_encoder.fit_transform(y)

    # Feature scaling
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.2,
        random_state=42
    )

    print("\nTRAIN TEST SPLIT COMPLETE")

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "scaler": scaler,
        "label_encoders": label_encoders,
        "target_encoder": target_encoder,
        "input_shape": X_train.shape[1],
        # keep the original feature column order so exported inference can reorder inputs
        "feature_columns": list(X.columns)
    }