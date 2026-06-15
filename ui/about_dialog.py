from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os
import sys
from PyQt6.QtCore import qVersion
from storage.statistics import statistics_manager
from storage.settings import settings_manager

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        
        theme = settings_manager.get("theme", "dark")
        suffix = "white.svg" if theme == "dark" else "black.svg"
        base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "icons")
        self.setWindowIcon(QIcon(os.path.join(base_path, f"info_{suffix}")))
        
        self.setFixedSize(300, 300)
        self.setObjectName("AboutCard")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("NexusChat")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4f8cff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info = QLabel(f"""
Version: 1.0.0
Python: {sys.version.split(' ')[0]}
PyQt6: {qVersion()}
Build Date: June 2026

Total Messages Processed: {statistics_manager.stats.get("total_messages", 0)}
Bot Responses: {statistics_manager.stats.get("bot_responses", 0)}
Unknown Queries: {statistics_manager.stats.get("unknown_queries", 0)}
        """)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addStretch()
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
