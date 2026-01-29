"""
Configuration file for Anomaly Detection System.
Centralizes parameters for security and reproducibility.
"""

import os
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'
RESULTS_DIR = PROJECT_ROOT / 'results'
MODELS_DIR = PROJECT_ROOT / 'models'

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Model Parameters
MODEL_CONFIG = {
    'contamination': float(os.getenv('CONTAMINATION', '0.1')),
    'random_state': int(os.getenv('RANDOM_STATE', '42')),
    'n_estimators': int(os.getenv('N_ESTIMATORS', '100')),
    'max_samples': os.getenv('MAX_SAMPLES', 'auto'),
    'n_jobs': int(os.getenv('N_JOBS', '-1'))
}

# Data Generation Parameters
DATA_CONFIG = {
    'n_samples': int(os.getenv('N_SAMPLES', '10000')),
    'n_features': int(os.getenv('N_FEATURES', '10')),
    'test_size': float(os.getenv('TEST_SIZE', '0.3'))
}

# Security Settings
SECURITY_CONFIG = {
    'validate_inputs': True,
    'log_sensitive_data': False,
    'max_file_size_mb': 100
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': str(RESULTS_DIR / 'pipeline.log')
}
