"""
Simple Non-LLM Chatbot Implementation
This is a compatibility-focused implementation that doesn't rely on ChatterBot.
Instead, it uses rule-based responses, pattern                elif pattern_info['category'] == 'math':
                    # Extract math expression - look for sequences with numbers and operators
                    math_pattern = r'\d+(?:\s*[+\-*/]\s*\d+)+'
                    math_expr = re.search(math_pattern, user_input)
                    if math_expr:
                        response = self.handle_math(math_expr.group())
                        return response, confidenceing, and simple ML techniques.
"""

import re
import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import difflib
import random

class SimpleChatbot:
    def __init__(self, db_path: str = "simple_chatbot.db"):
        self.db_path = db_path
        self.conversation_history = []
        self.init_database()
        self.load_responses()
        self.user_context = {}
        
    def init_database(self):
        """Initialize SQLite database for storing conversations and learning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                confidence REAL DEFAULT 0.0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT NOT NULL,
                response TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                weight REAL DEFAULT 1.0
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Load initial patterns if database is new
        if self.is_database_empty():
            self.load_initial_patterns()
    
    def is_database_empty(self) -> bool:
        """Check if the patterns table is empty"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM patterns")
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0
    
    def load_initial_patterns(self):
        """Load initial conversation patterns into database"""
        initial_patterns = [
            # Greetings
            ("hello|hi|hey|good morning|good afternoon|good evening", 
             "Hello! How can I help you today?", "greeting", 1.0),
            ("how are you|how do you do", 
             "I'm doing well, thank you for asking! How are you?", "greeting", 1.0),
            
            # Questions about the bot
            ("what are you|who are you|what is your name", 
             "I'm a simple non-LLM chatbot built with Python. I use pattern matching and rule-based responses!", "identity", 1.0),
            ("what can you do|what are your capabilities", 
             "I can have conversations, answer basic questions, do simple math, tell time, and learn from our chats!", "capabilities", 1.0),
            
            # Math expressions - handled separately
            (r".*\d+\s*[\+\-\*\/]\s*\d+.*", "", "math", 2.0),
            
            # Time queries
            ("what time|current time|time now", "", "time", 2.0),
            ("what date|current date|today", "", "date", 2.0),
            
            # General conversation
            ("thank you|thanks", "You're welcome! Is there anything else I can help you with?", "gratitude", 1.0),
            ("goodbye|bye|see you|farewell", "Goodbye! It was nice chatting with you. Come back anytime!", "farewell", 1.0),
            ("help|assistance", "I'm here to help! You can ask me questions, chat with me, or ask me to solve simple math problems.", "help", 1.0),
            
            # Fun responses
            ("tell me a joke|joke|funny", "Why don't scientists trust atoms? Because they make up everything! 😄", "humor", 1.0),
            ("how old are you", "I was just created, so I'm practically a newborn in AI years!", "age", 1.0),
            
            # Default fallback
            (".*", "I understand you're trying to tell me something, but I'm not quite sure how to respond. Could you try rephrasing?", "fallback", 0.1)
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for pattern, response, category, weight in initial_patterns:
            cursor.execute(
                "INSERT INTO patterns (pattern, response, category, weight) VALUES (?, ?, ?, ?)",
                (pattern, response, category, weight)
            )
        
        conn.commit()
        conn.close()
    
    def load_responses(self):
        """Load response patterns from database"""
        self.patterns = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT pattern, response, category, weight FROM patterns ORDER BY weight DESC")
        
        for pattern, response, category, weight in cursor.fetchall():
            self.patterns.append({
                'pattern': re.compile(pattern, re.IGNORECASE),
                'response': response,
                'category': category,
                'weight': weight
            })
        
        conn.close()
    
    def handle_math(self, expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Clean the expression - remove extra words and keep only math parts
            # Extract numbers and operators
            expr = re.sub(r'[^\d\+\-\*\/\(\)\.\s]', '', expression)
            expr = re.sub(r'\s+', '', expr)
            
            # Only allow numbers and basic operators
            if not re.match(r'^[\d\+\-\*\/\(\)\.]+$', expr):
                return "I can only handle basic math with +, -, *, / and parentheses."
            
            # Evaluate safely
            result = eval(expr)
            return f"The answer is: {result}"
            
        except ZeroDivisionError:
            return "Oops! Division by zero is not allowed."
        except Exception as e:
            return f"I couldn't solve that math problem. Please check your expression."
    
    def handle_time_query(self) -> str:
        """Handle time-related queries"""
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')} on {now.strftime('%A, %B %d, %Y')}."
    
    def handle_date_query(self) -> str:
        """Handle date-related queries"""
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}."
    
    def find_best_response(self, user_input: str) -> Tuple[str, float]:
        """Find the best matching response for user input"""
        user_input = user_input.strip().lower()
        best_match = None
        best_confidence = 0.0
        
        for pattern_info in self.patterns:
            match = pattern_info['pattern'].search(user_input)
            if match:
                confidence = pattern_info['weight']
                
                # Handle special categories
                if pattern_info['category'] == 'math':
                    # Extract math expression
                    math_expr = re.search(r'[\d\+\-\*\/\(\)\.\s]+', user_input)
                    if math_expr:
                        response = self.handle_math(math_expr.group())
                        return response, confidence
                
                elif pattern_info['category'] == 'time':
                    return self.handle_time_query(), confidence
                
                elif pattern_info['category'] == 'date':
                    return self.handle_date_query(), confidence
                
                elif pattern_info['response']:  # Regular response
                    if confidence > best_confidence:
                        best_match = pattern_info['response']
                        best_confidence = confidence
        
        return best_match or "I'm not sure how to respond to that.", best_confidence
    
    def learn_from_conversation(self, user_input: str, bot_response: str, confidence: float):
        """Store conversation for potential learning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (user_input, bot_response, confidence) VALUES (?, ?, ?)",
            (user_input, bot_response, confidence)
        )
        conn.commit()
        conn.close()
    
    def get_conversation_stats(self) -> Dict:
        """Get statistics about conversations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM conversations")
        total_conversations = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(confidence) FROM conversations")
        avg_confidence = cursor.fetchone()[0] or 0.0
        
        cursor.execute("SELECT COUNT(DISTINCT user_input) FROM conversations")
        unique_inputs = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_conversations': total_conversations,
            'average_confidence': round(avg_confidence, 2),
            'unique_inputs': unique_inputs
        }
    
    def get_response(self, message: str) -> str:
        """Main method to get chatbot response"""
        try:
            # Handle empty messages
            if not message or not message.strip():
                return "Please say something! I'm here to chat with you."
            
            # Handle special commands
            if "conversation history" in message.lower() or "chat history" in message.lower():
                if self.conversation_history:
                    recent_history = self.conversation_history[-3:]
                    history_text = "\n".join([f"You: {q}\nMe: {a}" for q, a in recent_history])
                    return f"Here are our recent exchanges:\n\n{history_text}"
                else:
                    return "We haven't chatted yet! This is our first conversation."
            
            if "clear history" in message.lower():
                self.conversation_history.clear()
                return "Conversation history cleared! Starting fresh."
            
            if "stats" in message.lower() or "statistics" in message.lower():
                stats = self.get_conversation_stats()
                return f"Chat Statistics:\n• Total conversations: {stats['total_conversations']}\n• Average confidence: {stats['average_confidence']}\n• Unique questions: {stats['unique_inputs']}"
            
            # Get response using pattern matching
            response, confidence = self.find_best_response(message)
            
            # Learn from this conversation
            self.learn_from_conversation(message, response, confidence)
            
            # Store in conversation history
            self.conversation_history.append((message, response))
            if len(self.conversation_history) > 20:  # Keep last 20 exchanges
                self.conversation_history = self.conversation_history[-20:]
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try rephrasing your message."