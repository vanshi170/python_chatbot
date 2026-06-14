import os
from pathlib import Path
from storage.settings import settings_manager
from services.logger import logger

class ThemeManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        # Currently supported themes
        self.available_themes = ["dark", "light"]
        # Future architecture
        self.future_themes = ["midnight", "ocean", "emerald"]

    def load_theme(self, theme_name):
        if theme_name not in self.available_themes:
            logger.warning(f"Theme '{theme_name}' not fully implemented. Falling back to dark.")
            theme_name = "dark"
            
        qss_file = self.base_dir / f"{theme_name}.qss"
        if not qss_file.exists():
            logger.error(f"Stylesheet {qss_file} not found!")
            return ""
            
        try:
            with open(qss_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read stylesheet {theme_name}: {e}")
            return ""

    def apply_theme(self, app, theme_name=None):
        if theme_name is None:
            theme_name = settings_manager.get("theme", "dark")
            
        stylesheet = self.load_theme(theme_name)
        if stylesheet:
            app.setStyleSheet(stylesheet)
            settings_manager.set("theme", theme_name)
            logger.info(f"Theme applied: {theme_name}")
            return True
        return False

theme_manager = ThemeManager()
