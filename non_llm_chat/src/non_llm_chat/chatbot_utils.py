"""
Chatbot Utilities and Configurations
Different chatbot configurations for various use cases.
"""

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import os
import json
from datetime import datetime

class ChatbotFactory:
    """Factory class for creating different types of chatbots"""
    
    @staticmethod
    def create_basic_chatbot(name="BasicBot"):
        """Create a basic chatbot with minimal training"""
        return ChatBot(
            name,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri=f'sqlite:///{name.lower()}.db',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I need more training to understand that.',
                    'maximum_similarity_threshold': 0.90
                }
            ]
        )
    
    @staticmethod
    def create_math_chatbot(name="MathBot"):
        """Create a chatbot specialized in mathematical operations"""
        return ChatBot(
            name,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri=f'sqlite:///{name.lower()}.db',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.MathematicalEvaluation'
                },
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I can help with math problems. Try asking me to calculate something!',
                    'maximum_similarity_threshold': 0.80
                }
            ]
        )
    
    @staticmethod
    def create_time_chatbot(name="TimeBot"):
        """Create a chatbot specialized in time-related queries"""
        return ChatBot(
            name,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri=f'sqlite:///{name.lower()}.db',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.TimeLogicAdapter'
                },
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I can tell you about time-related information.',
                    'maximum_similarity_threshold': 0.80
                }
            ]
        )
    
    @staticmethod
    def create_customer_service_chatbot(name="ServiceBot"):
        """Create a chatbot for customer service scenarios"""
        return ChatBot(
            name,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri=f'sqlite:///{name.lower()}.db',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I\'m here to help! Could you please provide more details about your issue?',
                    'maximum_similarity_threshold': 0.85
                }
            ]
        )

class ChatbotTrainer:
    """Utility class for training chatbots with different datasets"""
    
    def __init__(self, chatbot):
        self.chatbot = chatbot
        self.corpus_trainer = ChatterBotCorpusTrainer(chatbot)
        self.list_trainer = ListTrainer(chatbot)
    
    def train_with_corpus(self, corpus_name):
        """Train with ChatterBot corpus"""
        self.corpus_trainer.train(corpus_name)
    
    def train_with_custom_data(self, conversation_list):
        """Train with custom conversation data"""
        self.list_trainer.train(conversation_list)
    
    def train_customer_service(self):
        """Train for customer service scenarios"""
        service_data = [
            "Hello, I need help",
            "Hello! I'm here to assist you. What can I help you with today?",
            "I have a problem with my order",
            "I'm sorry to hear about the issue with your order. Can you provide your order number?",
            "My account is locked",
            "I can help you with account issues. Have you tried resetting your password?",
            "How do I contact support?",
            "You can contact our support team through email or phone. Would you like those details?",
            "Is there a warranty?",
            "Yes, most of our products come with a warranty. The duration depends on the specific product.",
            "Can I return this item?",
            "Returns are typically accepted within 30 days of purchase. Do you have your receipt?",
            "What are your business hours?",
            "Our customer service is available Monday through Friday, 9 AM to 6 PM EST.",
            "Thank you for your help",
            "You're very welcome! Is there anything else I can assist you with today?"
        ]
        self.train_with_custom_data(service_data)
    
    def train_technical_support(self):
        """Train for technical support scenarios"""
        tech_data = [
            "My computer won't start",
            "Let's troubleshoot this step by step. First, check if the power cable is properly connected.",
            "The internet is not working",
            "I can help with internet connectivity issues. Are you using WiFi or ethernet?",
            "How do I install this software?",
            "Software installation varies by program. Do you have the installer file ready?",
            "My phone keeps crashing",
            "Phone crashes can be caused by various issues. Have you tried restarting your device?",
            "I forgot my password",
            "No problem! Most systems have a 'Forgot Password' option on the login page.",
            "The app won't open",
            "App issues can often be resolved by closing and reopening the app, or restarting your device.",
            "How do I backup my files?",
            "File backup is important! You can use cloud storage services or external drives.",
            "My printer isn't working",
            "Printer issues are common. First, check if it's properly connected and has paper and ink."
        ]
        self.train_with_custom_data(tech_data)
    
    def train_educational(self):
        """Train for educational scenarios"""
        edu_data = [
            "What is artificial intelligence?",
            "Artificial Intelligence is the simulation of human intelligence in machines that are programmed to think and learn.",
            "Explain machine learning",
            "Machine learning is a method of data analysis that automates analytical model building using algorithms that learn from data.",
            "What is programming?",
            "Programming is the process of creating instructions for computers using programming languages.",
            "How do computers work?",
            "Computers work by processing data through a series of electronic circuits following programmed instructions.",
            "What is the internet?",
            "The internet is a global network of interconnected computers that communicate using standardized protocols.",
            "What is a database?",
            "A database is an organized collection of structured information stored electronically in a computer system.",
            "Explain cloud computing",
            "Cloud computing delivers computing services over the internet, including storage, processing power, and software.",
            "What is cybersecurity?",
            "Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks."
        ]
        self.train_with_custom_data(edu_data)

