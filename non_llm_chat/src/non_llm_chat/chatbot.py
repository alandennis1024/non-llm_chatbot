"""
Basic chatbot implementation using ChatterBot library.
This module provides a non-LLM chatbot for Databricks Asset Bundle deployment.
"""

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.response_selection import get_random_response
from chatterbot.logic import BestMatch
import logging
import os
from typing import List, Optional


class BasicChatBot:
    """
    A basic chatbot implementation using ChatterBot library.
    
    This chatbot uses predefined conversation patterns and does not rely on LLMs.
    It can be trained with conversation data and responds based on pattern matching.
    """
    
    def __init__(self, name: str = "NonLLMBot", database_path: str = "db.sqlite3"):
        """
        Initialize the chatbot.
        
        Args:
            name: Name of the chatbot
            database_path: Path to the SQLite database for storing conversations
        """
        self.name = name
        self.database_path = database_path
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize the chatbot
        self.bot = ChatBot(
            name,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri=f'sqlite:///{database_path}',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I am sorry, I do not understand. Could you please rephrase?',
                    'maximum_similarity_threshold': 0.90
                },
                {
                    'import_path': 'chatterbot.logic.MathematicalEvaluation',
                },
                {
                    'import_path': 'chatterbot.logic.TimeLogicAdapter',
                }
            ]
        )
        
        self.trainer = ChatterBotCorpusTrainer(self.bot)
        self.list_trainer = ListTrainer(self.bot)
        
        self.logger.info(f"Chatbot '{name}' initialized successfully")
    
    def train_with_corpus(self, corpus_name: str = 'chatterbot.corpus.english'):
        """
        Train the chatbot with a predefined corpus.
        
        Args:
            corpus_name: Name of the corpus to train with
        """
        try:
            self.logger.info(f"Training chatbot with corpus: {corpus_name}")
            self.trainer.train(corpus_name)
            self.logger.info("Training completed successfully")
        except Exception as e:
            self.logger.error(f"Error during corpus training: {str(e)}")
            raise
    
    def train_with_conversations(self, conversations: List[str]):
        """
        Train the chatbot with custom conversation data.
        
        Args:
            conversations: List of conversation strings
        """
        try:
            self.logger.info("Training chatbot with custom conversations")
            self.list_trainer.train(conversations)
            self.logger.info("Custom training completed successfully")
        except Exception as e:
            self.logger.error(f"Error during custom training: {str(e)}")
            raise
    
    def get_response(self, message: str) -> str:
        """
        Get a response from the chatbot for the given message.
        
        Args:
            message: Input message from the user
            
        Returns:
            Response string from the chatbot
        """
        try:
            self.logger.info(f"Processing message: {message}")
            response = self.bot.get_response(message)
            self.logger.info(f"Generated response: {response}")
            return str(response)
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I encountered an error processing your message."
    
    def train_basic_conversations(self):
        """Train the chatbot with basic conversation patterns."""
        basic_conversations = [
            "Hello",
            "Hi there!",
            "How are you?",
            "I am doing well, thank you for asking.",
            "What is your name?",
            f"My name is {self.name}.",
            "What can you do?",
            "I can chat with you and answer basic questions.",
            "Goodbye",
            "Goodbye! Have a great day!",
            "Thank you",
            "You're welcome!",
            "What time is it?",
            "I can help you with time-related questions.",
            "What is 2 + 2?",
            "2 + 2 equals 4.",
            "Help",
            "I'm here to help! You can ask me questions and I'll do my best to respond.",
        ]
        
        self.train_with_conversations(basic_conversations)
    
    def cleanup(self):
        """Clean up resources."""
        try:
            if hasattr(self.bot, 'storage'):
                self.bot.storage.drop()
            self.logger.info("Chatbot cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")


class ChatBotManager:
    """
    Manager class for handling multiple chatbot instances and their lifecycle.
    """
    
    def __init__(self):
        """Initialize the chatbot manager."""
        self.bots = {}
        self.logger = logging.getLogger(__name__)
    
    def create_bot(self, name: str, database_path: Optional[str] = None) -> BasicChatBot:
        """
        Create a new chatbot instance.
        
        Args:
            name: Name of the chatbot
            database_path: Optional custom database path
            
        Returns:
            BasicChatBot instance
        """
        if database_path is None:
            database_path = f"{name.lower()}_db.sqlite3"
        
        bot = BasicChatBot(name, database_path)
        self.bots[name] = bot
        self.logger.info(f"Created chatbot: {name}")
        return bot
    
    def get_bot(self, name: str) -> Optional[BasicChatBot]:
        """
        Get an existing chatbot by name.
        
        Args:
            name: Name of the chatbot
            
        Returns:
            BasicChatBot instance or None if not found
        """
        return self.bots.get(name)
    
    def remove_bot(self, name: str) -> bool:
        """
        Remove a chatbot instance.
        
        Args:
            name: Name of the chatbot to remove
            
        Returns:
            True if removed successfully, False if not found
        """
        if name in self.bots:
            self.bots[name].cleanup()
            del self.bots[name]
            self.logger.info(f"Removed chatbot: {name}")
            return True
        return False
    
    def list_bots(self) -> List[str]:
        """
        List all available chatbot names.
        
        Returns:
            List of chatbot names
        """
        return list(self.bots.keys())
    
    def cleanup_all(self):
        """Clean up all chatbot instances."""
        for bot_name in list(self.bots.keys()):
            self.remove_bot(bot_name)
        self.logger.info("All chatbots cleaned up")