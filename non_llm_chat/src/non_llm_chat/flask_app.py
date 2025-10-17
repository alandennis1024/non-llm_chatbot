"""
Flask web application for the non-LLM chatbot.
Provides REST API endpoints for chatbot interaction.
"""

from flask import Flask, request, jsonify, render_template_string
from chatbot import BasicChatBot, ChatBotManager
import logging
import sys
import os
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class ChatBotFlaskApp:
    """Flask application wrapper for the chatbot."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        """
        Initialize the Flask application.
        
        Args:
            host: Host address to bind to
            port: Port number to bind to
            debug: Enable debug mode
        """
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Creating bot manager")
        # Initialize chatbot manager
        self.bot_manager = ChatBotManager()
        self.logger.info("Bot manager created")
        # Create default chatbot
        self.default_bot = self.bot_manager.create_bot("DefaultBot")
        self.logger.info("Created default bot")
        self.default_bot.train_basic_conversations()
        self.logger.info("Default bot trained with basic conversations")
        # Set up routes
        self._setup_routes()
        self.logger.info("Set up routes")
        self.logger.info("Flask chatbot application initialized")
    
    def _setup_routes(self):
        """Set up Flask routes."""
        
        @self.app.route('/')
        def index():
            """Serve the main chat interface."""
            return render_template_string(self._get_chat_template())
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            """
            Chat endpoint for sending messages to the bot.
            
            Expected JSON payload:
            {
                "message": "user message",
                "bot_name": "optional bot name"
            }
            
            Returns:
            {
                "response": "bot response",
                "bot_name": "bot name used",
                "status": "success"
            }
            """
            try:
                data = request.get_json()
                
                if not data or 'message' not in data:
                    return jsonify({
                        "error": "Missing 'message' in request body",
                        "status": "error"
                    }), 400
                
                message = data['message']
                bot_name = data.get('bot_name', 'DefaultBot')
                
                # Get the specified bot or use default
                bot = self.bot_manager.get_bot(bot_name)
                if bot is None:
                    bot = self.default_bot
                    bot_name = "DefaultBot"
                
                # Get response from bot
                response = bot.get_response(message)
                
                return jsonify({
                    "response": response,
                    "bot_name": bot_name,
                    "status": "success"
                })
                
            except Exception as e:
                self.logger.error(f"Error in chat endpoint: {str(e)}")
                return jsonify({
                    "error": "Internal server error",
                    "status": "error"
                }), 500
        
        @self.app.route('/api/bots', methods=['GET'])
        def list_bots():
            """
            List all available bots.
            
            Returns:
            {
                "bots": ["bot1", "bot2", ...],
                "status": "success"
            }
            """
            try:
                bots = self.bot_manager.list_bots()
                return jsonify({
                    "bots": bots,
                    "status": "success"
                })
            except Exception as e:
                self.logger.error(f"Error listing bots: {str(e)}")
                return jsonify({
                    "error": "Internal server error",
                    "status": "error"
                }), 500
        
        @self.app.route('/api/bots', methods=['POST'])
        def create_bot():
            """
            Create a new bot.
            
            Expected JSON payload:
            {
                "name": "bot name",
                "train_basic": true (optional)
            }
            
            Returns:
            {
                "message": "Bot created successfully",
                "bot_name": "created bot name",
                "status": "success"
            }
            """
            try:
                data = request.get_json()
                
                if not data or 'name' not in data:
                    return jsonify({
                        "error": "Missing 'name' in request body",
                        "status": "error"
                    }), 400
                
                bot_name = data['name']
                train_basic = data.get('train_basic', True)
                
                # Check if bot already exists
                if self.bot_manager.get_bot(bot_name):
                    return jsonify({
                        "error": f"Bot '{bot_name}' already exists",
                        "status": "error"
                    }), 400
                
                # Create new bot
                new_bot = self.bot_manager.create_bot(bot_name)
                
                if train_basic:
                    new_bot.train_basic_conversations()
                
                return jsonify({
                    "message": "Bot created successfully",
                    "bot_name": bot_name,
                    "status": "success"
                })
                
            except Exception as e:
                self.logger.error(f"Error creating bot: {str(e)}")
                return jsonify({
                    "error": "Internal server error",
                    "status": "error"
                }), 500
        
        @self.app.route('/api/train', methods=['POST'])
        def train_bot():
            """
            Train a bot with custom conversations.
            
            Expected JSON payload:
            {
                "bot_name": "bot name",
                "conversations": ["message1", "response1", "message2", "response2", ...]
            }
            
            Returns:
            {
                "message": "Training completed successfully",
                "status": "success"
            }
            """
            try:
                data = request.get_json()
                
                if not data or 'bot_name' not in data or 'conversations' not in data:
                    return jsonify({
                        "error": "Missing 'bot_name' or 'conversations' in request body",
                        "status": "error"
                    }), 400
                
                bot_name = data['bot_name']
                conversations = data['conversations']
                
                # Get the bot
                bot = self.bot_manager.get_bot(bot_name)
                if bot is None:
                    return jsonify({
                        "error": f"Bot '{bot_name}' not found",
                        "status": "error"
                    }), 404
                
                # Train the bot
                bot.train_with_conversations(conversations)
                
                return jsonify({
                    "message": "Training completed successfully",
                    "status": "success"
                })
                
            except Exception as e:
                self.logger.error(f"Error training bot: {str(e)}")
                return jsonify({
                    "error": "Internal server error",
                    "status": "error"
                }), 500
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                "status": "healthy",
                "service": "non-llm-chatbot"
            })
    
    def _get_chat_template(self) -> str:
        """Get the HTML template for the chat interface."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Non-LLM Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chat-messages {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 20px;
            background-color: #fafafa;
        }
        .message {
            margin-bottom: 10px;
            padding: 8px 12px;
            border-radius: 18px;
            max-width: 70%;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .bot-message {
            background-color: #e9ecef;
            color: #333;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        #messageInput {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        #sendButton {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        #sendButton:hover {
            background-color: #0056b3;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>Non-LLM Chatbot</h1>
            <p>Chat with our basic pattern-matching chatbot!</p>
        </div>
        
        <div id="chatMessages" class="chat-messages">
            <div class="message bot-message">
                Hello! I'm a non-LLM chatbot. How can I help you today?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
            <button id="sendButton" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function addMessage(message, isUser) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.textContent = message;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, true);
            input.value = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message
                    })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    addMessage(data.response, false);
                } else {
                    addMessage('Sorry, I encountered an error. Please try again.', false);
                }
            } catch (error) {
                console.error('Error:', error);
                addMessage('Sorry, I encountered an error. Please try again.', false);
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>
        """
    
    def run(self):
        """Run the Flask application."""
        self.logger.info(f"Starting Flask app on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=self.debug)
    
    def get_app(self):
        """Get the Flask application instance."""
        return self.app


def create_app() -> Flask:
    """
    Factory function to create a Flask application instance.
    
    Returns:
        Flask application instance
    """
    chatbot_app = ChatBotFlaskApp(debug=True)
    return chatbot_app.get_app()