class ConversationLogger:
    """Utility class for logging and analyzing conversations"""
    
    def __init__(self, log_file="conversation_log.json"):
        self.log_file = log_file
        self.conversations = self.load_conversations()
    
    def load_conversations(self):
        """Load existing conversations from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def log_conversation(self, user_input, bot_response, confidence=None):
        """Log a conversation exchange"""
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'bot_response': bot_response,
            'confidence': confidence
        }
        self.conversations.append(conversation)
        self.save_conversations()
    
    def save_conversations(self):
        """Save conversations to file"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, indent=2, ensure_ascii=False)
    
    def get_recent_conversations(self, count=10):
        """Get recent conversations"""
        return self.conversations[-count:] if self.conversations else []
    
    def analyze_conversations(self):
        """Analyze conversation patterns"""
        if not self.conversations:
            return "No conversations to analyze."
        
        total_conversations = len(self.conversations)
        
        # Calculate average confidence if available
        confidences = [c.get('confidence', 0) for c in self.conversations if c.get('confidence')]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Find most common topics (simple keyword analysis)
        all_inputs = ' '.join([c['user_input'].lower() for c in self.conversations])
        common_words = {}
        for word in all_inputs.split():
            if len(word) > 3:  # Ignore short words
                common_words[word] = common_words.get(word, 0) + 1
        
        # Get top 5 most common words
        top_words = sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:5]
        
        analysis = f"""
Conversation Analysis:
- Total conversations: {total_conversations}
- Average confidence: {avg_confidence:.2f}
- Common topics: {', '.join([word for word, count in top_words])}
- Most recent conversation: {self.conversations[-1]['timestamp'] if self.conversations else 'None'}
        """
        
        return analysis.strip()

# Example usage and testing functions
def demo_different_chatbots():
    """Demonstrate different types of chatbots"""
    
    print("Creating different specialized chatbots...")
    
    # Create different chatbot types
    math_bot = ChatbotFactory.create_math_chatbot("MathBot")
    time_bot = ChatbotFactory.create_time_chatbot("TimeBot")
    service_bot = ChatbotFactory.create_customer_service_chatbot("ServiceBot")
    
    # Train service bot
    service_trainer = ChatbotTrainer(service_bot)
    service_trainer.train_customer_service()
    
    # Test each bot
    test_cases = [
        (math_bot, "What is 15 + 25?", "Math Bot"),
        (time_bot, "What time is it?", "Time Bot"),
        (service_bot, "I need help with my order", "Service Bot")
    ]
    
    print("\n" + "="*50)
    print("SPECIALIZED CHATBOT DEMO")
    print("="*50)
    
    for bot, question, bot_name in test_cases:
        try:
            response = bot.get_response(question)
            print(f"\n{bot_name}:")
            print(f"Q: {question}")
            print(f"A: {response}")
        except Exception as e:
            print(f"\n{bot_name} Error: {e}")

if __name__ == "__main__":
    demo_different_chatbots()