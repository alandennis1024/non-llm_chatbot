#!/usr/bin/env python3
"""
Simple Flask Test - Debug Version
Testing Flask functionality step by step
"""

import os
import sys

print("🔧 Flask Debug Test Starting...")
print(f"📁 Current directory: {os.getcwd()}")

# Test 1: Import tests
try:
    print("1️⃣ Testing Flask import...")
    from flask import Flask
    print("✅ Flask imported successfully")
except Exception as e:
    print(f"❌ Flask import failed: {e}")
    sys.exit(1)

# Test 2: Chatbot import tests
print("2️⃣ Testing chatbot imports...")

# Try enhanced chatbot first
try:
    from non_llm_chat.enhanced_chatbot import EnhancedChatbot
    chatbot = EnhancedChatbot()
    chatbot_type = "Enhanced (ChatterBot)"
    print("✅ EnhancedChatbot loaded successfully")
except Exception as e:
    print(f"⚠️ EnhancedChatbot failed: {e}")
    
    # Fallback to SimpleChatbot
    try:
        from non_llm_chat.SimpleChatbot import SimpleChatbot
        chatbot = SimpleChatbot()
        chatbot_type = "Simple (Pattern-based)"
        print("✅ SimpleChatbot loaded successfully")
    except Exception as e2:
        print(f"❌ SimpleChatbot also failed: {e2}")
        print("Creating basic fallback chatbot...")
        
        class BasicChatbot:
            def __init__(self):
                self.conversation_history = []
            
            def get_response(self, message):
                if "hello" in message.lower():
                    return "Hello! I'm a basic fallback chatbot."
                elif "time" in message.lower():
                    from datetime import datetime
                    return f"Current time: {datetime.now().strftime('%H:%M:%S')}"
                else:
                    return f"You said: {message}. This is a basic fallback response."
        
        chatbot = BasicChatbot()
        chatbot_type = "Basic Fallback"
        print("✅ Basic fallback chatbot created")

# Test 3: Chatbot functionality
print("3️⃣ Testing chatbot response...")
try:
    test_response = chatbot.get_response("Hello!")
    print(f"✅ Chatbot response: {test_response}")
except Exception as e:
    print(f"❌ Chatbot test failed: {e}")

# Test 4: Flask app creation
print("4️⃣ Creating Flask app...")
try:
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return f"""
        <html>
        <head><title>Flask Test</title></head>
        <body>
            <h1>🤖 Flask Chatbot Test</h1>
            <p><strong>Status:</strong> ✅ Server Running</p>
            <p><strong>Chatbot Type:</strong> {chatbot_type}</p>
            <p><strong>Test Response:</strong> {chatbot.get_response('Hello test!')}</p>
            <hr>
            <form action="/chat" method="post">
                <input type="text" name="message" placeholder="Type a message..." style="width: 300px; padding: 5px;">
                <button type="submit" style="padding: 5px 10px;">Send</button>
            </form>
        </body>
        </html>
        """
    
    @app.route('/chat', methods=['POST'])
    def chat():
        from flask import request
        message = request.form.get('message', '')
        if message:
            response = chatbot.get_response(message)
            return f"""
            <html>
            <head><title>Chat Response</title></head>
            <body>
                <h2>Chat Response</h2>
                <p><strong>You:</strong> {message}</p>
                <p><strong>Bot:</strong> {response}</p>
                <a href="/">← Back to chat</a>
            </body>
            </html>
            """
        return "No message received"
    
    print("✅ Flask app created successfully")
    
except Exception as e:
    print(f"❌ Flask app creation failed: {e}")
    sys.exit(1)

# Test 5: Start server
print("5️⃣ Starting Flask server...")
print("🌐 Server will start at: http://localhost:5000")
print("🛑 Press Ctrl+C to stop")

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Server failed to start: {e}")