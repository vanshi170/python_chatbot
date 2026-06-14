import json
import os
from pathlib import Path
from services.logger import logger

class StatisticsManager:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        self.data_dir = base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.stats_file = self.data_dir / "stats.json"
        
        self.default_stats = {
            "total_messages": 0,
            "bot_responses": 0,
            "unknown_queries": 0,
            "command_usage": {} # command -> count
        }
        self.stats = self.load_stats()
        
        # Session stats
        self.session_messages = 0
        self.session_bot_responses = 0

    def load_stats(self):
        if not self.stats_file.exists():
            return self.default_stats.copy()
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                stats = self.default_stats.copy()
                stats.update(data)
                return stats
        except Exception as e:
            logger.error(f"Failed to load statistics: {e}")
            return self.default_stats.copy()

    def save_stats(self):
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save statistics: {e}")

    def track_user_message(self, command=None):
        self.stats["total_messages"] += 1
        self.session_messages += 1
        
        if command:
            cmd = command.lower()
            self.stats["command_usage"][cmd] = self.stats["command_usage"].get(cmd, 0) + 1
            
        self.save_stats()

    def track_bot_response(self, is_unknown=False):
        self.stats["bot_responses"] += 1
        self.session_bot_responses += 1
        
        if is_unknown:
            self.stats["unknown_queries"] += 1
            
        self.save_stats()
        
    def get_most_used_command(self):
        usage = self.stats.get("command_usage", {})
        if not usage:
            return "None"
        return max(usage, key=usage.get)

    def get_unknown_percentage(self):
        total = self.stats.get("bot_responses", 0)
        if total == 0:
            return 0.0
        return (self.stats.get("unknown_queries", 0) / total) * 100.0

statistics_manager = StatisticsManager()
