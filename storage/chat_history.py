import json
import os
from pathlib import Path
from services.logger import logger

class ChatHistoryManager:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        self.data_dir = base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "history.json"
        self.messages = self.load_history()

    def load_history(self):
        if not self.history_file.exists():
            return []
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load chat history: {e}")
            return []

    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save chat history: {e}")

    def add_message(self, sender, text, timestamp):
        msg = {
            "sender": sender,
            "text": text,
            "timestamp": timestamp
        }
        self.messages.append(msg)
        self.save_history() # Auto-save protection
        return msg

    def clear_history(self):
        self.messages = []
        self.save_history()
        logger.info("Chat history cleared.")

    def get_messages(self):
        return self.messages

    def export_history(self, file_path, format="json"):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if format == "json":
                    json.dump(self.messages, f, indent=4)
                elif format == "txt":
                    for msg in self.messages:
                        f.write(f"[{msg['timestamp']}] {msg['sender']}: {msg['text']}\n")
            logger.info(f"Chat history exported to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export chat history: {e}")
            return False

    def import_history(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_messages = json.load(f)
                if isinstance(imported_messages, list):
                    # Validate format basically
                    if all(all(k in m for k in ("sender", "text", "timestamp")) for m in imported_messages):
                        self.messages.extend(imported_messages)
                        self.save_history()
                        logger.info(f"Chat history imported from {file_path}")
                        return True
            return False
        except Exception as e:
            logger.error(f"Failed to import chat history: {e}")
            return False

chat_history_manager = ChatHistoryManager()
