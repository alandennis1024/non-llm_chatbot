#!/usr/bin/env python3
"""
Streamlit Web Interface for SimpleChatbot
Simple Python-only web interface with built-in chat components
"""

import streamlit as st
from non_llm_chat.SimpleChatbot import SimpleChatbot
import time

# Page configuration
st.set_page_config(
    page_title="🤖 Simple Non-LLM Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize chatbot in session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = SimpleChatbot()

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm a simple non-LLM chatbot. I use pattern matching and can help with conversations, math problems, and more. What would you like to chat about?"}
    ]

# Main interface
st.title("🤖 Simple Non-LLM Chatbot")
st.caption("Pattern-based • Math-enabled • Learning System")

# Sidebar with information and controls
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This chatbot uses:
    - Pattern matching for responses
    - SQLite database for learning
    - No external LLM services
    - Local conversation storage
    """)
    
    st.header("🎯 Try These Commands")
    st.write("""
    • "Hello!" - Basic greeting
    • "What is 15 + 27?" - Math problems  
    • "What time is it?" - Current time
    • "Tell me a joke" - Entertainment
    • "Show stats" - Statistics
    • "Export history" - Export chats
    """)
    
    # Stats section
    if st.button("📊 Get Stats"):
        try:
            stats = st.session_state.chatbot.get_conversation_stats()
            st.success(f"""
            **Chat Statistics:**
            - Total conversations: {stats['total_conversations']}
            - Average confidence: {stats['average_confidence']}
            - Unique questions: {stats['unique_inputs']}
            """)
        except Exception as e:
            st.error(f"Error getting stats: {e}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared! How can I help you?"}
        ]
        st.session_state.chatbot.conversation_history.clear()
        st.rerun()

# Chat interface
st.header("💬 Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chatbot.get_response(prompt)
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.caption("🔧 Built with Streamlit and custom pattern-matching engine")