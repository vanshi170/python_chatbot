from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from storage.settings import settings_manager

class WelcomeScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setFixedSize(400, 300)
        
        # Apply local styling for the dialog depending on theme if we want,
        # but the global stylesheet handles it.
        self.setObjectName("AboutCard")
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Welcome to NexusChat")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4f8cff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        desc = QLabel("Your premium, rule-based desktop assistant.\nEnjoy a modern chat experience with no AI involved!")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        # Using a fixed color just for first launch, assuming dark mode
        desc.setStyleSheet("color: #94a3b8; font-size: 14px; margin-top: 20px; margin-bottom: 30px;")
        
        start_btn = QPushButton("Start Chatting")
        start_btn.setObjectName("StartButton")
        start_btn.setFixedSize(200, 40)
        start_btn.clicked.connect(self.start_chatting)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def start_chatting(self):
        settings_manager.set("first_launch", False)
        self.accept()
