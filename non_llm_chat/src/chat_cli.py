#!/usr/bin/env python3
"""
Command-line Non-LLM Chatbot
A simple, reliable chatbot interface that runs in the terminal
"""

from non_llm_chat.SimpleChatbot import SimpleChatbot
import sys

def main():
    print("="*60)
    print("🤖 SIMPLE NON-LLM CHATBOT")
    print("="*60)
    print("Welcome! This chatbot uses pattern matching and rule-based responses.")
    print("It can handle conversations, math problems, time queries, and more.")
    print("Type 'quit', 'exit', or press Ctrl+C to end the conversation.")
    print("Try: 'hello', 'what is 2+3?', 'what time is it?', 'tell me a joke'")
    print("-"*60)
    
    # Initialize chatbot
    try:
        chatbot = SimpleChatbot()
        print("✅ Chatbot initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return
    
    print("🎉 Ready to chat! Type your message:")
    print("-"*60)
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🤖 Bot: Goodbye! Thanks for chatting with me. Have a great day! 👋")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Get and display bot response
            response = chatbot.get_response(user_input)
            print(f"🤖 Bot: {response}")
            
        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Goodbye! Thanks for chatting with me. Have a great day! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again with a different message.")

if __name__ == "__main__":
    main()