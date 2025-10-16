#!/usr/bin/env python3
"""
Test script for the Simple Chatbot
"""

from non_llm_chat.SimpleChatbot import SimpleChatbot

def test_chatbot():
    print("Testing Simple Chatbot...")
    chatbot = SimpleChatbot()
    
    # Test basic functionality
    test_messages = [
        "Hello!",
        "What can you do?",
        "What is 2 + 3?", 
        "What time is it?",
        "Tell me a joke",
        "Thank you",
        "Goodbye"
    ]
    
    print("\n" + "="*50)
    print("CHATBOT TEST RESULTS")
    print("="*50)
    
    for message in test_messages:
        response = chatbot.get_response(message)
        print(f"\nUser: {message}")
        print(f"Bot:  {response}")
        print("-" * 40)
    
    # Test stats
    print(f"\nUser: show stats")
    stats_response = chatbot.get_response("show stats")
    print(f"Bot:  {stats_response}")
    
    print("\n" + "="*50)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*50)

if __name__ == "__main__":
    test_chatbot()