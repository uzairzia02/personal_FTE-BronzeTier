"""
Constants for the AI Employee system.
"""

# Default intervals
DEFAULT_WATCH_INTERVAL = 10  # seconds
DEFAULT_REASONING_INTERVAL = 15  # seconds

# Directory paths
PROCESSED_FILES_PATH = 'processed_files.yml'

# Sensitive keywords that trigger approval requirements
SENSITIVE_KEYWORDS = [
    'password',
    'credential',
    'secret',
    'credit card',
    'ssn',
    'social security',
    'financial',
    'bank account',
    'personal information',
    'private data',
    'confidential',
    'contract',
    'agreement',
    'legal',
    'salary',
    'payroll',
    'hr',
    'human resources',
    'medical',
    'health information',
    'patient data',
    'authorization',
    'admin',
    'administrator',
    'root',
    'sudo',
    'security clearance',
    'classified',
    'proprietary',
    'trade secret',
    'nda',
    'non-disclosure',
    'payment',
    'transaction',
    'invoice',
    'purchase order',
    'tax',
    'audit',
    'compliance'
]

# Default configuration
DEFAULT_CONFIG = {
    'vault_path': './AI_Employee_Vault',
    'watch_dir': './watch_folder',
    'log_level': 'INFO',
    'max_file_size': 10 * 1024 * 1024,  # 10 MB
    'supported_file_types': ['.txt', '.md', '.csv', '.json', '.xml', '.pdf']
}