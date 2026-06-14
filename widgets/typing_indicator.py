from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer

class TypingIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel("Bot is typing")
        self.label.setStyleSheet("color: #94a3b8; font-style: italic; background-color: transparent;")
        
        layout.addWidget(self.label)
        layout.addStretch()
        
        self.dots = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dots)
        
    def start(self):
        self.dots = 0
        self.label.setText("Bot is typing")
        self.show()
        self.timer.start(300)
        
    def stop(self):
        self.timer.stop()
        self.hide()
        
    def update_dots(self):
        self.dots = (self.dots + 1) % 4
        text = "Bot is typing" + "." * self.dots
        self.label.setText(text)
