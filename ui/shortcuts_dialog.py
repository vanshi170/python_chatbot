from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class ShortcutsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts")
        self.setFixedSize(300, 250)
        self.setObjectName("AboutCard")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Keyboard Shortcuts")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        shortcuts = {
            "Enter": "Send Message",
            "Shift + Enter": "New Line",
            "Ctrl + L": "Clear Chat",
            "Ctrl + D": "Toggle Theme",
            "Ctrl + F": "Search Messages",
            "F1": "Help (This Dialog)"
        }
        
        for key, desc in shortcuts.items():
            label = QLabel(f"<b>{key}</b> : {desc}")
            layout.addWidget(label)
            
        layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
