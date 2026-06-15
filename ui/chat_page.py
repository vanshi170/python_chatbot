import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QScrollArea, QTextEdit, QPushButton, QFrame, QLabel, QScrollBar)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from widgets.message_bubble import MessageBubble
from widgets.typing_indicator import TypingIndicator
from widgets.quick_reply import QuickReplyButton
from services.chat_engine import chat_engine
from storage.chat_history import chat_history_manager

class ChatPage(QWidget):
    message_sent = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_history()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Chat History Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.scroll_content)
        
        # Typing indicator
        self.typing_indicator = TypingIndicator()
        self.typing_indicator.hide()
        self.scroll_layout.addWidget(self.typing_indicator)
        
        # Suggested Commands / Quick Replies Area
        self.quick_replies_container = QWidget()
        qr_layout = QVBoxLayout(self.quick_replies_container)
        qr_layout.setContentsMargins(10, 10, 10, 0)
        
        qr_title = QLabel("Suggested Commands:")
        qr_title.setStyleSheet("color: #94a3b8; font-size: 12px; background-color: transparent;")
        
        qr_buttons_layout = QHBoxLayout()
        qr_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        for text in ["Hello", "Help", "How are you", "Thanks", "Bye"]:
            btn = QuickReplyButton(text)
            btn.clicked.connect(lambda checked, t=text: self.send_message(t))
            qr_buttons_layout.addWidget(btn)
            
        qr_buttons_layout.addStretch()
        
        qr_layout.addWidget(qr_title)
        qr_layout.addLayout(qr_buttons_layout)
        
        # Input Area
        self.input_area = QFrame()
        self.input_area.setObjectName("InputArea")
        input_layout = QHBoxLayout(self.input_area)
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Type a message...")
        self.text_input.setMaximumHeight(80)
        self.text_input.installEventFilter(self) # For Shift+Enter support
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("SendButton")
        self.send_btn.setFixedSize(80, 40)
        self.send_btn.clicked.connect(self.on_send_clicked)
        
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.send_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        
        main_layout.addWidget(self.scroll_area, 1)
        main_layout.addWidget(self.quick_replies_container)
        main_layout.addWidget(self.input_area)

    def eventFilter(self, obj, event):
        if obj is self.text_input and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                    return False
                else:
                    self.on_send_clicked()
                    return True
        return super().eventFilter(obj, event)

    def load_history(self):
        messages = chat_history_manager.get_messages()
        for msg in messages:
            self.add_message_bubble(msg["text"], msg["sender"], msg["timestamp"], msg["sender"] == "User", animate=False)
        self.scroll_to_bottom()

    def on_send_clicked(self):
        text = self.text_input.toPlainText().strip()
        if text:
            self.send_message(text)
            
    def send_message(self, text):
        self.text_input.clear()
        
        now = datetime.datetime.now().strftime("%I:%M %p")
        
        chat_history_manager.add_message("User", text, now)
        self.add_message_bubble(text, "User", now, is_user=True, animate=True)
        
        self.message_sent.emit()
        
        self.typing_indicator.start()
        
        self.scroll_layout.removeWidget(self.typing_indicator)
        self.scroll_layout.addWidget(self.typing_indicator)
        
        self.scroll_to_bottom()
        
        QTimer.singleShot(600, lambda: self.process_bot_response(text))

    def process_bot_response(self, text):
        self.typing_indicator.stop()
        
        response = chat_engine.get_response(text)
        now = datetime.datetime.now().strftime("%I:%M %p")
        
        chat_history_manager.add_message("Bot", response, now)
        self.add_message_bubble(response, "Bot", now, is_user=False, animate=True)
        
        self.message_sent.emit()
        self.scroll_to_bottom()

    def add_message_bubble(self, text, sender, timestamp, is_user, animate=True):
        bubble = MessageBubble(text, sender, timestamp, is_user)
        
        count = self.scroll_layout.count()
        self.scroll_layout.insertWidget(count - 1, bubble)

    def scroll_to_bottom(self):
        QTimer.singleShot(10, self._scroll)

    def _scroll(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def clear_chat(self):
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        chat_history_manager.clear_history()

    def refresh_chat(self):
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.load_history()
