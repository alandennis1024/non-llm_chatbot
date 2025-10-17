"""
Non-LLM Chatbot Package

A Flask-based chatbot implementation using ChatterBot library for Databricks Asset Bundle deployment.
This package provides basic chatbot functionality without relying on large language models.
"""

from .chatbot import BasicChatBot, ChatBotManager
from .flask_app import ChatBotFlaskApp, create_app
from .main import main, databricks_main

__version__ = "0.0.1"
__author__ = "alan.dennis@gmail.com"

__all__ = [
    "BasicChatBot",
    "ChatBotManager", 
    "ChatBotFlaskApp",
    "create_app",
    "main",
    "databricks_main"
]