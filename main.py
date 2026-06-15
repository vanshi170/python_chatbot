import sys
import os

# Add the root directory to sys.path before any imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.splash_screen import SplashScreen
from ui.main_window import MainWindow
from ui.welcome_screen import WelcomeScreen
from storage.settings import settings_manager
from styles.theme_manager import theme_manager
from services.logger import logger
from PyQt6.QtCore import QTimer

def main():
    logger.info("Starting ChatMate-PyQt...")
    app = QApplication(sys.argv)
    
    # Apply initial theme
    theme_manager.apply_theme(app)
    
    # Show Splash Screen
    splash = SplashScreen()
    splash.show()
    
    # Process events so splash screen animation runs
    while splash.timer.isActive():
        app.processEvents()
        
    splash.close()
    
    main_window = MainWindow()
    main_window.show()
        
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
