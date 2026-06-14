from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtProperty, QTimer, QEasingCurve

class Toast(QWidget):
    def __init__(self, text, parent=None, duration=3000):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        self._opacity = 0.0
        
        layout = QVBoxLayout(self)
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(34, 197, 94, 0.9);
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.label)
        
        self.duration = duration
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fade_out)
        
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    def show_toast(self):
        self.show()
        
        self.anim_in = QPropertyAnimation(self, b"opacity")
        self.anim_in.setDuration(300)
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim_in.start()
        
        self.timer.start(self.duration)

    def fade_out(self):
        self.anim_out = QPropertyAnimation(self, b"opacity")
        self.anim_out.setDuration(300)
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim_out.finished.connect(self.close)
        self.anim_out.start()
