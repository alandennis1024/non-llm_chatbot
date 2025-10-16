
from datetime import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import os
import json

class EnhancedChatbot:
    def __init__(self):
        # Initialize ChatterBot with multiple adapters
        self.chatbot = ChatBot(
            'Enhanced Non-LLM Chatbot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///chatbot.db',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I am sorry, but I do not understand. Could you please rephrase that?',
                    'maximum_similarity_threshold': 0.90
                },
                {
                    'import_path': 'chatterbot.logic.MathematicalEvaluation'
                },
                {
                    'import_path': 'chatterbot.logic.TimeLogicAdapter'
                }
            ]
        )
        
        # Initialize trainers
        self.corpus_trainer = ChatterBotCorpusTrainer(self.chatbot)
        self.list_trainer = ListTrainer(self.chatbot)
        
        # Train the chatbot if not already trained
        self.train_chatbot()
        
        # Custom conversation history
        self.conversation_history = []
    
    def train_chatbot(self):
        """Train the chatbot with corpus data and custom conversations"""
        db_path = 'chatbot.db'
        
        # Only train if database doesn't exist (first run)
        if not os.path.exists(db_path):
            print("Training chatbot... This may take a moment.")
            
            # Train with English corpus
            self.corpus_trainer.train("chatterbot.corpus.english.greetings")
            self.corpus_trainer.train("chatterbot.corpus.english.conversations")
            
            # Custom training data for specific topics
            custom_conversations = [
                "Hello",
                "Hi there! How can I help you today?",
                "What can you do?",
                "I can have conversations, solve math problems, tell time, and learn from our chats!",
                "What is your name?",
                "I'm an Enhanced Non-LLM Chatbot built with ChatterBot.",
                "How are you?",
                "I'm doing well, thank you for asking! How are you?",
                "What is the weather like?",
                "I don't have access to weather data, but you can check your local weather service.",
                "Tell me a joke",
                "Why don't scientists trust atoms? Because they make up everything!",
                "What programming language are you written in?",
                "I'm written in Python using the ChatterBot library.",
                "Can you help with math?",
                "Yes! I can solve basic mathematical expressions. Try asking me something like 'what is 2 + 2?'",
                "Goodbye",
                "Goodbye! It was nice chatting with you!"
            ]
            
            self.list_trainer.train(custom_conversations)
            print("Training completed!")
    
    def get_response(self, message):
        """Get response from the chatbot with custom handling"""
        try:
            # Handle empty messages
            if not message or not message.strip():
                return "Please say something! I'm here to chat."
            
            # Custom time handling (enhanced from original)
            if any(word in message.lower() for word in ['time', 'clock', 'hour']):
                now = datetime.now()
                return f"The current time is {now.strftime('%H:%M:%S')} on {now.strftime('%Y-%m-%d')}."
            
            # Handle conversation history requests
            if "conversation history" in message.lower() or "chat history" in message.lower():
                if self.conversation_history:
                    history = "\n".join([f"You: {q}\nBot: {a}" for q, a in self.conversation_history[-3:]])
                    return f"Here are our last few exchanges:\n{history}"
                else:
                    return "We haven't chatted yet! This is our first conversation."
            
            # Clear conversation history
            if "clear history" in message.lower():
                self.conversation_history.clear()
                return "Conversation history cleared!"
            
            # Get response from ChatterBot
            response = self.chatbot.get_response(message)
            
            # Store conversation in history
            self.conversation_history.append((message, str(response)))
            
            # Keep only last 10 conversations
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return str(response)
            
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try rephrasing your message."
