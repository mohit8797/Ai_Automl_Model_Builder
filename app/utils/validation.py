"""
Validation utilities for form inputs and files
"""

import os
import pandas as pd
from app.logger import get_logger, ValidationException

logger = get_logger('validation')

# Allowed file extensions
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    if "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def validate_file_size(file_size: int, max_size: int = MAX_FILE_SIZE) -> bool:
    """Validate file size"""
    return file_size <= max_size


def validate_project_name(project_name: str) -> bool:
    """Validate project name"""
    project_name = project_name.strip()
    if not project_name or len(project_name) > 100:
        raise ValidationException("Project name must be between 1 and 100 characters")
    return True


def validate_problem_statement(problem_statement: str) -> bool:
    """Validate problem statement"""
    problem_statement = problem_statement.strip()
    if not problem_statement or len(problem_statement) > 1000:
        raise ValidationException("Problem statement must be between 1 and 1000 characters")
    return True


def validate_target_column(target_column: str) -> bool:
    """Validate target column name"""
    target_column = target_column.strip()
    if not target_column or len(target_column) > 100:
        raise ValidationException("Target column must be between 1 and 100 characters")
    if not target_column.replace('_', '').replace('-', '').isalnum():
        raise ValidationException("Target column must contain only alphanumeric characters, hyphens, and underscores")
    return True


def validate_problem_type(problem_type: str) -> bool:
    """Validate problem type"""
    valid_types = ['classification', 'regression', 'clustering', 'anomaly_detection']
    if problem_type not in valid_types:
        raise ValidationException(f"Problem type must be one of: {', '.join(valid_types)}")
    return True


def validate_csv_file(file_path: str) -> dict:
    """
    Validate and analyze CSV file
    Returns metadata about the file
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        if df.empty:
            raise ValidationException("CSV file is empty")
        
        if len(df.columns) == 0:
            raise ValidationException("CSV file has no columns")
        
        metadata = {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
        }
        
        logger.info(f"CSV validation successful: {len(df)} rows, {len(df.columns)} columns")
        return metadata
        
    except pd.errors.ParserError as e:
        raise ValidationException(f"Invalid CSV format: {str(e)}")
    except Exception as e:
        raise ValidationException(f"Error reading CSV file: {str(e)}")


def validate_form_input(data: dict) -> dict:
    """
    Validate all form inputs
    Returns cleaned/validated data
    """
    try:
        # Validate project name
        project_name = (data.get('project_name') or '').strip()
        validate_project_name(project_name)
        
        # Validate problem statement
        problem_statement = (data.get('problem_statement') or '').strip()
        validate_problem_statement(problem_statement)
        
        # Validate target column
        target_column = (data.get('target_column') or '').strip()
        validate_target_column(target_column)
        
        # Validate problem type if provided
        problem_type = data.get('problem_type', 'classification')
        if problem_type:
            validate_problem_type(problem_type)
        
        logger.info(f"Form validation successful for project: {project_name}")
        
        return {
            'project_name': project_name,
            'problem_statement': problem_statement,
            'target_column': target_column,
            'problem_type': problem_type,
        }
        
    except ValidationException:
        raise
    except Exception as e:
        logger.error(f"Form validation error: {str(e)}")
        raise ValidationException(f"Invalid form input: {str(e)}")
