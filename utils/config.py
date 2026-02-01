"""
Configuration management for the AI Employee system.
"""

import os
import json
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class ConfigManager:
    """
    Manages configuration for the AI Employee system.
    Loads settings from various sources with proper precedence.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.settings = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from various sources with precedence:
        1. Environment variables
        2. Config file (if specified)
        3. Default values

        Returns:
            Dictionary containing all settings
        """
        settings = self.get_defaults()

        # Load from config file if it exists
        if self.config_path and os.path.exists(self.config_path):
            file_settings = self.load_from_file(self.config_path)
            settings.update(file_settings)

        # Override with environment variables
        env_settings = self.load_from_env()
        settings.update(env_settings)

        return settings

    def get_defaults(self) -> Dict[str, Any]:
        """
        Get default configuration values.

        Returns:
            Dictionary of default settings
        """
        return {
            'vault_path': './AI_Employee_Vault',
            'watch_dir': './watch_folder',
            'watch_interval': 10,
            'reasoning_interval': 15,
            'log_level': 'INFO',
            'max_file_size': 10 * 1024 * 1024,  # 10 MB
            'supported_file_types': ['.txt', '.md', '.csv', '.json', '.xml'],
            'sensitive_keywords': [
                'password', 'credential', 'secret', 'credit card', 'ssn',
                'social security', 'financial', 'bank account', 'personal information'
            ],
            'single_cycle': False,
            'debug': False
        }

    def load_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load configuration from a file (JSON or YAML).

        Args:
            file_path: Path to the configuration file

        Returns:
            Dictionary of settings from file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.lower().endswith('.json'):
                    return json.load(f)
                else:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading config from {file_path}: {str(e)}")
            return {}

    def load_from_env(self) -> Dict[str, Any]:
        """
        Load configuration from environment variables.

        Returns:
            Dictionary of settings from environment
        """
        env_mapping = {
            'VAULT_PATH': 'vault_path',
            'WATCH_DIR': 'watch_dir',
            'WATCH_INTERVAL': 'watch_interval',
            'REASONING_INTERVAL': 'reasoning_interval',
            'LOG_LEVEL': 'log_level',
            'MAX_FILE_SIZE': 'max_file_size',
            'SINGLE_CYCLE': 'single_cycle',
            'DEBUG': 'debug'
        }

        settings = {}
        for env_var, config_key in env_mapping.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # Convert string values to appropriate types
                if config_key in ['watch_interval', 'reasoning_interval', 'max_file_size']:
                    try:
                        settings[config_key] = int(env_value)
                    except ValueError:
                        print(f"Warning: Could not convert {env_var} to integer, using default")
                elif config_key in ['single_cycle', 'debug']:
                    settings[config_key] = env_value.lower() in ['true', '1', 'yes', 'on']
                else:
                    settings[config_key] = env_value

        return settings

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        """
        Set a configuration value.

        Args:
            key: Configuration key
            value: Value to set
        """
        self.settings[key] = value

    def save_to_file(self, file_path: str, format: str = 'yaml'):
        """
        Save current configuration to a file.

        Args:
            file_path: Path to save the configuration
            format: Format to save in ('yaml' or 'json')

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                if format.lower() == 'json':
                    json.dump(self.settings, f, indent=2)
                else:  # YAML
                    yaml.dump(self.settings, f, default_flow_style=False)

            return True
        except Exception as e:
            print(f"Error saving config to {file_path}: {str(e)}")
            return False

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate the configuration settings.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Validate vault path
        if not self.settings.get('vault_path'):
            errors.append("vault_path is required")

        # Validate intervals
        watch_interval = self.settings.get('watch_interval', 10)
        reasoning_interval = self.settings.get('reasoning_interval', 15)

        if not isinstance(watch_interval, int) or watch_interval <= 0:
            errors.append("watch_interval must be a positive integer")

        if not isinstance(reasoning_interval, int) or reasoning_interval <= 0:
            errors.append("reasoning_interval must be a positive integer")

        # Validate max file size
        max_file_size = self.settings.get('max_file_size', 10 * 1024 * 1024)
        if not isinstance(max_file_size, int) or max_file_size <= 0:
            errors.append("max_file_size must be a positive integer")

        return len(errors) == 0, errors


def get_config(config_path: Optional[str] = None) -> ConfigManager:
    """
    Convenience function to get a configuration manager instance.

    Args:
        config_path: Optional path to configuration file

    Returns:
        ConfigManager instance
    """
    return ConfigManager(config_path)