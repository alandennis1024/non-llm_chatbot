#!/usr/bin/env python3
"""
FastAPI Web Interface for SimpleChatbot
Modern async web interface with automatic API documentation
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from non_llm_chat.SimpleChatbot import SimpleChatbot
import os

app = FastAPI(
    title="Simple Non-LLM Chatbot API",
    description="A pattern-based chatbot with learning capabilities",
    version="1.0.0"
)

# Initialize chatbot
chatbot = SimpleChatbot()

# Request/Response models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

class StatsResponse(BaseModel):
    total_conversations: int
    average_confidence: float
    unique_inputs: int

# API endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Send a message to the chatbot and get a response"""
    try:
        if not chat_message.message.strip():
            raise HTTPException(status_code=400, detail="Empty message")
        
        response = chatbot.get_response(chat_message.message)
        return ChatResponse(response=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get chatbot conversation statistics"""
    try:
        stats = chatbot.get_conversation_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history():
    """Get recent conversation history"""
    try:
        history = chatbot.conversation_history[-10:]  # Last 10 conversations
        return {
            "history": [{"user": q, "bot": a} for q, a in history],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main chat interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 FastAPI Chatbot</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .chat-container { border: 1px solid #ddd; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
            .message { margin: 10px 0; padding: 8px; border-radius: 5px; }
            .user { background: #e3f2fd; text-align: right; }
            .bot { background: #f3e5f5; }
            .input-container { display: flex; gap: 10px; }
            input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .api-link { margin-top: 20px; text-align: center; }
        </style>
    </head>
    <body>
        <h1>🤖 FastAPI Chatbot</h1>
        <p>Modern async chatbot with automatic API documentation</p>
        
        <div id="chatContainer" class="chat-container">
            <div class="message bot">
                <strong>Bot:</strong> Hello! I'm a FastAPI-powered chatbot. Try asking me something!
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
            <button onclick="getStats()">Stats</button>
        </div>
        
        <div class="api-link">
            <p><strong>🔗 API Documentation:</strong> <a href="/docs" target="_blank">Interactive API Docs</a> | <a href="/redoc" target="_blank">ReDoc</a></p>
        </div>
        
        <script>
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;
                
                addMessage(message, 'user');
                input.value = '';
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    addMessage(data.response || data.detail, 'bot');
                } catch (error) {
                    addMessage('Error: ' + error.message, 'bot');
                }
            }
            
            async function getStats() {
                try {
                    const response = await fetch('/api/stats');
                    const data = await response.json();
                    const statsMsg = `Stats: ${data.total_conversations} conversations, ${data.average_confidence} avg confidence, ${data.unique_inputs} unique inputs`;
                    addMessage(statsMsg, 'bot');
                } catch (error) {
                    addMessage('Error getting stats', 'bot');
                }
            }
            
            function addMessage(text, sender) {
                const container = document.getElementById('chatContainer');
                const div = document.createElement('div');
                div.className = `message ${sender}`;
                div.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Bot'}:</strong> ${text}`;
                container.appendChild(div);
                container.scrollTop = container.scrollHeight;
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') sendMessage();
            }
            
            document.getElementById('messageInput').focus();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI Chatbot Server...")
    print("🌐 Main Interface: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)