#!/usr/bin/env python3
"""
Flask Web Interface for SimpleChatbot
Simple, reliable web interface with no complex dependencies
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Try to use EnhancedChatbot first, fallback to SimpleChatbot if issues
try:
    from non_llm_chat.enhanced_chatbot import EnhancedChatbot
    chatbot = EnhancedChatbot()
    chatbot_type = "Enhanced (ChatterBot)"
    print("✅ Using EnhancedChatbot with ChatterBot")
except Exception as e:
    print(f"⚠️ ChatterBot compatibility issue: {e}")
    print("🔄 Falling back to SimpleChatbot...")
    try:
        from non_llm_chat.SimpleChatbot import SimpleChatbot
        chatbot = SimpleChatbot()
        chatbot_type = "Simple (Pattern-based)"
        print("✅ Using SimpleChatbot (pattern-based)")
    except Exception as e2:
        print(f"❌ Error loading any chatbot: {e2}")
        chatbot = None
        chatbot_type = "Error"

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Handle chat messages via API"""
    try:
        if chatbot is None:
            return jsonify({
                'error': 'Chatbot not initialized. Please check server logs.',
                'status': 'error'
            }), 500
        
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        response = chatbot.get_response(message)
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get chatbot statistics"""
    try:
        if chatbot is None:
            return jsonify({'error': 'Chatbot not initialized', 'status': 'error'}), 500
            
        # Try to get stats from enhanced chatbot first
        if hasattr(chatbot, 'get_conversation_stats'):
            stats = chatbot.get_conversation_stats()
        else:
            # Fallback stats for basic chatbots
            stats = {
                'total_conversations': len(getattr(chatbot, 'conversation_history', [])),
                'average_confidence': 0.0,
                'unique_inputs': len(set([q for q, a in getattr(chatbot, 'conversation_history', [])]))
            }
        
        # Add chatbot type info
        stats['chatbot_type'] = chatbot_type
        
        return jsonify({
            'stats': stats,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/history')
def get_history():
    """Get conversation history"""
    try:
        if chatbot is None:
            return jsonify({'error': 'Chatbot not initialized', 'status': 'error'}), 500
            
        # Get recent conversations - handle both chatbot types
        if hasattr(chatbot, 'conversation_history'):
            history = chatbot.conversation_history[-10:]  # Last 10 conversations
            return jsonify({
                'history': [{'user': q, 'bot': a} for q, a in history],
                'status': 'success'
            })
        else:
            return jsonify({
                'history': [],
                'message': 'No conversation history available',
                'status': 'success'
            })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🚀 Starting Flask Chatbot Server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000)