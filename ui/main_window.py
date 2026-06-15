import os
import datetime
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QMessageBox, QStatusBar, QLineEdit)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QAction, QKeySequence, QShortcut, QIcon
from ui.chat_page import ChatPage
from ui.settings_dialog import SettingsDialog
from ui.about_dialog import AboutDialog
from ui.shortcuts_dialog import ShortcutsDialog
from storage.settings import settings_manager
from storage.statistics import statistics_manager
from styles.theme_manager import theme_manager
from widgets.toast import Toast

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatMate-PyQt")
        self.setMinimumSize(1000, 700)
        
        # Restore geometry if available
        geometry = settings_manager.get("window_geometry")
        if geometry and len(geometry) == 4:
            self.setGeometry(*geometry)
            
        if settings_manager.get("window_state") == "maximized":
            self.showMaximized()
            
        self.init_ui()
        self.init_shortcuts()
        
        self.init_status_bar()

    def init_ui(self):
        self.setWindowTitle("NexusChat")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Header ---
        self.header = QWidget()
        self.header.setObjectName("HeaderWidget")
        self.header.setFixedHeight(60)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        title_label = QLabel("NexusChat")
        title_label.setObjectName("HeaderTitle")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search messages...")
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(self.on_search)
        self.search_input.hide() # Hidden by default, shown via Ctrl+F
        
        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(48, 48)
        self.theme_btn.setIconSize(QSize(28, 28))
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        self.clear_btn = QPushButton("Clear Chat")
        self.clear_btn.setFixedHeight(48)
        self.clear_btn.clicked.connect(self.clear_chat)
        
        self.settings_btn = QPushButton()
        self.settings_btn.setFixedSize(48, 48)
        self.settings_btn.setIconSize(QSize(28, 28))
        self.settings_btn.clicked.connect(self.show_settings)
        
        self.about_btn = QPushButton()
        self.about_btn.setFixedSize(48, 48)
        self.about_btn.setIconSize(QSize(28, 28))
        self.about_btn.clicked.connect(self.show_about)
        
        self.update_icons()
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.search_input)
        header_layout.addWidget(self.theme_btn)
        header_layout.addWidget(self.clear_btn)
        header_layout.addWidget(self.about_btn)
        header_layout.addWidget(self.settings_btn)
        
        # --- Chat Page ---
        self.chat_page = ChatPage()
        
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.chat_page)

    def init_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def init_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+L"), self).activated.connect(self.clear_chat)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self.toggle_theme)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.toggle_search)
        QShortcut(QKeySequence("F1"), self).activated.connect(self.show_shortcuts)

    def toggle_theme(self):
        current = settings_manager.get("theme", "dark")
        new_theme = "light" if current == "dark" else "dark"
        
        from PyQt6.QtWidgets import QApplication
        theme_manager.apply_theme(QApplication.instance(), new_theme)
        self.update_icons()
        Toast(f"Switched to {new_theme} theme", self).show_toast()

    def clear_chat(self):
        reply = QMessageBox.question(self, "Clear Chat", "Are you sure you want to clear the conversation history?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.chat_page.clear_chat()
            Toast("Chat history cleared", self).show_toast()

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()
        
        new_theme = settings_manager.get("theme", "dark")
        self.update_icons()
        from PyQt6.QtWidgets import QApplication
        theme_manager.apply_theme(QApplication.instance(), new_theme)

    def update_icons(self):
        theme = settings_manager.get("theme", "dark")
        base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "icons")
        
        suffix = "white.svg" if theme == "dark" else "black.svg"
        
        self.setWindowIcon(QIcon(os.path.join(base_path, f"logo_{suffix}")))
        self.settings_btn.setIcon(QIcon(os.path.join(base_path, f"settings_{suffix}")))
        self.about_btn.setIcon(QIcon(os.path.join(base_path, f"info_{suffix}")))
        
        if theme == "dark":
            self.theme_btn.setIcon(QIcon(os.path.join(base_path, "sun_white.svg")))
        else:
            self.theme_btn.setIcon(QIcon(os.path.join(base_path, "moon_black.svg")))

    def show_about(self):
        AboutDialog(self).exec()

    def show_shortcuts(self):
        ShortcutsDialog(self).exec()

    def toggle_search(self):
        if self.search_input.isVisible():
            self.search_input.hide()
            self.search_input.clear()
        else:
            self.search_input.show()
            self.search_input.setFocus()

    def on_search(self, text):
        text = text.lower()
        count = 0
        for i in range(self.chat_page.scroll_layout.count()):
            item = self.chat_page.scroll_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if hasattr(widget, 'text'):
                    if text in widget.text.lower():
                        widget.setStyleSheet("border: 2px solid #22c55e;")
                        count += 1
                    else:
                        widget.setStyleSheet("")
        if text:
            self.status.showMessage(f"{count} results found", 3000)
        else:
            self.status.clearMessage()

    def closeEvent(self, event):
        settings_manager.set("window_geometry", [self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()])
        if self.isMaximized():
            settings_manager.set("window_state", "maximized")
        else:
            settings_manager.set("window_state", "normal")
        event.accept()
