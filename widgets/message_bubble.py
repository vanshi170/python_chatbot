import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QMenu)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QCursor, QAction
from PyQt6.QtWidgets import QApplication

class MessageBubble(QWidget):
    def __init__(self, text, sender, timestamp, is_user=True, parent=None):
        super().__init__(parent)
        self.text = text
        self.sender_name = sender
        self.timestamp = timestamp
        self.is_user = is_user
        
        self.init_ui()
        
    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 5, 0, 5)
        
        # Avatar (Placeholder for now, can be an icon later)
        avatar_label = QLabel()
        avatar_label.setFixedSize(32, 32)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_label.setStyleSheet("border-radius: 16px; background-color: #4f8cff; color: white; font-weight: bold;")
        if self.is_user:
            avatar_label.setText("U")
        else:
            avatar_label.setStyleSheet("border-radius: 16px; background-color: #22c55e; color: white; font-weight: bold;")
            avatar_label.setText("B")
            
        # Message Container
        msg_container = QFrame()
        msg_container.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        msg_container.customContextMenuRequested.connect(self.show_context_menu)
        
        # Bubble styling based on sender
        if self.is_user:
            msg_container.setStyleSheet("""
                QFrame {
                    background-color: #4f8cff;
                    color: white;
                    border-radius: 12px;
                    border-top-right-radius: 2px;
                }
            """)
            time_color = "rgba(255, 255, 255, 0.7)"
            text_color = "white"
        else:
            msg_container.setObjectName("BotBubble")
            msg_container.setStyleSheet("""
                QFrame#BotBubble {
                    background-color: #2d3340; 
                    color: white;
                    border-radius: 12px;
                    border-top-left-radius: 2px;
                }
            """)
            time_color = "rgba(255, 255, 255, 0.5)"
            text_color = "white"
            
        container_layout = QVBoxLayout(msg_container)
        container_layout.setContentsMargins(12, 10, 12, 10)
        
        text_label = QLabel(self.text)
        text_label.setWordWrap(True)
        text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text_label.setStyleSheet(f"background-color: transparent; color: {text_color};")
        
        time_label = QLabel(self.timestamp)
        time_font = QFont()
        time_font.setPointSize(8)
        time_label.setFont(time_font)
        time_label.setStyleSheet(f"color: {time_color}; background-color: transparent;")
        
        from storage.settings import settings_manager
        if not settings_manager.get("show_timestamps", True):
            time_label.hide()
        
        container_layout.addWidget(text_label)
        container_layout.addWidget(time_label, alignment=Qt.AlignmentFlag.AlignRight)
        
        if self.is_user:
            main_layout.addStretch()
            main_layout.addWidget(msg_container)
            main_layout.addWidget(avatar_label)
        else:
            main_layout.addWidget(avatar_label)
            main_layout.addWidget(msg_container)
            main_layout.addStretch()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        copy_action = QAction("Copy Message", self)
        copy_action.triggered.connect(self.copy_message)
        menu.addAction(copy_action)
        menu.exec(QCursor.pos())

    def copy_message(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text)
