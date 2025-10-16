"""
Demo script for testing the non-LLM chatbot functionality.
This script demonstrates how to use the chatbot classes and Flask app.
"""

import sys
import os
import time
import logging

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from non_llm_chat.chatbot import BasicChatBot, ChatBotManager
from non_llm_chat.flask_app import ChatBotFlaskApp


def demo_basic_chatbot():
    """Demonstrate basic chatbot functionality."""
    print("=" * 50)
    print("DEMO: Basic Chatbot Functionality")
    print("=" * 50)
    
    # Create a chatbot
    bot = BasicChatBot("DemoBot")
    
    # Train with basic conversations
    print("Training chatbot with basic conversations...")
    bot.train_basic_conversations()
    
    # Test some interactions
    test_messages = [
        "Hello",
        "How are you?", 
        "What is your name?",
        "What can you do?",
        "What time is it?",
        "Thank you",
        "Goodbye"
    ]
    
    print("\nTesting chatbot responses:")
    print("-" * 30)
    
    for message in test_messages:
        response = bot.get_response(message)
        print(f"User: {message}")
        print(f"Bot:  {response}")
        print()
        time.sleep(1)  # Small delay for readability
    
    # Cleanup
    bot.cleanup()
    print("Demo completed successfully!")


def demo_chatbot_manager():
    """Demonstrate chatbot manager functionality."""
    print("\n" + "=" * 50)
    print("DEMO: Chatbot Manager")
    print("=" * 50)
    
    # Create manager
    manager = ChatBotManager()
    
    # Create multiple bots
    print("Creating multiple chatbots...")
    bot1 = manager.create_bot("FriendlyBot")
    bot2 = manager.create_bot("HelpfulBot")
    
    # Train them differently
    bot1.train_basic_conversations()
    
    # Custom training for HelpfulBot
    helpful_conversations = [
        "I need help",
        "I'm here to help! What do you need assistance with?",
        "How do I get started?",
        "Getting started is easy! Just ask me any question.",
        "What services do you offer?",
        "I offer helpful information and friendly conversation.",
    ]
    bot2.train_with_conversations(helpful_conversations)
    
    # List available bots
    print(f"Available bots: {manager.list_bots()}")
    
    # Test both bots
    test_message = "Hello, I need help"
    
    print(f"\nTesting message: '{test_message}'")
    print("-" * 30)
    
    response1 = bot1.get_response(test_message)
    response2 = bot2.get_response(test_message)
    
    print(f"FriendlyBot: {response1}")
    print(f"HelpfulBot:  {response2}")
    
    # Cleanup
    manager.cleanup_all()
    print("\nManager demo completed successfully!")


def demo_flask_app():
    """Demonstrate Flask app setup (without actually running it)."""
    print("\n" + "=" * 50)
    print("DEMO: Flask App Setup")
    print("=" * 50)
    
    print("Creating Flask chatbot application...")
    
    try:
        app = ChatBotFlaskApp(host="127.0.0.1", port=5000, debug=True)
        flask_app = app.get_app()
        
        print("Flask app created successfully!")
        print(f"Available routes:")
        for rule in flask_app.url_map.iter_rules():
            print(f"  {rule.rule} [{', '.join(rule.methods)}]")
        
        print("\nFlask app demo completed successfully!")
        print("Note: To actually run the app, use: python -m non_llm_chat.main --mode web")
        
    except ImportError as e:
        print(f"Warning: Flask not available ({e})")
        print("Install Flask to run the web interface: pip install Flask")


def main():
    """Run all demos."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    print("Non-LLM Chatbot Demo")
    print("Running comprehensive demonstration...")
    
    try:
        # Run demos
        demo_basic_chatbot()
        demo_chatbot_manager()
        demo_flask_app()
        
        print("\n" + "=" * 50)
        print("ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run web interface: python -m non_llm_chat.main --mode web")
        print("3. Run CLI interface: python -m non_llm_chat.main --mode cli")
        print("4. Deploy with Databricks Asset Bundle: databricks bundle deploy")
        
    except Exception as e:
        print(f"\nDemo failed with error: {str(e)}")
        logging.exception("Demo error details:")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())