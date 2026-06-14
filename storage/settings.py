import json
import os
from pathlib import Path
from services.logger import logger

class SettingsManager:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        self.data_dir = base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.settings_file = self.data_dir / "settings.json"
        
        self.default_settings = {
            "theme": "dark",
            "animations_enabled": True,
            "auto_scroll": True,
            "show_timestamps": True,
            "first_launch": True,
            "window_geometry": None,
            "window_state": None
        }
        self.settings = self.load_settings()

    def load_settings(self):
        if not self.settings_file.exists():
            logger.info("Settings file not found. Creating default settings.")
            self.save_settings(self.default_settings)
            return self.default_settings.copy()
            
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Merge with defaults in case of new settings
                settings = self.default_settings.copy()
                settings.update(data)
                return settings
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            return self.default_settings.copy()

    def save_settings(self, settings_dict=None):
        if settings_dict is not None:
            self.settings = settings_dict
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

settings_manager = SettingsManager()
