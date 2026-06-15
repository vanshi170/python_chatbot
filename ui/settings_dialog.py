from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os
from storage.settings import settings_manager
from storage.chat_history import chat_history_manager
from widgets.toast import Toast

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        
        theme = settings_manager.get("theme", "dark")
        suffix = "white.svg" if theme == "dark" else "black.svg"
        base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "icons")
        self.setWindowIcon(QIcon(os.path.join(base_path, f"settings_{suffix}")))
        
        self.setFixedSize(400, 350)
        self.setObjectName("SettingsCard")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Theme
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setCurrentText(settings_manager.get("theme", "dark").capitalize())
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)
        
        # Checkboxes
        self.animations_cb = QCheckBox("Enable Animations")
        self.animations_cb.setChecked(settings_manager.get("animations_enabled", True))
        layout.addWidget(self.animations_cb)
        
        self.auto_scroll_cb = QCheckBox("Auto Scroll to Bottom")
        self.auto_scroll_cb.setChecked(settings_manager.get("auto_scroll", True))
        layout.addWidget(self.auto_scroll_cb)
        
        self.timestamps_cb = QCheckBox("Show Timestamps")
        self.timestamps_cb.setChecked(settings_manager.get("show_timestamps", True))
        layout.addWidget(self.timestamps_cb)
        
        # Export / Import
        export_btn = QPushButton("Export Chat History (JSON)")
        export_btn.clicked.connect(self.export_json)
        layout.addWidget(export_btn)
        
        export_txt_btn = QPushButton("Export Chat History (TXT)")
        export_txt_btn.clicked.connect(self.export_txt)
        layout.addWidget(export_txt_btn)
        
        import_btn = QPushButton("Import Chat History (JSON)")
        import_btn.clicked.connect(self.import_json)
        layout.addWidget(import_btn)
        
        layout.addStretch()
        
        # Save Button
        save_btn = QPushButton("Save Settings")
        save_btn.setObjectName("StartButton")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def save_settings(self):
        settings_manager.set("theme", self.theme_combo.currentText().lower())
        settings_manager.set("animations_enabled", self.animations_cb.isChecked())
        settings_manager.set("auto_scroll", self.auto_scroll_cb.isChecked())
        settings_manager.set("show_timestamps", self.timestamps_cb.isChecked())
        self.accept()
        if hasattr(self.parent(), 'chat_page'):
            self.parent().chat_page.refresh_chat()
        
    def export_json(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export JSON", "", "JSON Files (*.json)")
        if path:
            chat_history_manager.export_history(path, "json")
            Toast("Exported JSON successfully", self).show_toast()

    def export_txt(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export TXT", "", "Text Files (*.txt)")
        if path:
            chat_history_manager.export_history(path, "txt")
            Toast("Exported TXT successfully", self).show_toast()

    def import_json(self):
        if len(chat_history_manager.get_messages()) > 0:
            reply = QMessageBox.question(self, "Save Ongoing Chat", "There is an ongoing chat. Do you want to save it before importing?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Yes:
                path, _ = QFileDialog.getSaveFileName(self, "Export JSON", "", "JSON Files (*.json)")
                if path:
                    chat_history_manager.export_history(path, "json")
                else:
                    return
            elif reply == QMessageBox.StandardButton.Cancel:
                return
                
        path, _ = QFileDialog.getOpenFileName(self, "Import JSON", "", "JSON Files (*.json)")
        if path:
            chat_history_manager.clear_history()
            if chat_history_manager.import_history(path):
                Toast("Imported successfully", self).show_toast()
                if hasattr(self.parent(), 'chat_page'):
                    self.parent().chat_page.refresh_chat()
            else:
                Toast("Failed to import history", self).show_toast()
