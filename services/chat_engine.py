import string
import re
from storage.statistics import statistics_manager
from services.logger import logger

class ChatEngine:
    def __init__(self):
        # Dictionary mapping normalized intents to responses
        self.rules = {
            "hello": "Hi!",
            "how are you": "I'm fine, thanks!",
            "bye": "Goodbye!",
            "thanks": "You're welcome!",
            "help": "Available commands:\n- Hello\n- How are you\n- Thanks\n- Bye",
        }
        
        # Variations mapped to main intents
        self.variations = {
            "hi": "hello",
            "hey": "hello",
            "good morning": "hello",
            "good evening": "hello",
            
            "how are you doing": "how are you",
            "hows it going": "how are you",
            
            "goodbye": "bye",
            "see you": "bye",
            "exit": "bye",
            
            "thank you": "thanks",
            "thx": "thanks"
        }

    def normalize_input(self, text):
        """
        Convert to lowercase, trim whitespace, remove repeated spaces,
        and remove common punctuation.
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove repeated spaces and trim
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def match_command(self, normalized_text):
        """
        Match the normalized text against variations and rules.
        """
        # 1. Check if it's a variation
        if normalized_text in self.variations:
            intent = self.variations[normalized_text]
        else:
            intent = normalized_text
            
        # 2. Match against rules
        if intent in self.rules:
            return intent, self.rules[intent]
            
        return None, None

    def get_response(self, text):
        logger.info(f"Processing input: {text}")
        normalized = self.normalize_input(text)
        
        intent, response = self.match_command(normalized)
        
        if response:
            statistics_manager.track_user_message(command=intent)
            statistics_manager.track_bot_response(is_unknown=False)
            logger.info(f"Matched intent: {intent}")
            return response
        else:
            # Unknown query
            statistics_manager.track_user_message(command="unknown")
            statistics_manager.track_bot_response(is_unknown=True)
            logger.info(f"Unknown input after normalization: {normalized}")
            return "Sorry, I don't understand that yet. Try typing Help to see available commands."

chat_engine = ChatEngine()
