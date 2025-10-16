"""
Enhanced Non-LLM Chatbot Examples and Testing
This script demonstrates various capabilities of the ChatterBot-powered chatbot.
"""

from datetime import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import os

def create_specialized_chatbot():
    """Create a chatbot with specialized training for specific domains"""
    
    # Create chatbot with different logic adapters
    chatbot = ChatBot(
        'Specialized Bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///specialized_bot.db',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I\'m still learning about that topic.',
                'maximum_similarity_threshold': 0.85
            },
            {
                'import_path': 'chatterbot.logic.MathematicalEvaluation'
            },
            {
                'import_path': 'chatterbot.logic.TimeLogicAdapter'
            }
        ]
    )
    
    # Train with specific domain knowledge
    trainer = ListTrainer(chatbot)
    
    # Programming and tech conversations
    programming_data = [
        "What is Python?",
        "Python is a high-level programming language known for its simplicity and readability.",
        "What is machine learning?",
        "Machine learning is a subset of AI that enables computers to learn from data without explicit programming.",
        "What is a database?",
        "A database is an organized collection of data that can be easily accessed, managed, and updated.",
        "What is an API?",
        "An API (Application Programming Interface) is a set of protocols for building software applications.",
        "What is debugging?",
        "Debugging is the process of finding and fixing errors or bugs in computer programs.",
        "What is version control?",
        "Version control is a system that tracks changes to files over time, like Git.",
    ]
    
    # Science conversations
    science_data = [
        "What is photosynthesis?",
        "Photosynthesis is the process by which plants convert sunlight into energy using chlorophyll.",
        "What is gravity?",
        "Gravity is a fundamental force that attracts objects with mass toward each other.",
        "What is DNA?",
        "DNA is the molecule that carries genetic information in living organisms.",
        "What is evolution?",
        "Evolution is the process by which species change over time through natural selection.",
    ]
    
    # Customer service conversations
    service_data = [
        "I need help with my account",
        "I'd be happy to help you with your account. What specific issue are you experiencing?",
        "How do I reset my password?",
        "To reset your password, go to the login page and click 'Forgot Password', then follow the instructions.",
        "When are you open?",
        "I'm available 24/7 to help answer your questions and provide support.",
        "Can I speak to a human?",
        "I'm an AI assistant, but I'm here to help! If you need human support, I can direct you to the right resources.",
    ]
    
    # Train with all datasets
    trainer.train(programming_data)
    trainer.train(science_data)
    trainer.train(service_data)
    
    return chatbot

def test_chatbot_capabilities():
    """Test various chatbot capabilities"""
    
    print("Creating and testing specialized chatbot...")
    bot = create_specialized_chatbot()
    
    # Test questions
    test_questions = [
        "What is Python?",
        "What is 5 + 7?",
        "What time is it?",
        "What is photosynthesis?",
        "I need help with my account",
        "How do I reset my password?",
        "Tell me about machine learning",
        "What is debugging?",
        "Hello there!",
        "What is the square root of 16?"
    ]
    
    print("\n" + "="*50)
    print("CHATBOT CAPABILITY TEST")
    print("="*50)
    
    for question in test_questions:
        try:
            response = bot.get_response(question)
            print(f"\nQ: {question}")
            print(f"A: {response}")
            print(f"Confidence: {response.confidence}")
        except Exception as e:
            print(f"\nQ: {question}")
            print(f"Error: {e}")
    
    print("\n" + "="*50)

def interactive_chat():
    """Run an interactive chat session"""
    
    print("Starting interactive chat...")
    bot = create_specialized_chatbot()
    
    print("\n" + "="*50)
    print("INTERACTIVE CHAT SESSION")
    print("Type 'quit' to exit")
    print("="*50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Bot: Goodbye! Thanks for chatting!")
                break
            
            if user_input:
                response = bot.get_response(user_input)
                print(f"Bot: {response}")
            else:
                print("Bot: Please say something!")
                
        except KeyboardInterrupt:
            print("\nBot: Goodbye! Thanks for chatting!")
            break
        except Exception as e:
            print(f"Bot: Sorry, I encountered an error: {e}")

if __name__ == "__main__":
    print("Enhanced Non-LLM Chatbot Demo")
    print("Choose an option:")
    print("1. Test chatbot capabilities")
    print("2. Interactive chat")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        test_chatbot_capabilities()
    elif choice == "2":
        interactive_chat()
    elif choice == "3":
        test_chatbot_capabilities()
        input("\nPress Enter to start interactive chat...")
        interactive_chat()
    else:
        print("Invalid choice. Running tests by default...")
        test_chatbot_capabilities()