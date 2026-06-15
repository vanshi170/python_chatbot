from PyQt6.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont, QColor

class SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(500, 300)
        pixmap.fill(QColor("#0f1117")) # Dark theme by default for splash
        super().__init__(pixmap)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("NexusChat")
        title_font = QFont("Segoe UI", 28, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white; background-color: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Version 1.0.0")
        subtitle.setStyleSheet("color: #94a3b8; font-size: 14px; background-color: transparent;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #2d3340;
                height: 4px;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #4f8cff;
                border-radius: 2px;
            }
        """)
        self.progress.setFixedSize(300, 4)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        # Assuming app loading takes ~1-2 seconds, so 1.5s total = 100 steps of 15ms
        self.timer.start(15) 

    def update_progress(self):
        self.counter += 1
        self.progress.setValue(self.counter)
        if self.counter >= 100:
            self.timer.stop()
